from blog_app import app
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from blog_app.models import Users
from blog_app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    strings = ['String 1', 'String 2', 'String 3']
    if current_user.is_anonymous:
        username = None
    else:
        username = current_user.name
    return render_template('index.html', title='Home', user=username, strings=strings)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:   # если пользователь уже вошел, то будет перенаправлен
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():   # обработка формы и валидация данных только при запросе POST
        user = Users.query.filter_by(name=form.username.data).first()
        if user is None:    # проверка имени пользователя (такой пользователь существует)
            flash('Invalid username')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):   # проверка пароля
            flash('Invalid password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)    # теперь в переменной current_user данные об этом пользователе
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
