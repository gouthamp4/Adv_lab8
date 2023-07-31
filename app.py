import os
from flask import Flask, render_template, session,redirect,url_for,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField,FloatField
from wtforms.validators import NumberRange
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oursecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    grade = db.Column(db.Float)

    def __init__(self,name,grade):
        self.name=name
        self.grade=grade
    def __repr__(self):
        return f"Student {self.name} got {self.grade}"



class MyForm(FlaskForm):
    student = StringField("Full Name: ")
    mid1 = FloatField("Midterm#1: ")
    mid2 = FloatField("Midterm#2: ")    
    mid3 = FloatField("Final Exam: ")
    submit = SubmitField("Save")
    display = SubmitField("Display the records")
    deletename = StringField("Full Name: ")
    delete = SubmitField("Delete the record")




@app.route('/', methods=['GET','POST'])
def index():
    error=''
    form = MyForm()
    if request.method == 'POST':
        
        if form.submit.data:
            
            session['student'] = form.student.data
            session['mid1'] = form.mid1.data
            session['mid2'] = form.mid2.data
            session['mid3'] = form.mid3.data
            if session['student'] == '':
                error="Student name is empty"
            elif session['mid1']==None or session['mid1']< 0 or session['mid1'] >100.0:
                error="Invalid Mid1 marks"
            elif session['mid2']==None or session['mid2']< 0 or session['mid2'] >100.0:
                error="Invalid Mid2 marks"
            elif session['mid3']==None or session['mid3']< 0 or session['mid3'] >100.0:
                error="Invalid Final marks"
            if error!='':
                return render_template('index.html',form=form,error=error)
            average = (session['mid1'] + session['mid2'] + 2 * session['mid3']) / 4
            

            new_student = Student(session['student'],average)
            db.session.add(new_student)
            db.session.commit()

            student_details = Student.query.all()
            for student in student_details:
                print(student.name)
                print(student.grade)

            return redirect(url_for('index'))
      

        elif form.display.data:
            return redirect(url_for('display'))
        
        elif form.delete.data:
            deldata = form.deletename.data
            delstudent = Student.query.filter_by(name=deldata).all()
            for delete_student in delstudent:
                db.session.delete(delete_student) #referred in chatgpt
                db.session.commit()
            return redirect(url_for('index'))
    return render_template('index.html',form=form,error=error)

@app.route('/display')
def display():
    student_details = Student.query.all() 
    return render_template('display.html',students=student_details)



if __name__ == '__main__':
    
    app.app_context().push()
    db.create_all()
    app.run(debug=True)