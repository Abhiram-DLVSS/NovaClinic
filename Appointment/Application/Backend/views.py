from datetime import timedelta,date,datetime
from Application.DBHandler import Appointment
from flask import Blueprint,render_template,request,flash,jsonify,redirect,session


views = Blueprint('views',__name__)
views.permanent_session_lifetime=timedelta(days=7)

@views.route('/showaptmnt',methods=['GET','POST'])
def showaptmnt():
    if request.method=="POST":
        phno=request.json['phno']
        todaysdate=date.today()
        Fname=request.json['Fname']
        Lname=request.json['Lname']
        val= Appointment.show_aptmnt(0,phno,todaysdate,Fname,Lname)
        return jsonify({'val': val})

@views.route('/deleteoldaptmnt',methods=['GET','POST'])
def deleteoldaptmnt():
    if request.method=="POST":
        todaysdate=date.today()
        Appointment.delete_old_aptmnt(0,todaysdate)
        return "success"

@views.route('/aptmntdoctors',methods=['GET','POST'])
def aptmntdoctors():
    if request.method=="POST":
        identifier=request.json['identifier']
        speciality=request.json['speciality']
        gender=request.json['gender']
        high=request.json['high']
        val=Appointment.aptmnt_doctors(0,identifier,speciality,gender,high)
        return jsonify({'val': val})

@views.route('/getslot',methods=['GET','POST'])
def getslot():
    if request.method=="POST":
        docID=request.json['docID']
        date=request.json['date']
        val=Appointment.getSlot(0,docID,date)
        return jsonify({'val': val})

@views.route('/addslot',methods=['GET','POST'])
def addslot():
    if request.method=="POST":
        docID=request.json['docID']
        date=request.json['date']
        val=Appointment.addSlot(0,docID,date)
        return jsonify({'val': val})


@views.route('/getslottimestring',methods=['GET','POST'])
def getslottimestring():
    if request.method=="POST":
        docID=request.json['docID']
        date=request.json['date']
        val=Appointment.getSlottimestring(0,docID,date)
        return jsonify({'val': val})

@views.route('/addtempuser',methods=['GET','POST'])
def addtempuser():
    if request.method=="POST":
        p_Fname=request.json['p_Fname']
        p_Lname=request.json['p_Lname']
        date=request.json['date']
        gender=request.json['gender']
        pphno=request.json['pphno']
        slot=request.json['slot']
        docID=request.json['docID']
        Appointment.addTempUser(0,p_Fname,p_Lname,date,gender,pphno,slot,docID)     
        return "success"

@views.route('/updateslot',methods=['GET','POST'])
def updateslot():
    if request.method=="POST":
        docID=request.json['docID']
        date=request.json['date']
        newtimestring=request.json['newtimestring']
        slotdictslot=request.json['slotdictslot']
        val=Appointment.updateSlot(0,newtimestring,slotdictslot,docID,date)
        return jsonify({'val': val})

@views.route('/insertaptmnt',methods=['GET','POST'])
def insertaptmnt():
    if request.method=="POST":
        docID=request.json['docID']
        date=request.json['date']
        phno=request.json['phno']
        slot=request.json['slot']
        Appointment.insertAptmnt(0,phno,docID,date,slot)
        return "success"

@views.route('/deleteaptmnt',methods=['GET','POST'])
def deleteaptmnt():
    if request.method=="POST":
        docID=request.json['docID']
        date=request.json['date']
        phno=request.json['phno']
        slot=request.json['slot']
        aptmnt_id=request.json['aptmnt_id']
        newtimestring=request.json['newtimestring']
        Appointment.delete_aptmnt(0,aptmnt_id,docID,date,newtimestring,phno,slot)
        return "success"