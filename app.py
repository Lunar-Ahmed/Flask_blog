from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQL

app = Flask(__name__)

app.config['SECRET_KEY']= 'b81f169758b476bf1c1bbec7825b149a'

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
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for{form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__ =='__main__':
    app.run(debug=True)