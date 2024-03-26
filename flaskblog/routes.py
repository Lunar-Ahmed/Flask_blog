from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, Loginform, UpdateAccountForm, request
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

app.app_context().push()
db.create_all()

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog post 2',
        'content': 'second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! you are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
            user = user.query.filter_by(email=form.email.data).first()
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
     logout_user()
     return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
     form = UpdateAccountForm()
     if form.validate_on_submit():
          current_user.username = form.username.data
          current_user.email = form.email.data
          db.session.commit()
          flash('Your accout has been updated!', 'success')
          return redirect(url_for('account'))
     elif request.method == 'GET':
          form.username.data = current_user.username
          form.email.data = current_user.email
     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
     return render_template('account.html', tittle='Account', image_file=image_file, form=form)