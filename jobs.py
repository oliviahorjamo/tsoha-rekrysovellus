from db import db
from users import user_id
from users import user_role

def get_my_jobs(user_id, application_status, job_status):
    """returns all the jobs the user has created if an employer,
    returns all the jobs the user has applied for if an employee with a given application status and a given job status"""
    if user_role() == 0:
        sql = """SELECT j.role, j.description, j. beginning, j. ends, j.closing, u.name, a.status, a.id from jobs j, users u, applications a
        WHERE j.employer_id = u.id AND a.job_id = j.id and a.user_id =:user_id and a.status =:application_status and j.status =:job_status and j.visible = 1"""
        return db.session.execute(sql, {"user_id":user_id, "application_status":application_status, "job_status":job_status}).fetchall()
    if user_role() == 1:
        if job_status == 1:
            sql = """SELECT j.role, j.id, j.description, j.form, count(a.id) from jobs j left join applications a on a.job_id=j.id
            where j.employer_id =:user_id and j.status =:job_status and j.visible = 1 group by j.id"""
            return db.session.execute(sql, {"user_id": user_id, "job_status":job_status}).fetchall()
        elif job_status == 0:
            #returns the chosen applicant for the given job if one has been chosen, hence the subqueries
            
            subquery1 = "(select a.id from jobs j left join applications a on a.job_id = j.id where a.id is not null and a.status = 1)"
            subquery2 = "select u.name from users u, applications a2 where u.id = a2.id and a.id = a2.id"

            sql = """select j.id as job_id, j.role, j.description, a.id, case when a.id in (select a.id from jobs j left join applications a on a.job_id = j.id where a.id is not null and a.status = 1) 
            then (select u.name from users u, applications a2 where u.id = a2.user_id and a.id = a2.id) else 'Ei valittua hakijaa' end as applicant_name from jobs j
            left join applications a on j.id = a.job_id where j.employer_id =:user_id and j.status =:job_status"""

            return db.session.execute(sql, {"user_id":user_id, "job_status":job_status}).fetchall()

def get_open_jobs_employer():
    """returns all the jobs for the employee (in the main page)"""
    sql = """SELECT u.name as employer_name, u.id as employer_id, j.id, j.role, j.description, j.beginning, j.ends, j.opened, j.closing FROM USERS u, JOBS j WHERE
    u.id = j.employer_id AND j.visible = 1 AND j.status = 1"""
    return db.session.execute(sql).fetchall()

def get_open_jobs_employee(employee_id):
    """returns all the jobs the employee has not applied for"""
    sql = """SELECT u.name as employer_name, u.id as employer_id, j.id, j.role, j.description, j.beginning, j.ends, j.opened, j.closing FROM USERS u, JOBS j WHERE 
    u.id = j.employer_id AND j.visible = 1 AND j.status = 1 AND j.id NOT IN (SELECT job_id FROM applications WHERE applications.user_id =:employee_id)"""
    return db.session.execute(sql, {"employee_id":employee_id}).fetchall()

def get_job_info(job_id):
    """returns the info of a certain job and info on whether the user has applied for the job"""
    sql = """SELECT j.id, j.opened, j.closing, j.role, j.description,
    j.beginning, j.ends, j.form, e.name, af.question_1, af.question_2, af.question_3, af.question_4,
    af.question_5 FROM JOBS j, users e, application_forms af WHERE j.employer_id = 
    e.id and j.form = af.id and j.id =:job_id"""
    return db.session.execute(sql, {"job_id":job_id}).fetchone()

def add_job_1(employer_id, role, description, beginning, ends, closing):
    """"adds a new job to apply for (only for employers"""
    try:
        sql = """INSERT into JOBS (employer_id, role, description, beginning, ends, opened, closing, status, visible, form) VALUES (:employer_id, 
        :role, :description, :beginning, :ends, CAST(GET_DATE() AS date), :closing, 1, 1, NULL) RETURNING id"""
        job_id = db.session.execute(sql, {"employer_id":employer_id, "role":role, 
        "description":description, "beginning":beginning, "ends":ends, "closing":closing}).fetchone()[0]
        db.session.commit()
        return job_id
    except:
        return False

def add_job(employer_id, role, description, beginning, ends, closing):
    """"adds a new job to apply for (only for employers"""
    sql = """INSERT into JOBS (employer_id, role, description, beginning, ends, opened, closing, status, visible, form) VALUES (:employer_id, 
    :role, :description, :beginning, :ends, NOW(), :closing, 1, 1, NULL) RETURNING id"""
    job_id = db.session.execute(sql, {"employer_id":employer_id, "role":role, 
    "description":description, "beginning":beginning, "ends":ends, "closing":closing}).fetchone()[0]
    db.session.commit()
    return job_id

def delete_job(user_id, job_id):
    """removes a job (only available for the one who added the job"""
    try:
        sql = """UPDATE JOBS SET visible = 0 WHERE id=:job_id AND employer_id=:user_id"""
        db.session.execute(sql, {"job_id":job_id, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def add_application_form(job_id, question_1, question_2, question_3, question_4, question_5):
    try: 
        sql = """INSERT into APPLICATION_FORMS (question_1, question_2, question_3, question_4, question_5) VALUES (:question_1, 
        :question_2, :question_3, :question_4, :question_5) RETURNING id"""

        form_id = db.session.execute(sql, {"question_1":question_1, "question_2": question_2, "question_3": question_3, 
        "question_4": question_4, "question_5": question_5}).fetchone()[0]
        
        db.session.commit()

        sql = """UPDATE JOBS SET form =:form_id WHERE id=:job_id"""
        db.session.execute(sql, {"form_id":form_id,"job_id":job_id})
        db.session.commit()
        return True
    except:
        return False

def get_application_form(job_id):
    sql = """SELECT a.id, question_1, question_2, question_3, question_4, question_5 
    from application_forms a, jobs j where j.form = a.id and j.id=:job_id"""
    return db.session.execute(sql, {"job_id":job_id}).fetchone()

def get_job_role(job_id):
    sql = "select role from jobs where id =:job_id"
    return db.session.execute(sql, {"job_id":job_id}).fetchone()[0]

def close_job(job_id):
    sql = """UPDATE jobs SET status = 0 where id =:job_id"""
    db.session.execute(sql, {"job_id":job_id})
    db.session.commit()

def close_multiple_jobs(job_id_list):
    sql = """UPDATE jobs SET status = 0 where id in :job_id_list"""
    db.session.execute(sql, {"job_id_list":job_id_list})
    db.session.commit()

def get_job_id(application_id):
    """returns the job id related to a specific application id"""
    sql = """SELECT job_id from applications where id =:application_id"""
    return db.session.execute(sql, {"application_id":application_id}).fetchone()[0]

def find_jobs_to_close(date_today):
    """returns all jobs whose application period has ended and that are still open and visible"""
    sql = """SELECT id from JOBS WHERE closing < :date_today AND status = 1 AND visible = 1"""
    return db.session.execute(sql, {"date_today":date_today}).fetchall()

def count_applicants(job_id):
    """returns the number of applicants that have applied for a given job"""
    sql = """SELECT COUNT(id) FROM APPLICATIONS where job_id=:job_id"""
    return db.session.execute(sql, {"job_id":job_id})