#uutta työtä lisättäessä lisätään kyseiselle työlle hakulomake
    #voiko selata vanhoja lomakkeita?
    #

#hakemuksen muokkaaminen seuraavasti:
    #ensin lähetetään uusi hakemus
    #jos onnistuu, poista vanha
    #jos ei onnistu, anna virheviesti

#tarjoa myös mahdollisuus poista hakemus suoraan

from db import db

def get_all_application_forms():
    """returns all application forms"""
    pass

def add_application_form(question1, question2, question3, question4, question5, job_id):
    """adds a new application form into application_form -table,
    adds a reference to the application form into the jobs -table"""
    pass

def get_application_form(job_id):
    """returns the application form of a given job"""
    pass

def send_application(user_id, job_id, form_id, answer_1, answer_2, answer_3, answer_4, answer_5):
    """sends an application to a given job"""
    sql = """INSERT INTO applications (user_id, job_id, form_id, answer_1, answer_2, answer_3,
    answer_4, answer_5, sent_at, status) VALUES (:user_id, :job_id, :form_id, :answer_1,
    :answer_2, :answer_3, :answer_4, :answer_5, NOW(), 0)"""
    db.session.execute(sql, {"user_id":user_id, "job_id":job_id, "form_id":form_id,
    "answer_1": answer_1, "answer_2":answer_2, "answer_3":answer_3, "answer_4":answer_4, "answer_5":answer_5})
    db.session.commit()

def delete_application(user_id, application_id):
    """deletes a sent application if the job is still open"""
    pass

def get_all_applications(job_id):
    """lists all applications into a job if the user has
    added the job"""
    sql = """select a.id, j.role, u.name, f.question_1, f.question_2, f.question_3, f.question_4,
    f.question_5, a.answer_1, a.answer_2, a.answer_3, a.answer_4, a.answer_5,
    a.sent_at from applications a, users u, application_forms f, jobs j where a.job_id =:job_id and
    j.id =:job_id and a.form_id = f.id and a.user_id = u.id"""
    return db.session.execute(sql, {"job_id":job_id}).fetchall()

def get_application_status(application_id, user_id):
    """returns the status of an application if
    the application is sent by the user"""
    #pitäiskö tän olla jobs.py -tiedostossa mieluummin?
    pass

def own_applications(user_id, status):
    """returns all jobs a given user has applied for and that has a given status"""
    #TODO hakee vaan uusimman hakemuksen per työpaikka
    sql = """SELECT j.role, u.name, a.status, a.id from jobs j, users u, applications a
    WHERE j.employer_id = u.id AND a.job_id = j.id and a.user_id =:user_id and a.status =:status"""
    return db.session.execute(sql, {"user_id":user_id, "status":status}).fetchall()

def show_application(id):
    sql = """SELECT j.role, u.name, af.question_1, af.question_2, af.question_3, af.question_4,
    af.question_5, a.answer_1, a.answer_2, a.answer_3, a.answer_4, a.answer_5 FROM applications a, application_forms af, jobs j, users u
    where j.id = a.job_id and a.form_id = af.id and a.id=:id and u.id = a.user_id"""
    return db.session.execute(sql, {"id":id}).fetchone()

def get_all_applicants(job_id):
    sql = """select u.name, a.id from applications a, users u where a.job_id =:job_id and
    a.user_id = u.id"""
    return db.session.execute(sql, {"job_id":job_id}).fetchall()