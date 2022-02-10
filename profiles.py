
from db import db

#profiilitekstin muokkaaminen tehdään lähettämällä uusi profiiliteksti ja poistamalla sen jälkeen vanha jos onnistuu

def add_profile_text(user_id, text):
    print("minua kutsuttiin")
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

def add_job(user_id):
    """adds a job experience into the profile (only for employees)"""
    pass

def get_jobs(user_id):
    """returns all the job experience of a user (only for employees)"""
    pass

def delete_job(user_id):
    """deletes a given job experience of a user (only for employees)"""

def add_education(user_id):
    """adds an education (only for employees)"""

def delete_education(user_id):
    """deletes and education (only for employees"""

def get_education(user_id):
    """returns all the education of a user (only for employees)"""