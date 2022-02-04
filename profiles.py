
from db import db

def add_profile_text(user_id, user_role, text):
    if user_role == 0:
        sql = "INSERT into EMPLOYEES (profile_text) VALUES (:text) WHERE id =:user_id"
    else:
        sql = "INSERT into EMPLOYERS (profile_text) VALUES (:text) WHERE id =:user_id"
    db.session.execute(sql, {"text":text, "user_id":user_id})
    db.session.commit()

def delete_profile_text(user_id,user_role):
    if user_role == 0:
        sql = "UPDATE EMPLOYEES SET profile_text = NULL where id =:user_id"
    else:
        sql = "UPDATE EMPLOYERS SET profile_text = NULL where id =:user_id"
    db.session.execute(sql, {"user_id": user_id})
    db.session.commit()


def get_profile_text(user_id, user_role):
    if user_role == 0:
        sql = "SELECT profile_text from EMPLOYEES where id =: user_id"
    else:
        sql = "SELECT profile_text from EMPLOYERS where id =: user_id"
    return db.session.execute(sql, {"user_id": user_id}).fetchone([0])