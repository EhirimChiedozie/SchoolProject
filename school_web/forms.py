from flask_wtf import FlaskForm,Form,csrf
from wtforms import StringField,PasswordField,DateField,SubmitField,EmailField,\
BooleanField,IntegerField,RadioField,SelectField
from wtforms.validators import InputRequired, Length, EqualTo,Email,DataRequired,Optional,\
    ValidationError 
from flask_wtf.file import FileField,FileAllowed
from school_web.models import Student
from school_web import session
import pycountry

class RegistrationForm(FlaskForm):
    surname = StringField('Surname:', validators=[DataRequired(),Length(min=2,max=30)])
    firstname = StringField('Firstname:',validators=[DataRequired(),Length(min=2,max=30)])
    middlename = StringField('Middlename(Optional):', validators=[Optional(),Length(min=2,max=30)])
    gender = RadioField('Gender',choices=[('Male','Male'),('Female','Female'),\
        ('Transgender','Transgender'),('Prefer not to say','Prefer not to say')],\
            validators=[InputRequired()],coerce=str)
    phonenumber = StringField('Phonenumber:',validators=[DataRequired(),Length(min=9,max=18)])
    email = StringField('Email Address:',validators=[DataRequired(),Length(min=7,max=100)])
    country = SelectField('Country',choices=[(country.alpha_2,country.name)\
        for country in pycountry.countries])
    state = StringField('State Of Origin:',validators=[DataRequired(),Length(min=2,max=19)])
    date_of_birth = DateField('Date Of Birth:',validators=[DataRequired()])
    username = StringField('Choose a username:',validators=[DataRequired(),Length(min=2,max=50)])
    password = PasswordField('Choose a password:',validators=[DataRequired(),Length(min=8,max=50)])
    confirm_password = PasswordField('Confirm your password:',validators=[DataRequired(), EqualTo('password')])
    #picture = FileField('Recent Passport Photograph',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Register')

    def validate_phonenumber(self,phonenumber):
        phone = session.query(Student).filter_by(phonenumber=phonenumber.data).first()
        if phone:
            raise ValidationError('This phonenumber already exists. Please enter a different one')

    def validate_email(self,email):
        email = session.query(Student).filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email already exists. Please choose a different one')

    def validate_username(self,username):
        username = session.query(Student).filter_by(username=username.data).first()
        if username:
            raise ValidationError('This username already exists. Please choose a different one')


class LoginForm(FlaskForm):
    username = StringField('Username:',validators=[DataRequired(),Length(min=2,max=50)])
    password = PasswordField('Password:',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email Address:',validators=[DataRequired(),Length(min=7,max=100)])
    submit = SubmitField('Submit')
    
    def validate_email(self,email):
        email = session.query(Student).filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('This email does not exist in the database')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Choose a password:',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm your password:',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class ExamForm(FlaskForm):
    question1 = RadioField('What is your name',\
    choices=[('Edozie','Edozie'),('Ehirim','Ehirim'),('David','David'),('Osuamadi','Osuamadi')],\
    validators=[Optional()],coerce=str)

    question2 = RadioField('What is your relationship status',\
    choices=[('Single','Single'),('Married','Married'),('Breakfasted','Breakfasted'),('God when','God when')],\
    validators=[Optional()],coerce=str)
    submit = SubmitField('Submit')