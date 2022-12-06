from datetime import timedelta,date,datetime
from Application.DBHandler import Admin
from flask import Blueprint,render_template,request,flash,jsonify,redirect,session

views = Blueprint('views',__name__)
views.permanent_session_lifetime=timedelta(days=7)
todaysdate=date.today()


@views.route('/verify',methods=['GET','POST'])
def verify():
    if request.method=="POST":
        admin_id=request.json['admin_id']
        password=request.json['password']
        val= Admin.verify(0,admin_id,password)
        return jsonify({'val': val})

@views.route('/getname',methods=['GET','POST'])
def getname():
    if request.method=="POST":
        admin_id=request.json['admin_id']
        val= Admin.getName(0,admin_id)
        return jsonify({'val': val})

@views.route('/showadmins',methods=['GET','POST'])
def showadmins():
    if request.method=="POST":
        val= Admin.showAdmins(0)
        return jsonify({'val': val})

@views.route('/showreceps',methods=['GET','POST'])
def showreceps():
    if request.method=="POST":
        val= Admin.showReceptionists(0)  
        return jsonify({'val': val})

@views.route('/chknewrecep',methods=['GET','POST'])
def chknewrecep():
    if request.method=="POST":
        id=request.json['id']
        val= Admin.check_new_recep_id(0,id)
        return jsonify({'val': val})

@views.route('/addrecep',methods=['GET','POST'])
def addrecep():
    if request.method=="POST":
        id=request.json['id']
        Fname=request.json['Fname']
        Lname=request.json['Lname']
        Admin.addReceptionist(0,id,Fname,Lname)
        return "success"

@views.route('/deleterecep',methods=['GET','POST'])
def deleterecep():
    if request.method=="POST":
        id=request.json['id']
        Admin.deleteReceptionist(0,id)
        return "success"

@views.route('/getrecep',methods=['GET','POST'])
def getrecep():
    if request.method=="POST":
        id=request.json['id']
        val=Admin.getReceptionist(0,id)
        return jsonify({'val': val})

@views.route('/updatecredentials',methods=['GET','POST'])
def updatecredentials():
    if request.method=="POST":
        CurrentPassword=request.json['CurrentPassword']
        Newpassword=request.json['Newpassword']
        admin_id=request.json['admin_id']
        val= Admin.update_credentials(0,CurrentPassword,Newpassword,admin_id)
        return jsonify({'val': val})


@views.route('/rverify',methods=['GET','POST'])
def rverify():
    if request.method=="POST":
        recep_id=request.json['recep_id']
        password=request.json['password']
        val= Admin.rverify(0,recep_id,password)
        return jsonify({'val': val})
        
@views.route('/rgetname',methods=['GET','POST'])
def rgetname():
    if request.method=="POST":
        recep_id=request.json['recep_id']
        val= Admin.rgetName(0,recep_id)
        return jsonify({'val': val})

@views.route('/rupdatecredentials',methods=['GET','POST'])
def rupdatecredentials():
    if request.method=="POST":
        CurrentPassword=request.json['CurrentPassword']
        Newpassword=request.json['Newpassword']
        recep_id=request.json['recep_id']
        val= Admin.rupdate_credentials(0,CurrentPassword,Newpassword,recep_id)
        return jsonify({'val': val})