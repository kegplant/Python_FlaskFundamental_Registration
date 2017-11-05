from flask import Flask, render_template, request, redirect,session, flash
import random
import re
import datetime
app = Flask(__name__)
app.secret_key='poshit'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# our index route will handle rendering our form
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process():
    session['user']=request.form
    for key,value in request.form.items():
        if len(request.form[key])<1:
            flash('{} must not be empty!'.format(key))
            return redirect('/')
    if not (request.form['first_name'].isalpha() and request.form['last_name'].isalpha()):
        flash('First and Last Names are letters only!')
        return redirect('/')
    if len(request.form['password'])<8:
        flash('Password must be 8 or more letters long!')
        return redirect('/')
    if len(request.form['password'])!=len(request.form['password2']):
        flash('Passwords must match!')
        return redirect('/')
    if not EMAIL_REGEX.match(request.form['eml']):
        flash('Invalid Email Address!')
        return redirect('/')
    if (not any(c.isupper() for c in request.form['password'])) or (not any(c.isdigit() for c in request.form['password'])):
        flash('Password must have at least one capital letter and one number!')
        return redirect('/')
    today=str(datetime.date.today())
    if (today<request.form['bday']):
        flash('B-day must not be in the future!')
        return redirect('/')
    flash('Thanks for submitting your information!')
    return redirect('/')
    # print type(request.form)
    # print 'abcde'

    # return render_template('result.html',info=session['user'])


app.run(debug=True)