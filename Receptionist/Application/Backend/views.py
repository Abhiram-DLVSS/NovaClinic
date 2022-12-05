from datetime import timedelta,date,datetime
from Application.DBHandler import Receptionist
from flask import Blueprint,render_template,request,flash,jsonify,redirect,session

views = Blueprint('views',__name__)
views.permanent_session_lifetime=timedelta(days=7)

@views.route('/verify',methods=['GET','POST'])
def verify():
    if request.method=="POST":
        recep_id=request.json['recep_id']
        password=request.json['password']
        val= Receptionist.verify(0,recep_id,password)
        return jsonify({'val': val})

@views.route('/getname',methods=['GET','POST'])
def getname():
    if request.method=="POST":
        recep_id=request.json['recep_id']
        val= Receptionist.getName(0,recep_id)
        return jsonify({'val': val})

@views.route('/showaptmnts',methods=['GET','POST'])
def showaptmnts():
    if request.method=="POST":
        date=request.json['date']
        speciality=request.json['speciality']
        identifier=request.json['identifier']
        todaysdate=request.json['todaysdate']
        val= Receptionist.show_aptmnts(0,date,speciality,identifier,todaysdate)
        return jsonify({'val': val})

@views.route('/updatecredentials',methods=['GET','POST'])
def updatecredentials():
    if request.method=="POST":
        CurrentPassword=request.json['CurrentPassword']
        Newpassword=request.json['Newpassword']
        recep_id=request.json['recep_id']
        val= Receptionist.update_credentials(0,CurrentPassword,Newpassword,recep_id)
        return jsonify({'val': val})