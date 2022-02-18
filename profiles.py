
from db import db

#profiilitekstin muokkaaminen tehdään lähettämällä uusi profiiliteksti ja poistamalla sen jälkeen vanha jos onnistuu

def add_profile_text(user_id, text):
    """adds profile text to the profile (both employees and employers)"""
    try:
        sql = "UPDATE PROFILE_TEXT SET visible = 0 WHERE user_id=:user_id"
        db.session.execute(sql, {"user_id":user_id})
        db.session.commit()
        #tähän kohtaan pitäisi laittaa vanhan profiilitekstin poistaminen, tavallaan ei haittaa jos käyttäjällä useita profiilitekstejä, mutta
        #jotenkin olis hyvä pitää tiedossa mikä on viimeisin
        #esim alkuun vois laittaa vanhojen profiilitekstien laittamisen piiloon
        #jos haluaa kokonaan poistaa niin voi poistaa tän jälkeen ne missä visible = 0
        sql = "INSERT into PROFILE_TEXT (profile_text, user_id, visible) VALUES (:text, :user_id, 1)"
        db.session.execute(sql, {"text":text, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

#tätä funktiota ei varmaan tarvita, koska käyttäjä voi "poistaa" profiilitekstinsä lähettämällä vaan tyhjän lomakkeen
#def delete_profile_text(user_id):
 #   """deletes a profile text"""
  #  sql = "UPDATE PROFILE_TEXT SET profile_text = NULL where user_id =:user_id"
   # db.session.execute(sql, {"user_id": user_id})
    #db.session.commit()


def get_profile_text(user_id):
    """returns the profile text of a given user"""
    try:
        sql = "SELECT profile_text from PROFILE_TEXT where user_id =:user_id and visible = 1"
        return db.session.execute(sql, {"user_id": user_id}).fetchone()[0]
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

def get_job_experience(user_id):
    """returns all the job experience of a user (only for employees)"""
    sql = "SELECT employer, role, description, beginning, ended FROM JOB_EXPERIENCE WHERE user_id=:user_id ORDER BY ended"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def delete_job(user_id):
    """deletes a given job experience of a user (only for employees)"""
    pass

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

def delete_education(user_id):
    """deletes and education (only for employees)"""
    pass

def get_education(user_id):
    """returns all the education of a user (only for employees)"""
    sql = "SELECT school, level, description, beginning, graduation FROM EDUCATION WHERE user_id=:user_id ORDER BY graduation"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()