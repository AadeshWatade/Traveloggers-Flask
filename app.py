from flask import Flask, render_template, url_for, request, redirect, flash, session, jsonify
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
import random
import datetime
from uuid import uuid4
from flask import request
import requests


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/traveloggers"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


# @app.route("/")
# def helo():
#     return render_template("index.html")


@app.route("/")
def index():
    if 'fullName' in session:
        fullName = session['fullName']
        print(fullName)
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        Full_Name = request.form['Full_name']
        Email = request.form['Email']
        Password = request.form['Password']
        Confirm_password = request.form['Confirm_password']
        City = request.form['City']
        State = request.form['State']
        author_id = random.randint(11111, 99999)
        

        if Password == Confirm_password:
            pw_hash = bcrypt.generate_password_hash(Password).decode('utf-8')
            user_id = users.insert_one(
            {'email': email, 'password': password}).inserted_id
            session['user_id'] = str(user_id)
            mongo.db.users.insert_one(
                {
                    "author_id": author_id,
                    "fullName": Full_Name,
                    "email": Email,
                    "password": pw_hash,
                    "city": City,
                    "state": State

                }
            )
            flash("Account created Successfully", "success")
            return redirect(url_for('login'))
        else:
            flash('Password and confirm password are not same', 'danger')
    return render_template("signup.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        Email = request.form["Email"]
        Password = request.form["Password"]
        found_user = mongo.db.users.find_one({"email": Email})
        if found_user:
            if bcrypt.check_password_hash(found_user['password'], request.form['Password']):
                session['user_id'] = str(user['_id'])
                session['fullName'] = found_user['fullName']
                session['email'] = found_user['email']
                flash("Successful Login", "success")
                return redirect(url_for("index"))
            else:
                flash("Login failed. Please try again!", "danger")
        else:
            flash("User not found", "danger")
    return render_template("login.html")


@app.route("/add_blog", methods=['GET', 'POST'])
def add_blog():

    if request.method == "POST":
        location = request.form['location']
        date = request.form['date']
        content = request.form['blog']
        blog_id = random.randint(1111, 9999)

        mongo.db.blogs.insert_one({
            'content': content,
            'location': location,
            'blog_id': blog_id,
            'created_at': datetime.datetime.now(),
            'creater': {
                'name': session['fullName'],
                'email': session['email']
            }
        })

        flash("Blog added successfully", "success")
    return render_template("add_blog.html")



@app.route('/blogs')
def blogs():
    blogs = mongo.db.blogs.find()
    return render_template("view_blog.html", blogs=blogs)


@app.route("/view_blog/<int:blog_id>")
def view_blog(blog_id):
    blog = mongo.db.blogs.find_one({'blog_id': blog_id})
    return render_template("view_blog.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Successfuly logged out!", "success")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = "asdtc"
    app.run(debug=True)
