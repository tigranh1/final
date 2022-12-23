from flask import Flask, redirect, url_for, render_template, request, session, flash

#for login session time
from datetime import timedelta
from flask_sqlalchemy import  SQLAlchemy
import pymysql
import os

import json


with open('news/news.json') as n:
   newsposts = json.load(n)

with open('events/events.json') as e:
   newevents = json.load(e)

app = Flask(__name__)


#logined session lifetime set
app.permanent_session_lifetime = timedelta(days=3)

#db - sqllite:// - WORD - this word will be the name of database we want to make
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:new_password@localhost/ORMBD'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"
#encrypt data
app.secret_key = "teamo"

db = SQLAlchemy(app)

#creating class for users - with the same logic I guess I should make classes for content


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class users(db.Model):

    __tablename__ = 'users'
    
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    #for representing users
    def __repr__(self) -> str:
        return "<Name %>" % self.name


@app.route("/")
def home():
    return render_template("index.html", content="Testing")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        #session.paremanent = True - if we want not to loose session even after browser exit
        user = request.form["nm"]
        session["user"] = user
        

        #check if user exists
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session['email'] = found_user.email
        else:
        #if user does not exist, create it
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("You are already logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None 
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            #guess it is for upd email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

#remove user data from session - from dictionary with this info
#we should activate this chapter by button to logout
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been loged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    
    return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/news")
def news():
    return render_template("news.html", newsposts=newsposts)

@app.route("/news/<newsname>")
def newpost(newsname):
    return render_template("newpost.html", newsposts=newsposts, newsname=newsname)


@app.route("/events")
def events():
    return render_template("events.html", newevents=newevents)

@app.route("/events/<eventname>")
def event(eventname):
    return render_template("event.html", newevents=newevents, eventname=eventname)

@app.route("/partners")
def partners():
    return render_template("partners.html")

@app.route("/volunteers")
def volunteers():
    return render_template("volunteers.html")


if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



#Successfully installed SQLAlchemy-1.4.45 flask-sqlalchemy-3.0.2 greenlet-2.0.1