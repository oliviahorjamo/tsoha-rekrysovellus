import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

#user_role = 1 means that the user is an employer and the user information is
#in the employers -table

def login(name, password):
    sql = "SELECT password, id FROM employees WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        sql = "SELECT password, id FROM employers WHERE name=:name"
        result = db.session.execute(sql, {"name":name})
        user = result.fetchone()
        if not user:
            return False
        if not check_password_hash(user[0], password):
            return False
        session["user_role"] = 1
    else:
        if not check_password_hash(user[0], password):
            return False
        session["user_role"] = 0

    session["user_id"] = user[1]
    session["user_name"] = name
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def register(name, password, role):
    print("db", db)
    print("minua kutsuttiin")
    hash_value = generate_password_hash(password)
    print("role", role)
    print(type(role))
    print(role == "1")
    print(role == "0")
    if role == "1":
        print("roolini on 1")
        try:
            sql = "INSERT INTO employers (name, password) VALUES (:name, :password)"
            print("olen tehnyt sql lauseen, rooli = 1")
            db.session.execute(sql, {"name":name, "password":hash_value})
            print("olen suorittanut sql komennon, rooli = 1")
            db.session.commit()
            print("commit onnistui")
        except:
            return False
    elif role == "0":
        try:
            print("olen tryssa")
            sql = "INSERT INTO employees (name, password) VALUES (:name, :password)"
            print("olen tehnyt sql lauseen")
            db.session.execute(sql, {"name":name, "password":hash_value})
            print("olen suorittanut executen")
            db.session.commit()
        except:
            return False
    return login(name, password)

def user_id():
    return session.get("user_id", 0)

def user_role():
    return session.get("user_role", 0)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

