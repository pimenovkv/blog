from blog_app import db
from blog_app.models import Users, Posts, Comments


def add_user(name, email, password):
    user = Users(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        print(error)


def get_users():
    return Users.query.all()


def get_user(user_id):
    return Users.query.get(user_id)


def add_post(title, body, user):
    post = Posts(title=title, body=body, author=user)
    db.session.add(post)
    try:
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        print(error)


def get_posts():
    return Posts.query.all()


def get_post(post_id):
    return Posts.query.get(post_id)


def get_posts_from_user(user):
    return user.posts.all()


def add_comment(body, user, post):
    comment = Comments(body=body, author=user, post=post)
    db.session.add(comment)
    try:
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        print(error)


def get_comments():
    return Comments.query.all()


def get_comment(comment_id):
    return Comments.query.get(comment_id)


def get_comments_from_post(post):
    return post.comments.all()


def get_comments_from_user(user):
    return user.comments.all()


def delete_all_users():
    users = get_users()
    for user in users:
        db.session.delete(user)
    try:
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        print(error)


def delete_all_posts():
    posts = get_posts()
    for post in posts:
        db.session.delete(post)
    try:
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        print(error)


def delete_all_comments():
    comments = get_comments()
    for comment in comments:
        db.session.delete(comment)
    try:
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        print(error)


delete_all_comments()
delete_all_posts()
delete_all_users()

add_user('tester1', 'tester1@gmail.com', '111')
add_user('tester2', 'tester2@gmail.com', '222')
add_user('tester3', 'tester3@gmail.com', '333')

print('get_users():', get_users())

print('get_user(1):', get_user(1))
print('get_user(2):', get_user(2))
print('get_user(3):', get_user(3))
print('get_user(999):', get_user(999))    # return None

add_post('Post1', 'First post from user 3', get_user(3))
add_post('Post2', 'First post from user 1', get_user(1))
add_post('Post3', 'First post from user 2', get_user(2))

print('get_posts():', get_posts())

print('get_post(1):', get_post(1))

print('get_posts_from_user(get_user(3)):', get_posts_from_user(get_user(3)))

add_comment('Comment1', get_user(1), get_post(1))
add_comment('Comment2', get_user(2), get_post(1))
add_comment('Comment3', get_user(2), get_post(2))

print('get_comments():', get_comments())

print('get_comment(1):', get_comment(1))

print('get_comments_from_user(get_user(2)):', get_comments_from_user(get_user(2)))

print('get_comments_from_post(get_post(1)):', get_comments_from_post(get_post(1)))

print('post.id, post.timestamp, post.author.name, post.body')
posts = get_posts()
for post in posts:
    print(post.id, post.timestamp, post.author.name, post.body)

print('users order by name desc:', Users.query.order_by(Users.name.desc()).all())
print('users order by name desc where pw_hash is not NULL:',
      Users.query.filter(Users.password_hash.isnot(None)).order_by(Users.name.desc()).all())

# delete_all_comments()
# delete_all_posts()
# delete_all_users()
