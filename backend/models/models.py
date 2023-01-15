import os
import sys
import inspect
import config

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db_uri =  'mysql://' + config.user + ':' + config.password + '@' + config.host + '/' + config.database
db = SQLAlchemy()

# Create a MySQL database Courses table
class Courses(db.Model):
    __tablename__ = 'courses'
    cUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cName = db.Column(db.String(100), nullable=False)
    cSubject = db.Column(db.String(100), nullable=False)
    cCode = db.Column(db.String(100), nullable=False)
    cCredits = db.Column(db.String(20), nullable=False)
    cDescription = db.Column(db.String(2000), nullable=False)
    cReq = db.Column(db.String(400), nullable=False)

    def __init__(self, cUID, cName, cSubject, cCode, cCredits, cDescription, cReq):
        self.cUID = cUID
        self.cName = cName
        self.cSubject = cSubject
        self.cCode = cCode
        self.cCredits = cCredits
        self.cDescription = cDescription
        self.cReq = cReq

    def __repr__(self):
        return '<Course %r>' % self.cName

# Create a MySQL database Professors table
class Professors(db.Model):
    __tablename__ = 'professors'
    pUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pName = db.Column(db.String(100), nullable=False)
    pData = db.Column(db.String(300), nullable=False)
  
    def __init__(self, pUID, pName, pData):
        self.pUID = pUID
        self.pName = pName
        self.pData = pData

    def __repr__(self):
        return '<Professor %r>' % self.pName

# Create a MySQL database RC table
class RC(db.Model):
    __tablename__ = 'rc'
    comID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    comBody = db.Column(db.String(1000), nullable=False)
    comLink = db.Column(db.String(200), nullable=False)
    comVotes = db.Column(db.Integer, nullable=False)
    cUID = db.Column(db.Integer, db.ForeignKey('courses.cUID'), nullable=False)

    def __init__(self, comID, comBody, comLink, comVotes, cUID):
        self.comID = comID
        self.comBody = comBody
        self.comLink = comLink
        self.comVotes = comVotes
        self.cUID = cUID

    def __repr__(self):
        return '<RC %r>' % self.comID

# Create a MySQL database Teaches table
class Teaches(db.Model):
    __tablename__ = 'teaches'
    tUID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pUID = db.Column(db.Integer, db.ForeignKey('professors.pUID'), nullable=False)
    cUID = db.Column(db.Integer, db.ForeignKey('courses.cUID'), nullable=False)

    def __init__(self, tUID, pUID, cUID):
        self.tUID = tUID
        self.pUID = pUID
        self.cUID = cUID

    def __repr__(self):
        return '<Teaches %r>' % self.tUID