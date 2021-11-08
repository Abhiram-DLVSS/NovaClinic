from flask import Blueprint,render_template,request,flash,jsonify
from Application.DBHandler import Mysqlhandler

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    return "<p>Login</p>"

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

# @auth.route('/aptmnt/process_qtc', methods=['POST', 'GET'])
# def process_qt_calculation():
#     print("workig")
#     if request.method == "POST":
#         qtc_data = request.get_data()
#         print(qtc_data)
#     results = {'processed': 'true'}
#     return jsonify(results)

@auth.route('/process_qtc', methods=['POST', 'GET'])
def process_qt_calculation1():
    print("workin")
    if request.method == "POST":
        p_Lname = request.form.get('p_Lname')
        p_Fname = request.form.get('p_Fname')
        age = request.form.get('age')
        gender = request.form.get('gender')
        date = request.form.get('date')
        results={"p_Fname":p_Fname,"p_Lname":p_Lname,"age":age,"gender":gender,"date":date}
        print(results)
    return results
