from flask import Flask, render_template, request, redirect,session, flash
import random
app = Flask(__name__)
app.secret_key='poshit'
# our index route will handle rendering our form
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process():
    session['user']=request.form
    if False:
        flash('')
        return redirect('/')
    flash('Thanks for submitting your information')
    return render_template('result.html',info=session['user'])


app.run(debug=True)