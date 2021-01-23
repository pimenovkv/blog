from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from blog_app import app, db
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
    page_idx = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.timestamp.desc()).paginate(page_idx, app.config['POSTS_PER_PAGE'], False)
    if posts.has_prev:
        prev_url = url_for('index', page=posts.prev_num)
    else:
        prev_url = None
    if posts.has_next:
        next_url = url_for('index', page=posts.next_num)
    else:
        next_url = None
    return render_template('index.html', title='Home', username=username, form=form, posts=posts.items,
                           page_idx=page_idx, prev_url=prev_url, next_url=next_url)


@app.route('/user', methods=['GET', 'POST'])
def user():
    # posts = Posts.query.filter_by(user_id=current_user.id).order_by(Posts.timestamp.desc()).all()
    form = NewPostForm()
    if form.validate_on_submit():  # обработка формы и валидация данных только при запросе POST
        post = Posts(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user'))
    page_idx = request.args.get('page', 1, type=int)
    posts = Posts.query.filter_by(user_id=current_user.id).order_by(Posts.timestamp.desc()) \
                .paginate(page_idx, app.config['POSTS_PER_PAGE'], False)
    if posts.has_prev:
        prev_url = url_for('user', page=posts.prev_num)
    else:
        prev_url = None
    if posts.has_next:
        next_url = url_for('user', page=posts.next_num)
    else:
        next_url = None
    return render_template('user.html', title='UserX', username=current_user.name, form=form, posts=posts.items,
                           page_idx=page_idx, prev_url=prev_url, next_url=next_url)


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


@app.route('/like')
def like():
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    post_id = request.args.get('post')
    post = Posts.query.filter_by(id=post_id).first()
    if post is None or post.user_id == current_user.id:
        return redirect(next_page)
    post.like_num += 1
    db.session.commit()
    return redirect(next_page)
