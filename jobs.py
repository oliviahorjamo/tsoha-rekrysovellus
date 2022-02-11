from db import db

def get_my_jobs(user_id):
    """returns all the jobs the user has created if an employer,
    return all the jobs the user has applied for if an employee"""
    pass

def get_all_jobs():
    """returns all the jobs (in the main page)"""
    pass

def get_job_info(job_id):
    """returns the info of a certain job"""
    pass

def add_job(employer_id, role, description, beginning, ends, closing):
    """"adds a new job to apply for (only for employers"""
    #
    
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