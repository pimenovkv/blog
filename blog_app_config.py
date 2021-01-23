import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # секретный ключ (используется в некоторых расширениях flask для безопасности)
    SECRET_KEY = 'debug_secret_key'

    # путь для подключения к базе данных
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog_app.db')
    # отслеживание изменения объектов и отправка сигналов
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # число постов, отображаемых на странице
    POSTS_PER_PAGE = 10
    # число комментариев, отображаемых на странице
    COMMENTS_PER_PAGE = 10
