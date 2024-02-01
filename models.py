from db import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    courses = db.relationship('Course')
    departments = db.relationship('Department')
    students = db.relationship('Student')

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(80),  nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Department(db.Model):
    __tablename__='departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Student(db.Model):
    __tablename__ ='students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    academics = db.relationship('Academic', backref='student')

class Academic(db.Model):
    __tablename__ ='academics'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(80), nullable=True)
    year = db.Column(db.String(80), nullable=True)
    beg_semester = db.Column(db.String(80), nullable=True)
    end_semester = db.Column(db.String(80),  nullable=True)
    semester = db.Column(db.String(80),  nullable=True)
    school_year = db.Column(db.String(80), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)

