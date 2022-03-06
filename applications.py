from db import db

def send_application(user_id, job_id, form_id, answer_1, answer_2, answer_3, answer_4, answer_5):
    """sends an application to a given job"""
    try:
        sql = """INSERT INTO applications 
                (user_id, job_id, form_id, answer_1, answer_2, answer_3,
                answer_4, answer_5, sent_at, status) 
                VALUES (:user_id, :job_id, :form_id, :answer_1, :answer_2, :answer_3,
                :answer_4, :answer_5, NOW(), 0)"""
        db.session.execute(sql, {"user_id":user_id, "job_id":job_id, "form_id":form_id,
                                "answer_1": answer_1, "answer_2":answer_2, "answer_3":answer_3, 
                                "answer_4":answer_4, "answer_5":answer_5})
        db.session.commit()
        return True
    except:
        return False

def show_application(id):
    sql = """SELECT j.role, j.id AS job_id, u.name, af.question_1, af.question_2, af.question_3, af.question_4,
            af.question_5, a.answer_1, a.answer_2, a.answer_3, a.answer_4, a.answer_5, a.id AS application_id 
            FROM applications a, application_forms af, jobs j, users u
            WHERE j.id = a.job_id and a.form_id = af.id and a.id=:id and u.id = a.user_id"""
    return db.session.execute(sql, {"id":id}).fetchone()

def get_all_applicants(job_id):
    sql = """SELECT u.name, u.id AS applicant_id, a.id AS application_id 
    FROM applications a, users u 
    WHERE a.job_id =:job_id AND a.user_id = u.id"""
    return db.session.execute(sql, {"job_id":job_id}).fetchall()

def select_applicant(application_id):
    """changes the application status to 1 for the selected applicant"""
    sql = """UPDATE applications SET status = 1 WHERE id =:application_id"""
    db.session.execute(sql, {"application_id":application_id})
    db.session.commit()
    
def show_application_form(form_id):
    """shows the application form with the given form id"""
    sql = """SELECT question_1, question_2, question_3, question_4, question_5, j.role 
            FROM application_forms a, jobs j 
            WHERE a.id=:form_id and j.form = a.id"""
    return db.session.execute(sql, {"form_id":form_id}).fetchone()