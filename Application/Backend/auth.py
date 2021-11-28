from Application.DBHandler import Mysqlhandler
from flask import Blueprint, flash, jsonify, render_template, request

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    return "<p>Login</p>"

@auth.route('/home',methods=['GET','POST'])
def home():
    return "<p>Home</p>"

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    return "<p>Sign Up</p>"

@auth.route('/aptmnt',methods=['GET','POST'])
def aptmnt():
    if request.method=="POST":
        high = request.form.get('high')
        speciality = request.form.get('speciality')
        # print("chk")
        # print(high)
        # print(speciality)
        # print("chkend")
        
        print(request.form.get('book'))
        print("endend")
        if request.form.get('clear')=='clear':#if clear button is pressed
            high=None
            speciality=None

        if high=='high2low'and speciality==None:
            query="select * from doctors order by exp desc;"
            result=Mysqlhandler.show_doctors_as_requested(query)
            print(result)
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality)
        elif high=='low2high'and speciality==None:
            query="select * from doctors order by exp;"
            result=Mysqlhandler.show_doctors_as_requested(query)
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality)
        elif high==None and speciality!=None:
            query="select * from doctors where spec='"+speciality+"';"
            result=Mysqlhandler.show_doctors_as_requested(query)
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality)
        elif high=='high2low' and speciality!=None:
            query="select * from doctors where spec='"+speciality+"' order by exp desc;"
            result=Mysqlhandler.show_doctors_as_requested(query)
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality)
        elif high=='low2high' and speciality!=None:
            query="select * from doctors where spec='"+speciality+"' order by exp;"
            result=Mysqlhandler.show_doctors_as_requested(query)
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality)
        else:
            query="select * from doctors;"
            result=Mysqlhandler.show_doctors_as_requested(query)        
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality)

    else:
        query="select * from doctors;"
        result=Mysqlhandler.show_doctors_as_requested(query)        
        return render_template("aptmnt.html",result=result)
        

@auth.route('/process_qtc', methods=['POST', 'GET'])
def process_qt_calculation1():
    print("workin")
    if request.method == "POST":
        p_Lname = request.form.get('p_Lname')
        p_Fname = request.form.get('p_Fname')
        age = request.form.get('age')
        gender = request.form.get('gender')
        date = request.form.get('date')
        docName = request.form.get('docName')
        results={"p_Fname":p_Fname,"p_Lname":p_Lname,"age":age,"gender":gender,"date":date,"docName":docName}
        query="select * from slots where doctorid='{}' and date='{}';".format(docName,date)

        result=Mysqlhandler.show_doctors_as_requested(query)

        if not result:
            query="insert into slots values('{}','{}',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);".format(date,docName)
            Mysqlhandler.show_doctors_as_requested(query)
            

        query="select * from slots where doctorid='{}' and date='{}';".format(docName,date)
        result=Mysqlhandler.show_doctors_as_requested(query)
            
        if not result:#if result is empty
            print("Empty")
            return "Empty"
        else:
            for i in result:
                print(i[0])
            print(result[0][1])
            data={
                "date":result[0][0],
                "doctorid":result[0][1],
                "09:00-09:15":result[0][2],
                "09:15-09:30":result[0][3],
                "09:30-09:45":result[0][4],
                "09:45-10:00":result[0][5],
                "10:00-10:15":result[0][6],
                "10:15-10:30":result[0][7],
                "10:30-10:45":result[0][8],
                "10:45-11:00":result[0][9],
                "11:00-11:15":result[0][10],
                "11:15-11:30":result[0][11],
                "11:30-11:45":result[0][12],
                "11:45-12:00":result[0][13],
                "18:00-18:15":result[0][14],
                "18:15-18:30":result[0][15],
                "18:30-18:45":result[0][16],
                "18:45-19:00":result[0][17],
                "19:00-19:15":result[0][18],
                "19:15-19:30":result[0][19],
                "19:30-19:45":result[0][20],
                "19:45-20:00":result[0][21],
                "20:00-20:15":result[0][22],
                "20:15-20:30":result[0][23],
                "20:30-20:45":result[0][24],
                "20:45-21:00":result[0][25]
                }
        # data=[["date",result[0][0]],["doctorid",result[0][]]]
        # print("woah")
        # print(results)
        return data

@auth.route('/process_qtc2', methods=['POST', 'GET'])
def process_qt_calculation2():
    if request.method == "POST":
        if(request.form.get('flag')=="commit"):
            query="commit;"
            Mysqlhandler.show_doctors_as_requested(query)
            return "test"
        if(request.form.get('flag')=="rollback"):
            query="rollback;"
            Mysqlhandler.show_doctors_as_requested(query)
            return "test"
            
        p_Lname = request.form.get('p_Lname')
        p_Fname = request.form.get('p_Fname')
        age = request.form.get('age')
        gender = request.form.get('gender')
        date = request.form.get('date')
        docName = request.form.get('docName')
        slot = request.form.get('slot')
        results={"p_Fname":p_Fname,"p_Lname":p_Lname,"age":age,"gender":gender,"date":date,"docName":docName,"slot":slot}
        sqlslot=slot[0:2]+'$'+slot[3:5]+'_'+slot[6:8]+'$'+slot[9:11]
        query="update slots set {}=1 where doctorid='{}' and date='{}';".format(sqlslot,docName,date)
        Mysqlhandler.show_doctors_as_requested(query)
        
        query="insert into aptmnt(patientid,doctorid,date,slot) values('{}','{}','{}','{}');".format(p_Fname,docName,date,slot)
        Mysqlhandler.show_doctors_as_requested(query)
        return "Test"

@auth.route('/receptionist',methods=['GET','POST'])
def receptionist():
    query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.name,user_info.firstname,user_info.lastname,aptmnt.patientid,aptmnt.date,aptmnt.slot from aptmnt,doctors,user_info where aptmnt.doctorid=doctors.id and aptmnt.patientid=user_info.phno;"
    result=Mysqlhandler.show_doctors_as_requested(query) 
    if request.method=="POST":
        date = request.form.get('datePicker')
        speciality = request.form.get('speciality')

        if request.form.get('clear')=='clear':#if clear button is pressed
            date=None
            speciality=None
        
        # query="select * from doctors;"
        # result=Mysqlhandler.show_doctors_as_requested(query)        
        # return render_template("aptmnt.html",result=result)
        print(date)
        return render_template("receptionist.html",date=date,speciality=speciality,result=result)
    return render_template("receptionist.html",result=result)
