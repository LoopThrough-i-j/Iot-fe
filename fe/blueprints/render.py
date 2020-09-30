from flask import Blueprint, render_template

render = Blueprint("base", __name__, static_folder='static/')


@render.route('/signin')
def signin():
    return render_template('signin.html')
