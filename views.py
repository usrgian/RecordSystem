
from flask import Flask, redirect, url_for, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user,\
current_user, login_required
from models import User, Course, Department, Student, Academic
from flask_moment import Moment
from db import create_db, db
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key ='hshsh'
login_manger = LoginManager(app)
login_manger.login_view = 'login'
moment = Moment(app)
create_db(app)

@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    count_student = Student.query.count()
    return render_template('home.html',count_studen=count_student)

@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('userName')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user: 
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                pass
        else:
            pass
    return render_template('auth.html')

@app.route('/sign-up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('userName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(username=username).first()
        if user:
            pass
        elif password1 != password2:
            pass
        else:
            new_user = User(username=username,\
            email=email, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
    return redirect(url_for('home'))

@app.route('/student')
def method_name():
    return render_template('students.html')

@app.errorhandler(404)
def bar(error):
    return "Page not found!"

@app.route('/maintenance', methods=['GET', 'POST'])
@login_required
def department():
    if request.method == 'POST':
        department = request.form.get('department')
        description = request.form.get('description')
        status = request.form.get('status')
        new_department = Department(name=department,
        is_active=status, description=description,\
        user_id=current_user.id)
        db.session.add(new_department)
        db.session.commit()
        return redirect(url_for('department'))
    return render_template('maintenance.html')

@app.route('/course', methods=[ 'POST'])
@login_required
def course():
    if request.method == 'POST':
        course = request.form.get('course')
        department = request.form.get('department')
        description = request.form.get('description')
        status = request.form.get('status')
        new_course = Course(name=course,\
        is_active=status, department=department, description=description,\
        user_id=current_user.id)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('department'))
    return render_template('course.html')

@app.route('/add-student', methods=['POST','GET'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        new_student = Student(name=name, user_id=current_user.id)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('add_student'))
    return render_template('add_student.html')

@app.route('/name/<student_id>/student', methods=['POST','GET'])
def view_info(student_id):
    student = Student.query.get_or_404(student_id)
    if student and request.method == 'POST':
        course = request.form.get('course')
        year = request.form.get('year')
        beg_semester = request.form.get('beginningStatus')
        end_semester = request.form.get('endStatus')
        semester = request.form.get('semester')
        school_year = request.form.get('schoolYear')
        new_academic = Academic(course=course, year=year,\
        beg_semester=beg_semester, end_semester=end_semester,\
        school_year=school_year, student_id=student_id , semester=semester)
        db.session.add(new_academic)
        db.session.commit()
        return redirect(url_for('view_info', student_id=student.id))
    return render_template('academic.html', student=student)

@app.route('/delete/<academic_id>/academic')
def delete_academic(academic_id):
    academic = Academic.query.get_or_404(academic_id)
    db.session.delete(academic)
    db.session.commit()
    return redirect(url_for('view_info', student_id=academic.student_id))



@app.route('/profile/<userName>')
def profile(userName):
    username = User.query.filter_by(username=userName).first()
    return render_template('profile.html', username=username)    

if __name__ =='__main__':
    app.run(debug=True)