import re
from flask import Blueprint,render_template,request,flash,jsonify
from Application.DBHandler import Mysqlhandler

auth = Blueprint('auth',__name__)

@auth.route('/home',methods=['GET','POST'])
def home():
     return "<p>Home Page</p>"


@auth.route('/login',methods=['GET','POST'])
def sign_in():
    return render_template("login.html")

@auth.route('/signup',methods=['GET','POST'])
def sign_up():
    return render_template("signup.html")