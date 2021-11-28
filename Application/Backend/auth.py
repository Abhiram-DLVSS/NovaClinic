from datetime import timedelta
from Application.DBHandler import Mysqlhandler
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for,session


auth = Blueprint('auth',__name__)
# auth.secret_key="secretKEY"
auth.permanent_session_lifetime=timedelta(days=14)



@auth.route('/aptmnt',methods=['GET','POST'])
def aptmnt():
    if "phno" in session:
        phno=session["phno"]
        result=Mysqlhandler.show_aptmnt(0,phno)#need to be changed
    else:
        return redirect('/login')
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
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality,phno=phno)
        elif high=='low2high'and speciality==None:
            query="select * from doctors order by exp;"
            result=Mysqlhandler.show_doctors_as_requested(query)
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality,phno=phno)
        elif high==None and speciality!=None:
            query="select * from doctors where spec='"+speciality+"';"
            result=Mysqlhandler.show_doctors_as_requested(query)
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality,phno=phno)
        elif high=='high2low' and speciality!=None:
            query="select * from doctors where spec='"+speciality+"' order by exp desc;"
            result=Mysqlhandler.show_doctors_as_requested(query)
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality,phno=phno)
        elif high=='low2high' and speciality!=None:
            query="select * from doctors where spec='"+speciality+"' order by exp;"
            result=Mysqlhandler.show_doctors_as_requested(query)
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality,phno=phno)
        else:
            query="select * from doctors;"
            result=Mysqlhandler.show_doctors_as_requested(query)        
            return render_template("aptmnt.html",result=result,high=high,speciality=speciality,phno=phno)

    else:
        query="select * from doctors;"
        result=Mysqlhandler.show_doctors_as_requested(query)        
        return render_template("aptmnt.html",result=result,phno=phno)
        

@auth.route('/process_qtc', methods=['POST', 'GET'])
def process_qt_calculation1():
    print("workin")
    phno=session["phno"]
    if request.method == "POST":
        p_Lname = request.form.get('p_Lname')
        p_Fname = request.form.get('p_Fname')
        age = request.form.get('age')
        gender = request.form.get('gender')
        date = request.form.get('date')
        docID = request.form.get('docID')
        results={"p_Fname":p_Fname,"p_Lname":p_Lname,"age":age,"gender":gender,"date":date,"docID":docID}
        query="select * from slots where doctorid='{}' and date='{}';".format(docID,date)

        result=Mysqlhandler.show_doctors_as_requested(query)

        if not result:
            query="insert into slots values('{}','{}',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);".format(date,docID)
            Mysqlhandler.show_doctors_as_requested(query)
            

        query="select * from slots where doctorid='{}' and date='{}';".format(docID,date)
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
    phno=session["phno"]
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
        docID = request.form.get('docID')
        slot = request.form.get('slot')
        results={"p_Fname":p_Fname,"p_Lname":p_Lname,"age":age,"gender":gender,"date":date,"docID":docID,"slot":slot}
        sqlslot=slot[0:2]+'$'+slot[3:5]+'_'+slot[6:8]+'$'+slot[9:11]
        query="update slots set {}=1 where doctorid='{}' and date='{}';".format(sqlslot,docID,date)
        Mysqlhandler.show_doctors_as_requested(query)
        
        query="insert into aptmnt(patientid,doctorid,date,slot) values('{}','{}','{}','{}');".format(phno,docID,date,slot)
        Mysqlhandler.show_doctors_as_requested(query)
        return "Test"
@auth.route('/userName', methods=['POST', 'GET'])
def userName():    
    phno=session["phno"]
    query="select firstname,lastname from user_info where phno='{}';".format(phno)
    result=Mysqlhandler.show_doctors_as_requested(query)
    # print(result[0][0])
    data={
                "FName":result[0][0],
                "LName":result[0][1]}
    return data


@auth.route('/receptionist',methods=['GET','POST'])
def receptionist():
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
        query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.name,user_info.firstname,user_info.lastname,aptmnt.patientid,aptmnt.date,aptmnt.slot from aptmnt,doctors,user_info where aptmnt.doctorid=doctors.id and aptmnt.patientid=user_info.phno;"
        result=Mysqlhandler.show_doctors_as_requested(query) 
        return render_template("receptionist.html",date=date,speciality=speciality,result=result)
    query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.name,user_info.firstname,user_info.lastname,aptmnt.patientid,aptmnt.date,aptmnt.slot from aptmnt,doctors,user_info where aptmnt.doctorid=doctors.id and aptmnt.patientid=user_info.phno;"
    result=Mysqlhandler.show_doctors_as_requested(query) 
    return render_template("receptionist.html",result=result)


