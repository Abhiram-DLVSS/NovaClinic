from datetime import timedelta,date,datetime
from Application.DBHandler import User
from flask import Blueprint,render_template,request,flash,jsonify,redirect,session
views = Blueprint('views',__name__)
views.permanent_session_lifetime=timedelta(days=7)

# verify
@views.route('/verify',methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        phno=request.json['phno']
        password1=request.json['password1']
        val=User.verify(0,phno,password1)
        return jsonify({'val': val})

@views.route('/checknewphno',methods=['GET','POST'])
def checknewphno():
    if request.method == 'POST':
        phno=request.json['phno']
        val=User.check_new_phno(0,phno)
        return jsonify({'val': val})

@views.route('/getname',methods=['GET','POST'])
def getname():
    if request.method == 'POST':
        phno=request.json['phno']
        val=User.getName(0,phno)
        return jsonify({'val': val})

@views.route('/adduser',methods=['GET','POST'])
def adduser():
    if request.method == 'POST':
        phno=request.json['phno']
        password1=request.json['password1']
        firstname=request.json['firstname']
        lastname=request.json['lastname']
        dob=request.json['dob']
        gender=request.json['gender']
        User.add_user(0,firstname,lastname,dob,gender,phno,password1)
        return "success"

@views.route('/updateinfo',methods=['GET','POST'])
def updateinfo():
    if request.method == 'POST':
        phno=request.json['phno']
        FName=request.json['FName']
        LName=request.json['LName']
        NewPhno=request.json['NewPhno']
        User.update_info(0,FName,LName,NewPhno,phno)       
        return "success"

@views.route('/updatecredentials',methods=['GET','POST'])
def updatecredentials():
    if request.method == 'POST':
        phno=request.json['phno']
        CurrentPassword=request.json['CurrentPassword']
        Newpassword=request.json['Newpassword']
        val=User.update_credentials(0,CurrentPassword,Newpassword,phno)
        return jsonify({'val': val})

@views.route('/getuserdetails',methods=['GET','POST'])
def getuserdetails():
    if request.method == 'POST':
        phno=request.json['phno']
        val=User.getUserDetails(0,phno)
        year=val[0][2].year
        month=val[0][2].month
        day=val[0][2].day
        
        return jsonify({'val': val,'year': year,'month': month,'day': day})