from datetime import date
from app import app
from flask import render_template, request, redirect
import users
import profiles
import jobs
import applications

@app.route("/")
def index():

    jobs_to_close = jobs.find_jobs_to_close(date.today())

    for job in jobs_to_close:
        jobs.close_job(job[0])

    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():

    #showing the registration form
    if request.method == "GET":
        return render_template("register.html")

    #creating an account after receiving the registration form
    if request.method == "POST":
        username = request.form["username"]

        if not 0 < len(username) <16:
            return render_template("error.html", message = "Käyttäjänimessä tulee olla 1-15 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message = "Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message = "Salasana on tyhjä")

        role = request.form["role"]

        #call for function register in users.py to handle the registration
        if not users.register(username, password1, role):
            return render_template("error.html", message="Rekisteröinti epäonnistui")

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

    job_experience = profiles.get_all_job_experience(users.user_id())

    education = profiles.get_all_education(users.user_id())

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
        return render_template("pown_rofile.html", profile_text=profile_text, job_experience=job_experience, education=education)


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

        if len(profile_text) > 5000:
            return render_template("error.html", message = "Profiiliteksti on liian pitkä")

        if profiles.add_profile_text(users.user_id(), profile_text):
            return redirect("/profile")
        else:
            return render_template("error.html", message="Profiilitekstin päivittäminen epäonnistui")

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

        if len(employer) > 50:
            return render_template("error.html", message = "Työnantajan nimi voi olla max. 50 merkkiä")

        if len(role) > 50:
            return render_template("error.html", message = "Rooli voi olla max. 50 merkkiä")

        if len(employer) > 500:
            return render_template("error.html", message = "Työpaikan kuvaus voi olla max. 500 merkkiä")

        if profiles.add_job_experience(users.user_id(), employer, role, description, beginning, ended):
            return redirect("/profile")
        else:
            return render_template("error.html", message = "Työkokemuksen päivittäminen epäonnistui")

@app.route("/edit_job_experience/<int:experience_id>", methods = ["GET", "POST"])
def edit_job_experience(experience_id):
    """finds the html for editing a job experience and returns it
    calls for functions add_job_experience and delete_job_experience in profiles.py
    when editing a job experience, return the html file with the existing job experience
    then insert the new information and delete the old one"""

    job = profiles.get_job_experience(experience_id)

    if request.method == "GET":
        return render_template("edit_experience.html", job=job)
    
    if request.method == "POST":

        employer = request.form["employer"]
        role = request.form["role"]
        description = request.form["description"]
        beginning = request.form["beginning"]
        ended = request.form["ended"]

        if len(employer) > 50:
            return render_template("error.html", message = "Työnantajan nimi voi olla max. 50 merkkiä")

        if len(role) > 50:
            return render_template("error.html", message = "Rooli voi olla max. 50 merkkiä")

        if len(employer) > 500:
            return render_template("error.html", message = "Työpaikan kuvaus voi olla max. 500 merkkiä")

        if profiles.add_job_experience(users.user_id(), employer, role, description, beginning, ended):
            if profiles.delete_job_experience(experience_id):
                return redirect("/profile")
            else:
                return render_template("error.html", message = "Vanhan työkokemuksen poistaminen epäonnistui")
        else:
            return render_template("error.html", message = "Työkokemuksen päivittäminen epäonnistui")


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

        if len(school) > 50:
            return render_template("error.html", message = "Koulun nimi voi olla max. 50 merkkiä")

        if len(level) > 50:
            return render_template("error.html", message = "Koulutuksen tason pituus voi olla max. 50 merkkiä")

        if len(description) > 500:
            return render_template("error.html", message = "Koulutuksen kuvaus voi olla max. 500 merkkiä")

        if profiles.add_education(users.user_id(), school, level, description, beginning, graduation):
            return redirect("/profile")
        else:
            return False

@app.route("/edit_education/<int:id>", methods = ["GET", "POST"])
def edit_education(id):
    """finds the html for editing education and returns in
    calls for function add_education and delete_education in profiles.py"""
    
    education = profiles.get_education(id)

    if request.method == "GET":
        return render_template("edit_education.html", education=education)
    
    if request.method == "POST":

        school = request.form["school"]
        level = request.form["level"]
        description = request.form["description"]
        beginning = request.form["beginning"]
        graduation = request.form["graduation"]

        if len(school) > 50:
            return render_template("error.html", message = "Koulun nimi voi olla max. 50 merkkiä")

        if len(level) > 50:
            return render_template("error.html", message = "Koulutuksen taso voi olla max. 50 merkkiä")

        if len(description) > 500:
            return render_template("error.html", message = "Koulutuksen kuvaus voi olla max. 500 merkkiä")

        if profiles.add_education(users.user_id(), school, level, description, beginning, graduation):
            if profiles.delete_education(id):
                return redirect("/profile")
            else:
                return render_template("error.html", message = "Vanhan koulutuksen poistaminen epäonnistui")
        else:
            return render_template("error.html", message = "Koulutuksen päivittäminen epäonnistui")

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


        if len(role) > 50:
            return render_template("error.html", message = "Rooli voi olla max. 50 merkkiä")

        if len(description) > 500:
            return render_template("error.html", message = "Työpaikan kuvaus voi olla max. 500 merkkiä")     

        if len(question_1) > 100 or len(question_2) > 100 or len(question_3) > 100 or len(question_4) > 100 or len(question_5) > 100:
            return render_template("error.html", message = "Kysymyksen pituus voi olla max. 100 merkkiä") 

        if question_1 == "" and question_2 == "" and question_3 == "" and question_4 == "" and question_5 == "":
            return render_template("error.html", message = "Lomakkeeseen on lisättävä ainakin yksi kysymys.")

        job_id = jobs.add_job(users.user_id(), role, description, beginning, ends, application_period_closes)
        
        if job_id == False:
            return render_template("error.html", message = "Työpaikkailmoituksen lisääminen epäonnistui")
        
        if jobs.add_application_form(job_id, question_1, question_2, question_3, question_4, question_5):
            return redirect("/mainpage")
        else:
            return render_template("error.html", message = "Työpaikkailmoituksen kysymysten lisääminen epäonnistui")

