from blog_app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    strings = ['String 1', 'String 2', 'String 3']
    return render_template('index.html', title='Home', user='User', strings=strings)
