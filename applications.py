#uutta työtä lisättäessä lisätään kyseiselle työlle hakulomake
    #voiko selata vanhoja lomakkeita?
    #

#hakemuksen muokkaaminen seuraavasti:
    #ensin lähetetään uusi hakemus
    #jos onnistuu, poista vanha
    #jos ei onnistu, anna virheviesti

#tarjoa myös mahdollisuus poista hakemus suoraan

#hakemuksella status 0: paikka avoin
#hakemuksella status 1: paikka suljettu, hakijaa ei valittu
#hakemuksella status 2: paikka suljettu, hakija valittu paikkaan

from db import db

def send_application(user_id, job_id, form_id, answer_1, answer_2, answer_3, answer_4, answer_5):
    """sends an application to a given job"""
    try:
        sql = """INSERT INTO applications (user_id, job_id, form_id, answer_1, answer_2, answer_3,
        answer_4, answer_5, sent_at, status) VALUES (:user_id, :job_id, :form_id, :answer_1,
        :answer_2, :answer_3, :answer_4, :answer_5, NOW(), 0)"""
        db.session.execute(sql, {"user_id":user_id, "job_id":job_id, "form_id":form_id,
        "answer_1": answer_1, "answer_2":answer_2, "answer_3":answer_3, "answer_4":answer_4, "answer_5":answer_5})
        db.session.commit()
        return True
    except:
        return False

def delete_application(user_id, application_id):
    """deletes a sent application if the job is still open"""
    pass

def get_application_status(application_id, user_id):
    """returns the status of an application if
    the application is sent by the user"""
    #pitäiskö tän olla jobs.py -tiedostossa mieluummin?
    pass

def applied_or_not(user_id, job_id):
    """tells whether the user has applied for the given job or not"""
    sql = """SELECT id FROM applications where user_id=:user_id AND job_id=:job_id"""
    id = db.session.execute(sql, {"user_id":user_id, "job_id":job_id}).fetchone()
    if not id:
        return False
    return True

def own_applications(user_id, status):
    """returns all jobs a given user has applied for and that has a given status"""
    #TODO hakee vaan uusimman hakemuksen per työpaikka
    sql = """SELECT j.role, u.name, a.status, a.id from jobs j, users u, applications a
    WHERE j.employer_id = u.id AND a.job_id = j.id and a.user_id =:user_id and a.status =:status"""
    return db.session.execute(sql, {"user_id":user_id, "status":status}).fetchall()

def show_application(id):
    sql = """SELECT j.role, j.id as job_id, u.name, af.question_1, af.question_2, af.question_3, af.question_4,
    af.question_5, a.answer_1, a.answer_2, a.answer_3, a.answer_4, a.answer_5, a.id as application_id FROM applications a, application_forms af, jobs j, users u
    where j.id = a.job_id and a.form_id = af.id and a.id=:id and u.id = a.user_id"""
    return db.session.execute(sql, {"id":id}).fetchone()

def get_all_applicants(job_id):
    sql = """select u.name, u.id as applicant_id, a.id as application_id from applications a, users u where a.job_id =:job_id and
    a.user_id = u.id"""
    return db.session.execute(sql, {"job_id":job_id}).fetchall()

def select_applicant(application_id):
    """changes the application status to 1 for the selected applicant and to 0 for all other applicants, changes the job status to 0 (job not open)"""
    #päivitä kyseisen hakemuksen status saaduksi
    sql = """UPDATE applications SET status = 1 WHERE id =:application_id"""
    db.session.execute(sql, {"application_id":application_id})
    db.session.commit()
    
def show_application_form(form_id):
    """shows the application form with the given form id"""
    sql = """SELECT question_1, question_2, question_3, question_4, question_5, j.role FROM application_forms a, jobs j WHERE a.id=:form_id and j.form = a.id"""
    return db.session.execute(sql, {"form_id":form_id}).fetchone()