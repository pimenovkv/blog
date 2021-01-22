from blog_app import app, db
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from blog_app.models import Users, Posts
from blog_app.forms import LoginForm, RegistrForm, NewPostForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_anonymous:
        username = None
        form = None
    else:
        username = current_user.name
        form = NewPostForm()
        if form.validate_on_submit():  # обработка формы и валидация данных только при запросе POST
            post = Posts(title=form.title.data, body=form.body.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
    posts = Posts.query.order_by(Posts.timestamp.desc()).all()
    return render_template('index.html', title='Home', username=username, form=form, posts=posts)


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:   # если пользователь уже вошел, то будет перенаправлен
        return redirect(url_for('index'))
    form = RegistrForm()
    if form.validate_on_submit():   # обработка формы и валидация данных только при запросе POST
        user = Users(name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Redistration success!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)
