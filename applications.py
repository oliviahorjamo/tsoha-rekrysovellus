#uutta työtä lisättäessä lisätään kyseiselle työlle hakulomake
    #voiko selata vanhoja lomakkeita?
    #

#hakemuksen muokkaaminen seuraavasti:
    #ensin lähetetään uusi hakemus
    #jos onnistuu, poista vanha
    #jos ei onnistu, anna virheviesti

#tarjoa myös mahdollisuus poista hakemus suoraan

def get_all_application_forms():
    """returns all application forms"""
    pass

def add_application_form(job_id):
    """adds a new application form into application_form -table,
    adds a reference to the application form into the jobs -table"""
    pass

def get_application_form(job_id):
    """returns the application form of a given job"""
    pass

def send_application(user_id, user_role, job_id):
    """sends an application to a given job"""
    pass

def delete_application(user_id, application_id):
    """deletes a sent application if the job is still open"""
    pass

def get_all_applications(job_id, user_id):
    """lists all applications into a job if the user has
    added the job"""
    pass

def get_application_status(application_id, user_id):
    """returns the status of an application if
    the application is sent by the user"""
    #pitäiskö tän olla jobs.py -tiedostossa mieluummin?
    pass

