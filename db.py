
  
from os import getenv
from app import app
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URL"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)