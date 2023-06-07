from school_web import app,s,bcrypt,Base,mail,engine,session
from flask import render_template,redirect,url_for,flash,request
from school_web.forms import ExamForm, RegistrationForm,LoginForm,RequestResetForm,ResetPasswordForm,\
    ExamForm
from school_web.models import Student
from flask_login import login_user,current_user,login_required,logout_user
import itsdangerous
from email.message import EmailMessage
import ssl
import smtplib
from flask_mail import Message

@app.route('/')
def void():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        Base.metadata.create_all(engine)
        student = Student(surname=form.surname.data,firstname=form.firstname.data,
        middlename=form.middlename.data,gender=form.gender.data,
        phonenumber=form.phonenumber.data, 
        email=form.email.data,country=form.country.data,state=form.country.data,
        date_of_birth=form.date_of_birth.data,
        username=form.username.data,password=hashed_password)
        session.add(student)
        session.commit()
    if request.method == 'GET':
        return render_template('register.html',form=form,title='Register')
        
    email = request.form['email']
    token = s.dumps(email,salt='email-confirm')
    link = url_for('confirm_email',token=token,_external=True)
    msg_body = f'Your link is {link}'

    email_sender = 'chiedoziedavidehirim@gmail.com'
    email_receiver = [email]
    email_password = 'ogeapajgdeybegnu'
    email_subject = 'Confirm Email'
    email_body = msg_body

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = email_subject
    em.set_content(email_body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',port=465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())
    return f'''<h4>We sent a link to {form.email.data}.Please click on the link
    to confirm that you are the real owner of the email account.</h4>'''

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token,salt='email-confirm')
    except (itsdangerous.SignatureExpired,itsdangerous.BadTimeSignature) as error:
        if str(error).endswith('seconds'):
            error_message = 'This token has expired.Please try again'.title()
        elif str(error).endswith('does not match'):
            error_message = 'This token is invalid.Please check and try again'.title()
        return f'''<h4 style="background-color:red;color:blanchedalmond">
                        {error_message}
                    </h4>'''
    else:
        student = session.query(Student).all()
        student[-1].confirmed = True
        session.commit()
        return '''<div style="background-color:cyan;color:whitesmoke">
            <h4>Registration Successful.</h4>
        </div>'''

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = session.query(Student).filter_by(username=form.username.data).first()
        password = bcrypt.check_password_hash(student.password, form.password.data)
        #flash('Login Unsuccessful. Please check username and password'.capitalize())
        if student and password: #and student.confirmed==1:
            login_user(student,remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful'.title())
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password'.title())
    return render_template('login.html',form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def send_reset_email(student):
    token = student.get_reset_token()
    msg = Message('Password Reset Request',sender='noreply@demo.com',recipients=[student.email])
    msg.body = f'''To reset your password, visit the following link
    {url_for('reset_token',token=token,_external=True)}
    Please ignore if you did not make this request.
    '''
    mail.send(msg)

@app.route('/reset_request',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student:
            send_reset_email(student)
            flash('An email has been sent on how you can reset your password','info')
            return redirect(url_for('login'))
        else:
            flash('This email address does not exst'.title())
    return render_template('reset_request.html',title='Reset Password',form=form) 

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    student = Student.verify_reset_token(token)
    if student is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        student.password = hashed_password
        session.commit()
        flash('Your password has been updated')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset Password',form=form)

@app.route('/take_exams',methods=['post','get'])
@login_required
def take_exams():
    form = ExamForm()
    if form.validate_on_submit():
        Base.metadata.create_all(engine)
        flash('You have submitted successfully')
        print(form.question1.data)
        print(form.question2.data)
        return redirect(url_for('account'))
    else:
        print(form.errors)
    return render_template('take_exams.html',form=form,title='Exams')

@app.route('/check_results')
@login_required
def check_results():
    return render_template('check_results.html',title='CheckResults')

@app.route('/pay_fees')
@login_required
def pay_fees():
    return render_template('pay_fees.html',title='PayFees')