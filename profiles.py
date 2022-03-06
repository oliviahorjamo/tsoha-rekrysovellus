
from db import db

def add_profile_text(user_id, text):
    """adds profile text to the profile (both employees and employers)"""
    try:
        sql = "INSERT into PROFILE_TEXT (profile_text, user_id, visible) VALUES (:text, :user_id, 1)"
        db.session.execute(sql, {"text":text, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def get_profile_text(user_id):
    """returns the profile text of a given user"""
    try:
        sql = "SELECT profile_text from PROFILE_TEXT where user_id =:user_id and visible = 1"
        return db.session.execute(sql, {"user_id": user_id}).fetchone()[0]
    except:
        return False

def delete_profile_text(user_id):
    """deletes the profile text of the given user"""
    try:
        sql = """DELETE from profile_text WHERE user_id=:user_id"""
        db.session.execute(sql, {"user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def add_job_experience(user_id, employer, role, description, beginning, ended):
    """adds a job experience into the profile (only for employees)"""
    try:
        sql = """INSERT into JOB_EXPERIENCE (user_id, employer, role, description, beginning, ended) VALUES (:user_id, :employer, 
        :role, :description, :beginning, :ended)"""
        db.session.execute(sql, {"user_id":user_id, "employer":employer, "role":role, "description":description, "beginning":beginning, "ended":ended})
        db.session.commit()
        return True
    except:
        return False

def get_all_job_experience(user_id):
    """returns all the job experience of a user (only for employees)"""
    sql = "SELECT id, employer, role, description, beginning, ended FROM JOB_EXPERIENCE WHERE user_id=:user_id ORDER BY ended"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def delete_job_experience(experience_id):
    try:
        sql = """DELETE from JOB_EXPERIENCE WHERE id=:id"""
        db.session.execute(sql, {"id":experience_id})
        db.session.commit()
        return True
    except:
        return False

def add_education(user_id, school, level, description, beginning, graduation):
    """adds an education (only for employees)"""
    try:
        sql = """INSERT into EDUCATION (user_id, school, level, description, beginning, graduation) VALUES (:user_id, :school, 
        :level, :description, :beginning, :graduation)"""
        db.session.execute(sql, {"user_id":user_id, "school":school, "level":level, "description":description, "beginning":beginning, "graduation":graduation})
        db.session.commit()
        return True
    except:
        return False

def delete_education(education_id):
    """deletes education (only for employees)"""
    sql = """DELETE from EDUCATION WHERE id=:education_id"""
    db.session.execute(sql, {"education_id":education_id})
    db.session.commit()
    try:
        sql = """DELETE from EDUCATION WHERE id=:education_id"""
        db.session.execute(sql, {"education_id":education_id})
        db.session.commit()
        return True
    except:
        return False



def get_all_education(user_id):
    """returns all the education of a user (only for employees)"""
    sql = "SELECT id, school, level, description, beginning, graduation FROM EDUCATION WHERE user_id=:user_id ORDER BY graduation"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def get_job_experience(id):
    """returns the job experience info with the given id"""
    sql = """SELECT id, employer, role, description, beginning, ended FROM JOB_EXPERIENCE where id=:id"""
    return db.session.execute(sql, {"id":id}).fetchone()

def get_education(education_id):
    """returns the education information with the given education id"""
    sql = """SELECT id, school, level, description, beginning, graduation FROM EDUCATION where id=:education_id"""
    return db.session.execute(sql, {"education_id":education_id}).fetchone()