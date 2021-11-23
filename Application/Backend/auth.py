import re
from flask import Blueprint,render_template,request,flash
from Application.DBHandler import Mysqlhandler

auth = Blueprint('auth',__name__)


@auth.route('/homepage',methods=['GET','POST'])
def home_button():
    if request.method=="POST":
            name = request.form.get('name')
            docname = request.form.get('docname')
            spec = request.form.get('spec')
            message = request.form.get('message')
            if len(docname)<=0:
                flash('You forgot to fill the form completely.',category='error')
            elif len(name)<=0:
                flash('You forgot to fill the form completely.',category='error')
            elif len(spec)<=0:
                flash('You forgot to fill the form completely.',category='error')
            elif len(message)<=0:
             flash('You forgot to fill the form completely.',category='error')
            else:
                 #send user to the database            
                flash('Message Sent.',category='success')
                print(spec)
                Mysqlhandler.add_user(0,name,docname,spec,message)

    return render_template("home1.html")
    

@auth.route('/Our specializations',methods=['GET','POST'])
def specialization():
    return render_template("spec.html")



@auth.route('/logout')
def logout():
    return "<p>Logout</p>"