from blog_app import app
from blog_app import db
from blog_app.models import Users, Posts


# TODO: разобраься с flask shell
# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'Users': Users, 'Posts': Posts}


if __name__ == '__main__':
    app.run(debug=True)