@auth.route('/logout')
def logout():
    session.pop("phno",None)
    return redirect('/login')

@auth.route('/login',methods=['GET','POST'])
def login():
    if "phno" in session:
        phno=session["phno"]
        return redirect('/homepage')
    if request.method == 'POST':
        session.permanent=True
        phno = request.form.get('phno')
        password1 = request.form.get('password1')
        # print("phno="+phno)
        # print("password="+password1)
        
        val=Mysqlhandler.check_user(0,phno,password1)
        print("Val=")
        print(val)
        if val==0:
            flash('The Phone Number or Password you entered is incorrect', category='error')
            return render_template("login.html")
        elif val==-1:    
            return render_template("login.html")
        else:
            session["phno"]=phno
            return redirect('/homepage')
    else:
        if "phno" in session:
            phno=session["phno"]
            return redirect('/homepage')
        else:
            return render_template("login.html")

@auth.route('/signup',methods=['GET','POST'])
def user_info():
    if "phno" in session:
        phno=session["phno"]
        return redirect('/homepage')
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname  = request.form.get('lastname')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        phno = request.form.get('phno')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print("signup")
        print(firstname)
        print(lastname)
        print(dob)
        print(gender)
        print(phno)
        print(password1)
        print(password2)
        if Mysqlhandler.check_new_phno(0,phno)!=1:
            flash('An account already exists with the given phone number', category='error')
        elif len(firstname) <=0:
            flash('Please enter your details correctly', category='error')
        elif len(lastname) <=0:
            flash('Please enter your details correctly', category='error')
        elif gender=='Gender':
            flash('Please enter your details correctly', category='error')
        elif len(phno) != 10:
            flash('Please check your Phone Number.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 6:
            flash('Password is too short(minimum is 6 characters)', category='error')
        else:
            # flash('Account Created!', category='success')
            Mysqlhandler.add_user_info(0,firstname,lastname,dob,gender,phno)
            Mysqlhandler.add_user_credentials(0,phno,password1)
            session["phno"]=phno
            return redirect('/homepage')

    return render_template("signup.html")



@auth.route('/homepage',methods=['GET','POST'])
def homepage():
    if "phno" in session:
        phno=session["phno"]
        result=Mysqlhandler.show_aptmnt(0,phno)#need to be changed
        name=Mysqlhandler.getName(0,phno)
        print("Name=")
        print(name)
        if name!=None:
            Fname=name[0][0]
            Lname=name[0][1]
    else:
        return redirect('/login')
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
                Mysqlhandler.add_greviance(0,name,docname,spec,message)
    return render_template("home.html",result=result,phno=phno,Fname=Fname,Lname=Lname)



@auth.route('/updateInfo',methods=['GET','POST'])
def updateInfo():
    if request.method=="POST":
        phno=session["phno"]
        FName = request.form.get('p_FName')
        LName = request.form.get('p_LName')
        NewPhno = request.form.get('Phno')
        if len(NewPhno)!=10 or len(FName)<=0 or len(LName)<=0:
            return 'failed'
        elif Mysqlhandler.check_new_phno(0,NewPhno)!=1 and NewPhno!=phno:
            return 'failed1'
        else:
            # print(FName)
            Mysqlhandler.update_user_info(0,FName,LName,NewPhno,phno)
            return 'success'


        
    return 'failed'

@auth.route('/updateCredentials',methods=['GET','POST'])
def updateCredentials():
    if request.method=="POST":        
        phno=session["phno"]
        p_CurrentPassword = request.form.get('p_CurrentPassword')
        p_Newpassword = request.form.get('p_Newpassword')
        p_Confirmpassword = request.form.get('p_Confirmpassword')
        print(p_Confirmpassword)
        if p_Newpassword!=p_Confirmpassword:
            return 'failed1'
        elif len(p_Newpassword)<6:
            return 'failed2'
        else:
            if Mysqlhandler.update_user_credentials(0,p_CurrentPassword,p_Newpassword,phno)==-1:
                return 'failed'
            else:
                return 'success'