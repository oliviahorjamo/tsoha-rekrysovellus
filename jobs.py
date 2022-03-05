from db import db
from users import user_id
from users import user_role

def get_my_jobs(user_id, application_status, job_status):
    """returns all the jobs the user has created if an employer,
    returns all the jobs the user has applied for with a given application status and a given job status,
    if the user is an employee"""

    if user_role() == 0:
        sql = """SELECT j.role, j.description, j. beginning, j. ends, j.closing, u.name, a.status, a.id 
                FROM jobs j, users u, applications a
                WHERE j.employer_id = u.id AND a.job_id = j.id AND a.user_id =:user_id 
                AND a.status =:application_status and j.status =:job_status and j.visible = 1"""
        return db.session.execute(sql, {"user_id":user_id, "application_status":application_status, 
                                        "job_status":job_status}).fetchall()

    if user_role() == 1:

        if job_status == 1:
            sql = """SELECT j.role, j.id, j.description, j.form, COUNT(a.id)
                    FROM jobs j LEFT JOIN applications a ON a.job_id=j.id
                    WHERE j.employer_id =:user_id AND j.status =:job_status AND j.visible = 1 
                    GROUP BY j.id"""
            return db.session.execute(sql, {"user_id": user_id, "job_status":job_status}).fetchall()

        elif job_status == 0:
            sql = """SELECT j.id AS job_id, j.role, j.description, a.id, 
                    CASE WHEN a.id IN 
                    (SELECT a.id FROM jobs j LEFT JOIN applications a ON a.job_id = j.id 
                    WHERE a.id IS NOT NULL AND a.status = 1) 
                    THEN (SELECT u.name FROM users u, applications a2 WHERE u.id = a2.user_id AND a.id = a2.id) 
                    ELSE 'Ei valittua hakijaa' END 
                    AS applicant_name 
                    FROM jobs j LEFT JOIN applications a ON j.id = a.job_id 
                    WHERE j.employer_id =:user_id AND j.status =:job_status"""
            return db.session.execute(sql, {"user_id":user_id, "job_status":job_status}).fetchall()

def get_open_jobs_employer():
    """returns all the open jobs in the main page"""
    sql = """SELECT u.name AS employer_name, u.id AS employer_id, 
            j.id, j.role, j.description, j.beginning, j.ends, j.opened, j.closing 
            FROM users u, jobs j 
            WHERE u.id = j.employer_id AND j.visible = 1 AND j.status = 1"""
    return db.session.execute(sql).fetchall()

def get_open_jobs_employee(employee_id):
    """returns all the open jobs the employee has not applied for"""
    sql = """SELECT u.name AS employer_name, u.id AS employer_id, 
            j.id, j.role, j.description, j.beginning, j.ends, j.opened, j.closing 
            FROM users u, jobs j 
            WHERE u.id = j.employer_id AND j.visible = 1 AND j.status = 1 AND j.id NOT IN 
            (SELECT job_id FROM applications WHERE applications.user_id =:employee_id)"""
    return db.session.execute(sql, {"employee_id":employee_id}).fetchall()

def add_job(employer_id, role, description, beginning, ends, closing):
    """"adds a new job advertisement (only for employers)"""
    try:
        sql = """INSERT INTO jobs 
                (employer_id, role, description, beginning, ends, opened, closing, status, visible, form) 
                VALUES (:employer_id, :role, :description, :beginning, :ends, NOW(), :closing, 1, 1, NULL) 
                RETURNING id"""
        job_id = db.session.execute(sql, {"employer_id":employer_id, "role":role, 
                                        "description":description, "beginning":beginning, 
                                        "ends":ends, "closing":closing}).fetchone()[0]
        db.session.commit()
        return job_id
    except:
        return False

def delete_job(user_id, job_id):
    """removes a job (only available for the one who added the job)"""
    try:
        sql = """UPDATE jobs SET visible = 0 WHERE id=:job_id AND employer_id=:user_id"""
        db.session.execute(sql, {"job_id":job_id, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def add_application_form(job_id, question_1, question_2, question_3, question_4, question_5):
    """adds an application form for the given job with the given questions"""
    try: 
        sql = """INSERT into application_forms 
                (question_1, question_2, question_3, question_4, question_5) 
                VALUES (:question_1, :question_2, :question_3, :question_4, :question_5) 
                RETURNING id"""
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
    """returns the application form that belongs to the given job"""
    sql = """SELECT a.id, question_1, question_2, question_3, question_4, question_5 
                FROM application_forms a, jobs j WHERE j.form = a.id AND j.id=:job_id"""
    return db.session.execute(sql, {"job_id":job_id}).fetchone()

def get_job_role(job_id):
    sql = "SELECT role FROM jobs WHERE id =:job_id"
    return db.session.execute(sql, {"job_id":job_id}).fetchone()[0]

def close_job(job_id):
    """closes the jobs with the given id, used when an applicant is selected for the job"""
    sql = """UPDATE jobs SET status = 0 WHERE id =:job_id"""
    db.session.execute(sql, {"job_id":job_id})
    db.session.commit()

def close_old_jobs():
    sql = """UPDATE jobs SET status = 0 WHERE id IN
            (SELECT id from JOBS WHERE closing < NOW() AND status = 1 AND visible = 1)"""
    db.session.execute(sql)
    db.session.commit()

def get_job_id(application_id):
    """returns the job id related to a specific application id"""
    sql = """SELECT job_id FROM applications WHERE id =:application_id"""
    return db.session.execute(sql, {"application_id":application_id}).fetchone()[0]

def count_applicants(job_id):
    """returns the number of applicants that have applied for a given job"""
    sql = """SELECT COUNT(id) FROM applications WHERE job_id=:job_id"""
    return db.session.execute(sql, {"job_id":job_id})