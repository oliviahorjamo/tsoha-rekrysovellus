
from db import db

#profiilitekstin muokkaaminen tehdään lähettämällä uusi profiiliteksti ja poistamalla sen jälkeen vanha jos onnistuu

def add_profile_text(user_id, user_role, text):
    """adds profile text to the profile (both employees and employers)"""
    if user_role == 0:
        sql = "INSERT into EMPLOYEES (profile_text) VALUES (:text) WHERE id =:user_id"
    else:
        sql = "INSERT into EMPLOYERS (profile_text) VALUES (:text) WHERE id =:user_id"
    db.session.execute(sql, {"text":text, "user_id":user_id})
    db.session.commit()

def delete_profile_text(user_id,user_role):
    """deletes a profile text"""
    if user_role == 0:
        sql = "UPDATE EMPLOYEES SET profile_text = NULL where id =:user_id"
    else:
        sql = "UPDATE EMPLOYERS SET profile_text = NULL where id =:user_id"
    db.session.execute(sql, {"user_id": user_id})
    db.session.commit()


def get_profile_text(user_id, user_role):
    """returns the profile text of a given user"""
    if user_role == 0:
        sql = "SELECT profile_text from EMPLOYEES where id =: user_id"
    else:
        sql = "SELECT profile_text from EMPLOYERS where id =: user_id"
    return db.session.execute(sql, {"user_id": user_id}).fetchone([0])

def add_job(user_id, user_role):
    """adds a job experience into the profile (only for employees)"""
    pass

def get_jobs(user_id, user_role):
    """returns all the job experience of a user (only for employees)"""
    pass

def delete_job(user_id, user_role):
    """deletes a given job experience of a user (only for employees)"""

def add_education(user_id, user_role):
    """adds an education (only for employees)"""

def delete_education(user_id, user_role):
    """deletes and education (only for employees"""

def get_education(user_id, user_role):
    """returns all the education of a user (only for employees)"""