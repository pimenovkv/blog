from blog_app import app
from flask import render_template, flash, redirect, url_for
from blog_app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    strings = ['String 1', 'String 2', 'String 3']
    return render_template('index.html', title='Home', user='User', strings=strings)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():     # обработка формы только при запросе POST
        if form.validate():     # валидация полей
            return redirect(url_for('index'))
        else:
            flash('Wrong data!')
    return render_template('login.html', title='Sign In', form=form)
