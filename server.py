#note email is named eml in html & request.form
from flask import Flask, render_template, request, redirect,session, flash
from mysqlconnection import MySQLConnector
import random
import re
import datetime

import md5, os, binascii

app = Flask(__name__)
app.secret_key='poshit'
mysql = MySQLConnector(app,'registration')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# helper functions
def noDupeEmail(email):
    query='select email from users where email= :email'
    data={'email':email}
    result=mysql.query_db(query,data)
    if result:
        return False
    else:
        return True
def loggedIn():
    try:
        session['loggedIn']
    except:
        session['loggedIn']=False
    if session['loggedIn']==False:
        session['user_ID']=-1
    return session['loggedIn']

# our index route will handle rendering our form
@app.route('/')
def index():
    status=loggedIn()
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process(): 
    status=loggedIn()
    if request.form['type']=='log in':
        flash('loggin in...')
        for key,value in request.form.items():
            if len(request.form[key])<1:
                flash('{} must not be empty!'.format(key))
                return redirect('/')
        if not EMAIL_REGEX.match(request.form['eml']):
            flash('Invalid Email Address!')
            return redirect('/')
        if len(request.form['password'])<8:
            flash('Password must be 8 or more letters long!')
            return redirect('/')
        email = request.form['eml']
        password = request.form['password']
        user_query = "SELECT * FROM users WHERE users.email = :email LIMIT 1"
        query_data = {'email': email}
        user = mysql.query_db(user_query, query_data)
        if len(user) != 0:
            encrypted_password = md5.new(password + user[0]['salt']).hexdigest()
            if user[0]['password'] == encrypted_password:
                flash('Successfully logged in')
                session['loggedIn']=True
                session['user_ID']=user[0]['id']
                return redirect('/result')
            else:
                flash('invalid password!')
        else:
            flash('invalid email!')
        return redirect('/')

    elif request.form['type'] != 'register':
        flash('wrong choice!')
        return redirect('/')

    #session['loggedIn']=False
    for key,value in request.form.items():
        if len(request.form[key])<1:
            flash('{} must not be empty!'.format(key))
            return redirect('/')
    # if not (request.form['first_name'].isalpha() and request.form['last_name'].isalpha()):
    #     flash('First and Last Names are letters only!')
    #     return redirect('/')
    if not (len(request.form['first_name'])>1 and len(request.form['last_name'])>1):
        flash('First and Last Names must be at least 2 characters long!')
        return redirect('/')
    if len(request.form['password'])<8:
        flash('Password must be 8 or more letters long!')
        return redirect('/')
    if request.form['password'] != request.form['password2']:
        flash('Passwords must match!')
        return redirect('/')
    if not EMAIL_REGEX.match(request.form['eml']):
        flash('Invalid Email Address!')
        return redirect('/')
    # if (not any(c.isupper() for c in request.form['password'])) or (not any(c.isdigit() for c in request.form['password'])):
    #     flash('Password must have at least one capital letter and one number!')
    #     return redirect('/')

    # today=str(datetime.date.today())
    # if (today<request.form['bday']):
    #     flash('B-day must not be in the future!')
    #     return redirect('/')
    
    first_name=request.form['first_name']
    email=request.form['eml']
    #check no dupes
    if not noDupeEmail(email):
        flash('Email already registered!')
        return redirect('/')
    session['loggedIn']=True
    password=request.form['password']
    salt=binascii.b2a_hex(os.urandom(15))
    hashed_pw=md5.new(password+salt).hexdigest()
    insert_query = "INSERT INTO users (first_name, email, password, salt, created_at, updated_at) VALUES (:first_name, :email, :hashed_pw, :salt, NOW(), NOW())"
    query_data = { 'first_name': first_name, 'email': email, 'hashed_pw': hashed_pw, 'salt': salt}
    # print insert_query
    # print query_data
    session['user_ID']=mysql.query_db(insert_query,query_data)
    flash('Thanks for submitting your information!')

    return redirect('/result')
@app.route('/result')
def result():
    status=loggedIn()
    return render_template('result.html')
@app.route('/log_out')
def logOut():
    session['loggedIn']=False
    return redirect('/')

app.run(debug=True)