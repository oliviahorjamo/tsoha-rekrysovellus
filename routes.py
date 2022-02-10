from app import app
from flask import render_template, request, redirect
import users
import profiles

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():

    #showing the registration form
    if request.method == "GET":
        return render_template("register.html")

    #creating an account after receiving the registration form
    if request.method == "POST":
        username = request.form["username"]
        #TODO virheiden käsittely usernamen osalta

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        #TODO virheiden käsittely salasanojen osalta

        role = request.form["role"]

        #call for function register in users.py to handle the registration
        if not users.register(username, password1, role):
            #TODO virheiden käsittely rekisteröitymisen epäonnistumisen kannalta
            print("Rekisteröinti epäonnistui")

        return redirect("/mainpage")

@app.route("/login", methods =["GET","POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            #TODO virheiden käsittely
            print("Sisään kirjautuminen epäonnistui")

    return redirect("/mainpage")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/mainpage", methods = ["GET", "POST"])
def mainpage():
    return render_template("mainpage.html")

@app.route("/profile", methods = ["GET", "POST"])
def profile():

    #luo eka pohja profiilille html:lla

    if request.method == "GET":
        return render_template("profile.html")

    profile_text = profiles.get_profile_text(users.user_id(), users.user_role())

@app.route("/edit_profile", methods = ["GET", "POST"])
def edit_profile():
    """creates a route for editing ones profile
    find the editing html and return it
    when a new profile text is created, call functions add_profile_text and possibly delete_profile_text in profiles.py"""
    pass

@app.route("/edit_job_experience", methods = ["GET", "POST"])
def edit_job_experience():
    """finds the html for editing a job experience and returns it
    calls for functions add_job_experience and delete_job_experience in profiles.py
    when editing a job experience, return the html file with the existing job experience
    then insert the new information and delete the old one"""

@app.route("/edit_education", methods = ["GET", "POST"])
def edit_education():
    """finds the html for editing education and returns in
    calls for function add_education and delete_education in profiles.py"""