from db import db
from users import user_id

def get_my_jobs(user_id):
    """returns all the jobs the user has created if an employer,
    return all the jobs the user has applied for if an employee"""
    pass

def get_open_jobs():
    """returns all the jobs (in the main page)"""
    sql = """SELECT u.name, j.id, j.role, j.description FROM USERS u, JOBS j WHERE
    u.id = j.employer_id AND visible = 1 AND status = 0"""
    return db.session.execute(sql).fetchall()

def get_job_info(job_id, user_id):
    """returns the info of a certain job and info on whether the user has applied for the job"""
    sql = """SELECT j.id, j.opened, j.closing, j.role, j.description,
    j.beginning, j.ends, j.form, e.name, af.question_1, af.question_2, af.question_3, af.question_4,
    af.question_5, a.id FROM JOBS j left join applications a on a.job_id = j.id, users e, application_forms af WHERE j.employer_id = 
    e.id and j.form = af.id and j.id =:job_id and a.user_id =:user_id"""
    return db.session.execute(sql, {"job_id":job_id, "user_id":user_id}).fetchone()

def add_job(employer_id, role, description, beginning, ends, closing):
    """"adds a new job to apply for (only for employers"""
    sql = """INSERT into JOBS (employer_id, role, description, beginning, ends, opened, closing, status, visible, form) VALUES (:employer_id, 
    :role, :description, :beginning, :ends, NOW(), :closing, 0, 1, NULL) RETURNING id"""
    job_id = db.session.execute(sql, {"employer_id":employer_id, "role":role, 
    "description":description, "beginning":beginning, "ends":ends, "closing":closing}).fetchone()[0]
    db.session.commit()

    return job_id

def delete_job(user_id, user_role, job_id):
    """removes a job (only available for the one who added the job"""
    pass

def add_application_form(job_id, question_1, question_2, question_3, question_4, question_5):
    sql = """INSERT into APPLICATION_FORMS (question_1, question_2, question_3, question_4, question_5) VALUES (:question_1, 
    :question_2, :question_3, :question_4, :question_5) RETURNING id"""

    print("sql kuselu", sql)
    form_id = db.session.execute(sql, {"question_1":question_1, "question_2": question_2, "question_3": question_3, 
    "question_4": question_4, "question_5": question_5}).fetchone()[0]

    print("form_id", form_id)
    db.session.commit()

    sql = """UPDATE JOBS SET form =:form_id WHERE id=:job_id"""
    db.session.execute(sql, {"form_id":form_id,"job_id":job_id})
    db.session.commit()

def get_application_form(job_id):
    sql = """SELECT a.id, question_1, question_2, question_3, question_4, question_5 
    from application_forms a, jobs j where j.form = a.id and j.id=:job_id"""
    return db.session.execute(sql, {"job_id":job_id}).fetchone()