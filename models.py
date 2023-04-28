import os
from sqlalchemy import Column, String, Integer, Boolean, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from decouple import config

db_host = config('DB_HOST')
db_user = config('DB_USER')
db_password = config('DB_PASSWORD')
db_name = config('DB_NAME')
database_path = 'postgresql://{}:{}@{}/{}'.format(
    db_user, db_password, db_host, db_name)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


"""
Users

"""

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    privileges = Column(String)

    def __init__(self, username, password, privileges):
        self.username = username
        self.password = password
        self.privileges = privileges

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'privileges': self.privileges,
        }


"""
Jobs

"""

class Job(db.Model):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    company = Column(String, nullable=False)
    company_img = Column(String, nullable=False)
    job_title = Column(String)
    job_description = Column(String)
    upload_date = Column(Date)
    is_approved = Column(Boolean, default=False)

    def __init__(self, company, company_img, job_title, job_description):
        self.company = company
        self.company_img = company_img
        self.job_title = job_title
        self.job_description = job_description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'company': self.company,
            'company_img': self.company_img,
            'job_title': self.job_title,
            'job_description': self.job_description,
            'upload_date': self.upload_date,
            'is_approved': self.is_approved
        }
