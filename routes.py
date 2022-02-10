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

    profile_text = profiles.get_profile_text(users.user_id())
    print(profile_text)

    job_experience = profiles.get_job_experience(users.user_id())
    print(job_experience)

    education = profiles.get_education(users.user_id())
    print(education)

    #nyt on haettu profiiliteksti, työkokemus ja koulutus
        #jos ei ole näitä, näytetään vaihtoehdot lisää
        #jos on, näytetään nämä profiilissa
        #pitäisi siis antaa parametrina profile.html tiedostolle

    #kun tämä on tehty, siirry profiilitekstin lisäämiseen
    #siinä seuraavat vaiheet
    #luo html pohja uuden profiilitekstin lisäämiselle
    #tallenna kirjoitus profile_texts -tauluun
    #jos käyttäjällä on jo teksti, hae valmis teksti
    #muokkaa tekstiä

    #luo eka pohja profiilille html:lla

    if request.method == "GET":
        return render_template("profile.html", profile_text=profile_text, job_experience=job_experience, education=education)


@app.route("/edit_profile", methods = ["GET", "POST"])
def edit_profile():
    """creates a route for editing ones profile
    find the editing html and return it
    when a new profile text is created, call functions add_profile_text and possibly delete_profile_text in profiles.py"""

    #TODO profiilitekstin oikeellisuuden käsittely

    profile_text = profiles.get_profile_text(users.user_id())

    if request.method == "GET":
        return render_template("profile_text.html", profile_text=profile_text)
    
    if request.method == "POST":
        profile_text = request.form["profile_text"]
        if profiles.add_profile_text(users.user_id(), profile_text):
            return redirect("/profile")
        else:
            print("profiilitekstin päivittäminen epäonnistui")
            #tähän vielä error.html käsittely

@app.route("/add_job_experience", methods = ["GET", "POST"])
def add_job_experience():
    if request.method == "GET":
        return render_template("add_job_experience.html")
    
    if request.method == "POST":

        employer = request.form["employer"]
        role = request.form["role"]
        description = request.form["description"]
        beginning = request.form["beginning"]
        ended = request.form["ended"]
        profiles.add_job(users.user_id(), employer, role, description, beginning, ended)

        return redirect("/profile")

@app.route("/edit_job_experience", methods = ["GET", "POST"])
def edit_job_experience():
    """finds the html for editing a job experience and returns it
    calls for functions add_job_experience and delete_job_experience in profiles.py
    when editing a job experience, return the html file with the existing job experience
    then insert the new information and delete the old one"""
    pass

@app.route("/edit_education", methods = ["GET", "POST"])
def edit_education():
    """finds the html for editing education and returns in
    calls for function add_education and delete_education in profiles.py"""
    pass