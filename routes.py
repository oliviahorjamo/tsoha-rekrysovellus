from app import app
from flask import render_template, request, redirect
import users

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

