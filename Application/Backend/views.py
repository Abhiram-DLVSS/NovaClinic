from flask import Blueprint,render_template

from Application.DBHandler.sqlhandler import Mysqlhandler

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("welcome.html")
