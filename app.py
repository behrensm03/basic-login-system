# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import sqlite3
import account, bcrypt, security
from time import sleep


# create the application object
app = Flask(__name__)

app.secret_key = "secret"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# create sqlalchemy object
# db = SQLAlchemy(app)

from models import *



# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap




# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
   # posts = db.session.query(BlogPost).all()
   return render_template('index.html'
                          #,posts=posts
                          )



# @app.route('/welcome')
# def welcome():
#     return render_template('welcome.html')  # render a template


@app.route('/register', methods=['GET', 'POST'])
def register():
    error=None
    if request.method == 'POST':
        if (security.validRegister(request.form['username'], request.form['password'], request.form['confirmpassword'])):
            passHash = bcrypt.hashpw(request.form['password'].encode('utf8'), bcrypt.gensalt())
            act = account.Account(request.form['firstName'], request.form['lastName'], request.form['username'], passHash, request.form['email'], request.form['gradYear'], request.form['academy'], request.form['jobTitle'], request.form['company'])
            # security.register(request.form['username'], request.form['password'], request.form['confirmpassword'])
            security.registerV2(act, request.form['password'], request.form['confirmpassword'])
            return redirect(url_for('login'))
        else:
            error=security.registerError(request.form['username'], request.form['password'], request.form['confirmpassword'])
            
    return render_template('register.html', error=error)



# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'logged_in' in session:
        return redirect(url_for('home'))
    elif request.method == 'POST':
        if security.login(request.form['username'], request.form['password']):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials.'
    return render_template('login.html', error=error)
    

@app.route('/myaccount')
def myaccount():
    if not ('logged_in' in session):
        return redirect(url_for('login'))
    else:
        user = security.getUser(session['username'])
        return render_template('myaccount.html', us=account.getUsername(user), f=account.getProperty(user, 'firstName'),
                               l=account.getProperty(user, 'lastName'), e=account.getProperty(user, 'email'),
                               gy=account.getProperty(user, 'gradYear'), a=account.getProperty(user, 'academy'),
                               j=account.getProperty(user, 'jobTitle'), c=account.getProperty(user, 'company'))


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    error = None
    confirm = None
    if request.method == 'POST':
        if security.updatePassword(request.form['username'], request.form['password'], request.form['confirmpassword']):
            flash('Password updated.')
            sleep(1)
            return redirect(url_for('home'))
        else:
            error="Invalid."
    return render_template('update.html', error=error, confirm=confirm)


def renderv2(l, m):
    confirm=None
    return render_template(l, confirm=m)




@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# def connect_db():
#     return sqlite3.connect(app.database)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
    