@app.route("/job_info/<int:job_id>", methods = ["GET"])
def show_job(job_id):

    info = jobs.get_job_info(job_id)
    applied = applications.applied_or_not(users.user_id(), job_id)

    if request.method == "GET":
        return render_template("show_job.html", info=info, applied = applied)

@app.route("/apply/<int:job_id>", methods = ["GET" ,"POST"])
def apply(job_id):

    users.require_role(0)
    application_form = jobs.get_application_form(job_id)
    form_id = application_form.id

    if request.method == "GET":
        return render_template("apply.html", application_form=application_form, job_id=job_id)

    if request.method == "POST":

        answer_1 = request.form["answer_1"]
        answer_2 = request.form["answer_2"]
        answer_3 = request.form["answer_3"]
        answer_4 = request.form["answer_4"]
        answer_5 = request.form["answer_5"]


        if len(answer_1) > 500 or len(answer_2) > 500 or len(answer_3) > 500 or len(answer_4) > 500 or len(answer_5) > 500:
            return render_template("error.html", message = "Vastauksen pituus voi olla max. 500 merkkiä")

        if applications.send_application(users.user_id(), job_id, form_id, answer_1, answer_2, answer_3, answer_4, answer_5):

        #TODO sivu muuttuisi sellaiseksi että näkyy lähetetty lomake ja sitä voisi muokata?
            return redirect("/mainpage")
        else:
            return render_template("error.html", message = "Hakemuksen lähettäminen epäonnistui")

@app.route("/own_applications", methods = ["GET", "POST"])
def own_applications():

    users.require_role(0)
    not_elected = jobs.get_my_jobs(users.user_id(), application_status = 0, job_status = 0)

    #paikka saatu (tällöin job status automaattisesti 0)
    got_elected = jobs.get_my_jobs(users.user_id(), application_status = 1, job_status = 0)

    #haku vielä auki (tällöin application status automaattisesti 0)
    open_applications = jobs.get_my_jobs(users.user_id(), application_status = 0, job_status = 1)

    if request.method == "GET":
        return render_template("own_applications.html", open_applications=open_applications, got_elected=got_elected, not_elected = not_elected,
        count_open_applications = len(open_applications), count_got_elected = len(got_elected), count_not_elected = len(not_elected))

@app.route("/application/<int:id>", methods = ["GET", "POST"])
def show_application(id):

    application = applications.show_application(id)

    if request.method == "GET":
        return render_template("show_application.html", application=application, user_role = users.user_role())


@app.route("/own_jobs", methods = ["GET", "POST"])
def own_jobs():
    """returns the job advertisements of a given employer"""

    users.require_role(1)
    open_jobs = jobs.get_my_jobs(users.user_id(), None, 1)
    application_period_ended = jobs.get_my_jobs(users.user_id(), None, 0)

    if request.method == "GET":
        return render_template("my_jobs.html", open_jobs = open_jobs, application_period_ended = application_period_ended)


@app.route("/all_applicants/<int:job_id>", methods = ["GET", "POST"])
def all_applications(job_id):
    
    users.require_role(1)

    all_applicants = applications.get_all_applicants(job_id)

    job_role = jobs.get_job_role(job_id)

    if request.method == "GET":
        return render_template("all_applicants.html", all_applicants=all_applicants, job_role = job_role, job_id=job_id)

@app.route("/select_applicant/<int:application_id>", methods = ["GET", "POST"])
def select_applicant(application_id):

    users.require_role(1)

    applications.select_applicant(application_id)

    job_id = jobs.get_job_id(application_id)

    jobs.close_job(job_id)

    return redirect("/own_jobs")

@app.route("/delete_job_experience/<int:id>", methods = ["GET", "POST"])
def delete_job_experience(id):

    if profiles.delete_job_experience(id):
        return redirect("/profile")
    else:
        return render_template("error.html", message = "Työkokemuksen poistaminen epäonnistui")

@app.route("/delete_education/<int:education_id>", methods = ["GET", "POST"])
def delete_education(education_id):

    if profiles.delete_education(education_id):
        return redirect("/profile")
    else:
        return render_template("error.html", message = "Koulutuksen poistaminen epäonnistui")

@app.route("/delete_job/<int:job_id>", methods = ["GET", "POST"])
def delete_job(job_id):

    users.require_role(1)

    if jobs.delete_job(users.user_id(), job_id):
        return redirect("/own_jobs")
    else:
        return render_template("error.html", message = "Työpaikan poistaminen epäonnistui")

@app.route("/application_form/<int:form_id>", methods = ["GET", "POST"])
def show_application_form(form_id):

    form = applications.show_application_form(form_id)

    if request.method == "GET":
        return render_template("show_form.html", form = form)

@app.route("/show_profile/<int:applicant_id>/<int:job_id>", methods = ["GET", "POST"])
def show_profile(applicant_id, job_id):
    """shows the profile of the applicant with the given username"""

    name = users.get_name(applicant_id)

    profile_text = profiles.get_profile_text(applicant_id)

    job_experience = profiles.get_all_job_experience(applicant_id)

    education = profiles.get_all_education(applicant_id)

    if request.method == "GET":
        return render_template("show_profile.html", name = name, profile_text = profile_text, job_experience = job_experience, education = education, job_id = job_id)
