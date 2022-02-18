from app import app
from flask import render_template, request, redirect
import users
import profiles
import jobs
import applications

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
    #tähän kohtaan työpaikkojen listaus
    #hae työpaikat jobs.py get_all_jobs funktiolle
    #sit anna lista parametrina
    open_jobs = jobs.get_open_jobs()
    return render_template("mainpage.html", open_jobs = open_jobs)

@app.route("/profile", methods = ["GET", "POST"])
def profile():

    profile_text = profiles.get_profile_text(users.user_id())

    job_experience = profiles.get_job_experience(users.user_id())

    education = profiles.get_education(users.user_id())

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

@app.route("/add_education", methods =["GET", "POST"])
def add_education():
    if request.method == "GET":
        return render_template("add_education.html")
    
    if request.method == "POST":

        school = request.form["school"]
        level = request.form["level"]
        description = request.form["description"]
        beginning = request.form["beginning"]
        graduation = request.form["graduation"]

        profiles.add_education(users.user_id(), school, level, description, beginning, graduation)

        return redirect("/profile")

@app.route("/edit_education", methods = ["GET", "POST"])
def edit_education():
    """finds the html for editing education and returns in
    calls for function add_education and delete_education in profiles.py"""
    pass

@app.route("/add_job", methods = ["GET", "POST"])
def add_job():
    users.require_role(1)

    if request.method == "GET":
        return render_template("add_job.html")

    if request.method == "POST":

        #TODO syötteen oikeellisuuden tarkistus ja virhemahdollisuuden käsittely

        role = request.form["role"]
        description = request.form["description"]
        beginning = request.form["beginning"]
        ends = request.form["ends"]
        application_period_closes = request.form["application_period_closes"]
        question_1 = request.form["question_1"]
        question_2 = request.form["question_2"]
        question_3 = request.form["question_3"]
        question_4 = request.form["question_4"]
        question_5 = request.form["question_5"]
        job_id = jobs.add_job(users.user_id(), role, description, beginning, ends, application_period_closes)
        
        #TODO syötteen oikeellisuuden tarkistus
        
        jobs.add_application_form(job_id, question_1, question_2, question_3, question_4, question_5)

        return redirect("/mainpage")

@app.route("/job_info/<int:job_id>", methods = ["GET"])
def show_job(job_id):

    info = jobs.get_job_info(job_id)

    print(info)

    applied = applications.applied_or_not(users.user_id(), job_id)

    if request.method == "GET":
        return render_template("show_job.html", info=info, applied = applied)

@app.route("/apply/<int:job_id>", methods = ["GET" ,"POST"])
def apply(job_id):

    #jobs funktiolla get_application_form etsitään kysymykset
    #kysymykset parametrina html:lle
    #post metodi lähettää hakemuksen

    application_form = jobs.get_application_form(job_id)
    form_id = application_form.id

    if request.method == "GET":
        return render_template("apply.html", application_form=application_form, job_id=job_id)

    if request.method == "POST":

        #MIKÄ IHME TÄSSÄ MENEE PIELEEN?

        answer_1 = request.form["answer_1"]
        answer_2 = request.form["answer_2"]
        answer_3 = request.form["answer_3"]
        answer_4 = request.form["answer_4"]
        answer_5 = request.form["answer_5"]

        applications.send_application(users.user_id(), job_id, form_id, answer_1, answer_2, answer_3, answer_4, answer_5)

    #TODO sivu muuttuisi sellaiseksi että näkyy lähetetty lomake ja sitä voisi muokata

        return redirect("/mainpage")

@app.route("/own_applications", methods = ["GET", "POST"])
def own_applications():
    #hae omat hakemukset
    #grouppaa statuksen mukaan?

    #applications.py tiedostoon funktio own_applications

    #listataan tässä kaikki työpaikat joita on jo hakenut tyyliin
    #rooli
    #työnantaja
    #työnhaun status
    #tarkastele hakemustasi tästä

    #paikkaa ei saatu
    not_elected = jobs.get_my_jobs(users.user_id(), application_status = 0, job_status = 0)

    #paikka saatu (tällöin job status automaattisesti 0)
    got_elected = jobs.get_my_jobs(users.user_id(), application_status = 1, job_status = 0)

    #haku vielä auki (tällöin application status automaattisesti 0)
    open_applications = jobs.get_my_jobs(users.user_id(), application_status = 0, job_status = 1)

    if request.method == "GET":
        return render_template("own_applications.html", open_applications=open_applications, got_elected=got_elected, not_elected = not_elected)

    print("open applications", open_applications)
    print("got_elected", got_elected)

@app.route("/application/<int:id>", methods = ["GET", "POST"])
def show_application(id):

    #näyttää kyseisellä id:llä olevan hakemuksen
    application = applications.show_application(id)

    print(application)

    #lähettää hakemuksen parametrina html:lle
    if request.method == "GET":
        return render_template("show_application.html", application=application, user_role = users.user_role())


@app.route("/own_jobs", methods = ["GET", "POST"])
def own_jobs():
    #hakee tietyn työnantajan työpaikat statuksen mukaan parametrina html:lle

    open_jobs = jobs.get_my_jobs(users.user_id(), None, 1)
    print(open_jobs)

    #päättyneet haut
    application_period_ended = jobs.get_my_jobs(users.user_id(), None, 0)

    if request.method == "GET":
        return render_template("my_jobs.html", open_jobs = open_jobs, application_period_ended = application_period_ended)


@app.route("/all_applicants/<int:job_id>", methods = ["GET", "POST"])
def all_applications(job_id):
    #hakee tietyn työpaikan kaikki hakemukset parametriksi html:lle
    #post tarjoaa mahdollisuuden valita tietty työtekijä paikkaan ja ilmoittaa
    #muille että haku on päättynyt

    all_applicants = applications.get_all_applicants(job_id)
    job_role = jobs.get_job_role(job_id)

    if request.method == "GET":
        return render_template("all_applicants.html", all_applicants=all_applicants, job_role = job_role, job_id=job_id)

@app.route("/select_applicant/<int:application_id>", methods = ["GET", "POST"])
def select_applicant(application_id):

    users.require_role(1)
    #kutsu applications.py moduulista funktiota tietyn työntekijän valitsemiseen paikkaan

    applications.select_applicant(application_id)

    job_id = jobs.get_job_id(application_id)

    jobs.close_job(job_id)

    return redirect("/own_jobs")