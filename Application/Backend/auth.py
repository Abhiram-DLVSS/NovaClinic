import re
from flask import Blueprint,render_template,request,flash
from Application.DBHandler import Mysqlhandler

auth = Blueprint('auth',__name__)


@auth.route('/homepage',methods=['GET','POST'])
def home_button():
    return render_template("home1.html")

@auth.route('/Our specializations',methods=['GET','POST'])
def specialization():
    return render_template("spec.html")



@auth.route('/logout')
def logout():
    return "<p>Logout</p>"