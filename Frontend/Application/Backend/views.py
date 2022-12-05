from datetime import timedelta,date,datetime
from flask import Blueprint,render_template,request,flash,jsonify,redirect,session
import requests

views = Blueprint('views',__name__)
views.permanent_session_lifetime=timedelta(days=7)
todaysdate=date.today()

#Welcome Page
@views.route('/')
def welcome():
    if "phno" in session:
        return redirect('/home')
    elif "recep_id" in session:
        return redirect('/receptionist')
    elif "admin_id" in session:
        return redirect('/admin')
    return render_template("welcome.html")

#Users Login Page
@views.route('/login',methods=['GET','POST'])
def login():
    if "phno" in session:
        return redirect('/home')
    elif "recep_id" in session:
        return redirect('/receptionist')
    elif "admin_id" in session:
        return redirect('/admin')

    if request.method == 'POST':
        session.permanent=True
        phno = request.form.get('phno')
        password1 = request.form.get('password1')
        response = requests.post(url="http://localhost:8002/verify",json={'phno': phno,'password1':password1})
        val=response.json()['val']
        if val==0:
            flash('The Phone Number or Password is incorrect', category='error')
            return render_template("login.html")
        elif val==-1:    
            return render_template("login.html")
        else:
            session["phno"]=phno
            return redirect('/home')
    else:
        return render_template("login.html")

#Sign Up Page
@views.route('/signup',methods=['GET','POST'])
def user_info():
    if "phno" in session:
        return redirect('/home')
    elif "recep_id" in session:
        return redirect('/receptionist')
    elif "admin_id" in session:
        return redirect('/admin')
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname  = request.form.get('lastname')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        phno = request.form.get('phno')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        response = requests.post(url="http://localhost:8002/checknewphno",json={'phno': phno})
        if response.json()['val']!=1:
            flash('Given Phone Number is already associated with an account.', category='error')
        elif len(firstname) <=0 or len(lastname) <=0:
            flash('Please enter your details correctly', category='error')
        elif gender=='Gender' or gender==None or dob=='' or len(dob)!=10 or not phno.isnumeric():
            flash('Please enter your details correctly', category='error')
        elif len(phno) != 10:
            flash('Please check your Phone Number.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 6:
            flash('Password is too short(minimum is 6 characters)', category='error')
        else:
            requests.post(url="http://localhost:8002/adduser",json={'phno': phno,'firstname':firstname,'lastname':lastname,'dob':dob,'gender':gender,'password1':password1})
            session["phno"]=phno
            return redirect('/home')

    return render_template("signup.html")

 #Returns the Name of the User   
@views.route('/userName', methods=['POST', 'GET'])
def userName():    
    phno=session["phno"]
    response = requests.post(url="http://localhost:8002/getname",json={'phno': phno})
    result=response.json()['val']
    # result=User.getName(0,phno)
    data={
        "FName":result[0][0],
        "LName":result[0][1]}
    return data

#Home Page
@views.route('/home',methods=['GET','POST'])
def home():
    if "admin_id" in session:
        return redirect('/admin')
    elif "recep_id" in session:
        return redirect('/receptionist')
    elif "phno" in session:
        phno=session["phno"]
        response = requests.post(url="http://localhost:8002/getname",json={'phno': phno})
        name=response.json()['val']
        if name!=None and name:
            Fname=name[0][0]
            Lname=name[0][1]
        else:
            return redirect('/logout')
        response = requests.post(url="http://localhost:8005/showaptmnt",json={'phno': phno,'Fname':Fname,'Lname':Lname})
        result=response.json()['val']
        requests.post(url="http://localhost:8005/deleteoldaptmnt")
        # result=User.show_aptmnt(0,phno,todaysdate)
        # Appointment.delete_old_aptmnt(0,todaysdate)
    else:
        return redirect('/login')
    return render_template("home.html",result=result,phno=phno,Fname=Fname,Lname=Lname)

#Updates Users Information
@views.route('/updateInfo',methods=['GET','POST'])
def updateInfo():
    if request.method=="POST":
        phno=session["phno"]
        FName = request.form.get('p_FName')
        LName = request.form.get('p_LName')
        NewPhno = request.form.get('Phno')
        response = requests.post(url="http://localhost:8002/checknewphno",json={'phno': phno})
        if len(NewPhno)!=10 or len(FName)<=0 or len(LName)<=0:
            return 'failed'
        elif response.json()['val']!=1 and NewPhno!=phno:
            return 'failed1'
        else:
            response=requests.post(url="http://localhost:8002/updateinfo",json={'FName': FName,'LName': LName,'NewPhno': NewPhno,'phno': phno})       
            if NewPhno!=phno:    
                return 'success1'
            return 'success'        
    return 'failed'
    
#Appointment Page
@views.route('/aptmnt',methods=['GET','POST'])
def aptmnt():
    if "admin_id" in session:
        return redirect('/admin')
    elif "recep_id" in session:
        return redirect('/receptionist')
    elif "phno" in session:
        phno=session["phno"]
        response = requests.post(url="http://localhost:8002/getname",json={'phno': phno})
        name=response.json()['val']
        if name!=None and name:
            Fname=name[0][0]
            Lname=name[0][1]
        else:
            return redirect('/logout')
    else:
        return redirect('/login')
    if request.method=="POST":
        high = request.form.get('high')
        speciality = request.form.get('speciality')
        gender = request.form.get('gender')
        if request.form.get('clear')=='clear':#if clear button is pressed
            high=None
            speciality=None
            gender=None
        if high==None and speciality==None and gender==None:
            identifier=0
        elif high!=None and speciality==None and gender==None:
            identifier=1
        elif high==None and speciality!=None and gender==None:
            identifier=2
        elif high==None and speciality==None and gender!=None:
            identifier=3
        elif high!=None and speciality!=None and gender==None:
            identifier=4
        elif high==None and speciality!=None and gender!=None:
            identifier=5
        elif high!=None and speciality==None and gender!=None:
            identifier=6
        elif high!=None and speciality!=None and gender!=None:
            identifier=7
        
        response = requests.post(url="http://localhost:8005/aptmntdoctors",json={'identifier': identifier,'speciality':speciality,'gender':gender,'high':high})
        result=response.json()['val']
        # result=Appointment.aptmnt_doctors(0,identifier,speciality,gender,high)
        return render_template("aptmnt.html",result=result,high=high,speciality=speciality,phno=phno,gender=gender)
    else:
        response = requests.post(url="http://localhost:8005/aptmntdoctors",json={'identifier': 0,'speciality':None,'gender':None,'high':None})
        result=response.json()['val']
        # result=Appointment.aptmnt_doctors(0,0,None,None,None)      
        return render_template("aptmnt.html",result=result,phno=phno)

#Returns the availability of slots information on a Particular Day
@views.route('/getslotsinfo', methods=['POST', 'GET'])
def getslotsinfo():
    if request.method == "POST":
        date = request.form.get('date')
        docID = request.form.get('docID')
        response = requests.post(url="http://localhost:8005/getslot",json={'docID': docID,'date':date})
        result=response.json()['val']
        # result=Appointment.getSlot(0,docID,date)
        if not result:
            requests.post(url="http://localhost:8005/addslot",json={'docID': docID,'date':date})
            # Appointment.addSlot(0,docID,date)
        response = requests.post(url="http://localhost:8005/getslot",json={'docID': docID,'date':date})
        result=response.json()['val']
        if(str(date)==str(todaysdate)):
            now = datetime.now()
            current_time = now.strftime("%H%M")
            today_slot={"0859":0,"0914":1,"0929":2,"0944":3,"0959":4,"1014":5,"1029":6,"1044":7,"1059":8,"1114":9,"1129":10,"1144":11,"1759":12,"1814":13,"1829":14,"1844":15,"1859":16,"1914":17,"1929":18,"1944":19,"1959":20,"2014":21,"2029":22,"2044":23,"2044":24}
            timesup=24
            for a in today_slot:
                if(int(current_time)<int(a)):
                    timesup=today_slot[str(a)]
                    break
            res=''
            for x in range(timesup):
                res=res+'1'
            result=[(result[0][0],result[0][1],res+result[0][2][timesup:])]
        if not result:#if result is empty
            return "Empty"
        else:
            data={
                "date":result[0][0],
                "doctorid":result[0][1],
                "09:00-09:15":result[0][2][0],
                "09:15-09:30":result[0][2][1],
                "09:30-09:45":result[0][2][2],
                "09:45-10:00":result[0][2][3],
                "10:00-10:15":result[0][2][4],
                "10:15-10:30":result[0][2][5],
                "10:30-10:45":result[0][2][6],
                "10:45-11:00":result[0][2][7],
                "11:00-11:15":result[0][2][8],
                "11:15-11:30":result[0][2][9],
                "11:30-11:45":result[0][2][10],
                "11:45-12:00":result[0][2][11],
                "18:00-18:15":result[0][2][12],
                "18:15-18:30":result[0][2][13],
                "18:30-18:45":result[0][2][14],
                "18:45-19:00":result[0][2][15],
                "19:00-19:15":result[0][2][16],
                "19:15-19:30":result[0][2][17],
                "19:30-19:45":result[0][2][18],
                "19:45-20:00":result[0][2][19],
                "20:00-20:15":result[0][2][20],
                "20:15-20:30":result[0][2][21],
                "20:30-20:45":result[0][2][22],
                "20:45-21:00":result[0][2][23]
                }
        return data

#Adding the Appointment and updating the Slots data in the Database
@views.route('/confirmaptmnt', methods=['POST', 'GET'])
def confirmaptmnt():
    if "phno" in session:
        phno=session["phno"]
    if request.method == "POST":
        p_Lname = request.form.get('p_Lname')
        p_Fname = request.form.get('p_Fname')
        gender = request.form.get('gender')
        date = request.form.get('date')
        docID = request.form.get('docID')
        slot = request.form.get('slot')
        slot_dict={"09:00-09:15":0,"09:15-09:30":1,"09:30-09:45":2,"09:45-10:00":3,"10:00-10:15":4,"10:15-10:30":5,"10:30-10:45":6,"10:45-11:00":7,"11:00-11:15":8,"11:15-11:30":9,"11:30-11:45":10,"11:45-12:00":11,"18:00-18:15":12,"18:15-18:30":13,"18:30-18:45":14,"18:45-19:00":15,"19:00-19:15":16,"19:15-19:30":17,"19:30-19:45":18,"19:45-20:00":19,"20:00-20:15":20,"20:15-20:30":21,"20:30-20:45":22,"20:45-21:00":23}
        response = requests.post(url="http://localhost:8005/getslottimestring",json={'docID': docID,'date':date})
        timestring=response.json()['val']
        # timestring=Appointment.getSlottimestring(0,docID,date)
        newtimestring=timestring[0][0][0:slot_dict[slot]]+"1"+timestring[0][0][slot_dict[slot]+1:24]
        if "recep_id" in session:
            pphno=request.form.get('phno')
            
            response = requests.post(url="http://localhost:8002/checknewphno",json={'phno': pphno})
            print("chk1")
            if response.json()['val']!=0:
                requests.post(url="http://localhost:8005/addtempuser",json={'p_Fname': p_Fname,'p_Lname': p_Lname,'date': date,'gender': gender,'pphno': pphno,'slot': slot,'docID': docID})
                print("chk2")
                
                # Appointment.addTempUser(0,p_Fname,p_Lname,date,gender,pphno,slot,docID)         
            slotdictslot=slot_dict[slot]
            response = requests.post(url="http://localhost:8005/updateslot",json={'newtimestring': newtimestring,'slotdictslot':slotdictslot,'docID':docID,'date':date})
            slotchk=response.json()['val']
            # slotchk=Appointment.updateSlot(0,newtimestring,slotdictslot,docID,date)
            
            print("chk3")
            if slotchk==-1:
                print("chk4")
                return "failed1"
            
            print("chk5")
            requests.post(url="http://localhost:8005/insertaptmnt",json={'phno': pphno,'docID':docID,'date':date,'slot':slot})
            # Appointment.insertAptmnt(0,pphno,docID,date,slot)
            
            print("chk6")
            return "Success"
        else:
            slotdictslot=slot_dict[slot]
            response = requests.post(url="http://localhost:8005/updateslot",json={'newtimestring': newtimestring,'slotdictslot':slotdictslot,'docID':docID,'date':date})
            slotchk=response.json()['val']
            # slotchk=Appointment.updateSlot(0,newtimestring,slotdictslot,docID,date)
            if slotchk==-1:
                return "failed1"
            requests.post(url="http://localhost:8005/insertaptmnt",json={'phno': phno,'docID':docID,'date':date,'slot':slot})
            # Appointment.insertAptmnt(0,phno,docID,date,slot)
            return "Success"

#Deletes the Appointment
@views.route('/aptmntDelete', methods=['POST', 'GET'])
def aptmntDelete():
    if request.method == "POST":
        aptmnt_id = request.form.get('aptmnt_id')
        docID=request.form.get('docID')
        slot=request.form.get('slot')        
        date=request.form.get('date')
        phno=request.form.get('phno')
        slot_dict={"09:00-09:15":0,"09:15-09:30":1,"09:30-09:45":2,"09:45-10:00":3,"10:00-10:15":4,"10:15-10:30":5,"10:30-10:45":6,"10:45-11:00":7,"11:00-11:15":8,"11:15-11:30":9,"11:30-11:45":10,"11:45-12:00":11,"18:00-18:15":12,"18:15-18:30":13,"18:30-18:45":14,"18:45-19:00":15,"19:00-19:15":16,"19:15-19:30":17,"19:30-19:45":18,"19:45-20:00":19,"20:00-20:15":20,"20:15-20:30":21,"20:30-20:45":22,"20:45-21:00":23}
        response = requests.post(url="http://localhost:8005/getslottimestring",json={'docID': docID,'date':date})
        timestring=response.json()['val']
        # timestring=Appointment.getSlottimestring(0,docID,date)
        newtimestring=timestring[0][0][0:slot_dict[slot]]+"0"+timestring[0][0][slot_dict[slot]+1:24]
        
        requests.post(url="http://localhost:8005/deleteaptmnt",json={'aptmnt_id': aptmnt_id,'docID':docID,'newtimestring':newtimestring,'date':date,'phno':phno,'slot':slot})
        # Appointment.delete_aptmnt(0,aptmnt_id,docID,date,newtimestring,phno,slot)
        return "success"

#Receptionist Login
@views.route('/rlogin',methods=['GET','POST'])
def rlogin():
    if "recep_id" in session:
        return redirect('/receptionist')
    elif "phno" in session:
        return redirect('/home')
    elif "admin_id" in session:
        return redirect('/admin')
    if request.method == 'POST':
        session.permanent=True
        recep_id = request.form.get('recep_id')
        password = request.form.get('password')
        response = requests.post(url="http://localhost:8003/verify",json={'recep_id': recep_id,'password':password})
        val=response.json()['val']
        if val==-1:
            flash('Invalid Credentials. Please try again.', category='error')
            return render_template("rlogin.html")
        elif val==1:    
            flash('Incorrect Credentials. Please try again.', category='error')
            return render_template("rlogin.html")
        else:
            session["recep_id"]=recep_id
            return redirect('/receptionist')
    return render_template("rlogin.html")

#Receptionist Homepage
@views.route('/receptionist',methods=['GET','POST'])
def receptionist():
    
    if "phno" in session:
        return redirect('/home')
    elif "admin_id" in session:
        return redirect('/admin')
    elif "recep_id" in session:
        recep_id=session["recep_id"]
        
        response = requests.post(url="http://localhost:8003/getname",json={'recep_id': recep_id})
        name=response.json()['val']
        # name=Receptionist.getName(0,recep_id)
        if name!=None and name:
            Fname=name[0][0]
            Lname=name[0][1]
            # Appointment.delete_old_aptmnt(0,todaysdate)#FLAG
        else:
            return redirect('/logout')
    else:
        return redirect('/rlogin')

    if request.method=="POST":        
        date = request.form.get('datePicker')
        speciality = request.form.get('speciality')
        if date=='':
                date=None
        if request.form.get('clear')=='clear':#if clear button is pressed
            date=None
            speciality=None
        elif speciality==None and date==None:
            response = requests.post(url="http://localhost:8003/showaptmnts",json={'date': date,'speciality': speciality,'identifier': 0,'todaysdate': str(todaysdate)})
            result=response.json()['val']
            # result=Receptionist.show_aptmnts(0,date,speciality,0,todaysdate)
            return render_template("receptionist.html",date=date,speciality=speciality,result=result,Fname=Fname,Lname=Lname)
        
        elif speciality!=None and date==None:   
            response = requests.post(url="http://localhost:8003/showaptmnts",json={'date': date,'speciality': speciality,'identifier': 1,'todaysdate': str(todaysdate)})
            result=response.json()['val']        
            # result=Receptionist.show_aptmnts(0,date,speciality,1,todaysdate)
            return render_template("receptionist.html",date=date,speciality=speciality,result=result,Fname=Fname,Lname=Lname)
        elif speciality==None and date!=None:
            response = requests.post(url="http://localhost:8003/showaptmnts",json={'date': date,'speciality': speciality,'identifier': 2,'todaysdate': str(todaysdate)})
            result=response.json()['val']
            # result=Receptionist.show_aptmnts(0,date,speciality,2,todaysdate)
            return render_template("receptionist.html",date=date,speciality=speciality,result=result,Fname=Fname,Lname=Lname)
        elif speciality!=None and date!=None:
            response = requests.post(url="http://localhost:8003/showaptmnts",json={'date': date,'speciality': speciality,'identifier': 3,'todaysdate': str(todaysdate)})
            result=response.json()['val']
            # result=Receptionist.show_aptmnts(0,date,speciality,3,todaysdate)
            return render_template("receptionist.html",date=date,speciality=speciality,result=result,Fname=Fname,Lname=Lname)
        
    response = requests.post(url="http://localhost:8003/showaptmnts",json={'date': None,'speciality': None,'identifier': 0,'todaysdate': str(todaysdate)})
    result=response.json()['val']
    # result=Receptionist.show_aptmnts(0,None,None,0,todaysdate)
    return render_template("receptionist.html",date=None,speciality=None,result=result,Fname=Fname,Lname=Lname)

#Walk In Appointments
@views.route('/raptmnt',methods=['GET','POST'])
def raptmnt():
    if "admin_id" in session:
        return redirect('/admin')
    elif "phno" in session:
        return redirect('/home')
    elif "recep_id" in session:
        recep_id=session["recep_id"]
        response = requests.post(url="http://localhost:8003/getname",json={'recep_id': recep_id})
        name=response.json()['val']
        # name=Receptionist.getName(0,recep_id)
        if name!=None and name:
            Fname=name[0][0]
            Lname=name[0][1]
            # Appointment.delete_old_aptmnt(0,todaysdate)#FLAG
        else:
            return redirect('/logout')
    else:
        return redirect('/login')
    if request.method=="POST":
        high = request.form.get('high')
        speciality = request.form.get('speciality')
        gender = request.form.get('gender')
        if request.form.get('clear')=='clear':#If the clear button is pressed
            high=None
            speciality=None
            gender=None
        if high==None and speciality==None and gender==None:
            identifier=0
        elif high!=None and speciality==None and gender==None:
            identifier=1
        elif high==None and speciality!=None and gender==None:
            identifier=2
        elif high==None and speciality==None and gender!=None:
            identifier=3
        elif high!=None and speciality!=None and gender==None:
            identifier=4
        elif high==None and speciality!=None and gender!=None:
            identifier=5
        elif high!=None and speciality==None and gender!=None:
            identifier=6
        elif high!=None and speciality!=None and gender!=None:
            identifier=7
        
        response = requests.post(url="http://localhost:8005/aptmntdoctors",json={'identifier': identifier,'speciality': speciality,'gender': gender,'high': high})
        result=response.json()['val']
        # result=Appointment.aptmnt_doctors(0,identifier,speciality,gender,high)
        return render_template("raptmnt.html",result=result,high=high,speciality=speciality,gender=gender)
    else:
        response = requests.post(url="http://localhost:8005/aptmntdoctors",json={'identifier': 0,'speciality': None,'gender': None,'high': None})
        result=response.json()['val']
        # result=Appointment.aptmnt_doctors(0,0,None,None,None)        
        return render_template("raptmnt.html",result=result)

@views.route('/checkuser', methods=['POST', 'GET'])
def checkuser():
    if request.method == "POST":
        phno=request.form.get('phno')
        # print(User.check_new_phno(0,phno))
        response = requests.post(url="http://localhost:8002/checknewphno",json={'phno': phno})
        return str(response.json()['val'])+""

#Checks for the users existence
@views.route('/getuserinfo', methods=['POST', 'GET'])
def getuserinfo():
    if request.method == "POST":
        phno=request.form.get('phno')
        response = requests.post(url="http://localhost:8002/getuserdetails",json={'phno': phno})
        result=response.json()['val']
        # result=User.getUserDetails(0,phno)
        today = date.today()
        age = today.year - response.json()['year'] - ((today.month, today.day) < (response.json()['month'] , response.json()['day'] ))
        return {"Fname":result[0][0],"Lname":result[0][1],"Age":int(age),"Gender":result[0][3]}

#Admin Login Page
@views.route('/alogin',methods=['GET','POST'])
def alogin():
    if "admin_id" in session:
        admin_id=session["admin_id"]
        return redirect('/admin')
    elif "phno" in session:
        return redirect('/home')
    elif "recep_id" in session:
        return redirect('/receptionist')
    if request.method == 'POST':
        session.permanent=True
        admin_id = request.form.get('admin_id')
        password = request.form.get('password')
        response = requests.post(url="http://localhost:8004/verify",json={'admin_id': admin_id,'password':password})
        val=response.json()['val']
        # val=Admin.verify(0,admin_id,password)
        if val==-1:
            flash('Invalid Credentials. Please try again.', category='error')
            return render_template("alogin.html")
        elif val==1:    
            flash('Incorrect Credentials. Please try again.', category='error')
            return render_template("alogin.html")
        else:
            session["admin_id"]=admin_id
            return redirect('/admin')
    return render_template("alogin.html")

#Admin Homepage
@views.route('/admin',methods=['GET','POST'])
def admin():
    
    if "phno" in session:
        return redirect('/home')
    elif "recep_id" in session:
        return redirect('/receptionist')
    response = requests.post(url="http://localhost:8004/showdoctors")
    docids=response.json()['val']
    # docids=Admin.showDoctors(0)
    response = requests.post(url="http://localhost:8004/showreceps")
    recepids=response.json()['val']
    # recepids=Admin.showReceptionists(0)    
    response = requests.post(url="http://localhost:8004/showadmins")
    adminids=response.json()['val']
    # adminids=Admin.showAdmins(0)
    if "admin_id" in session:
        admin_id=session["admin_id"]
        
        response = requests.post(url="http://localhost:8004/getname",json={'admin_id': admin_id})
        name=response.json()['val']
        # name=Admin.getName(0,admin_id)
        if name!=None and name:
            Fname=name[0][0]
            Lname=name[0][1]
        else:
            return redirect('/logout')
    else:
        return redirect('/alogin')
        
    return render_template("admin.html",docids=docids,recepids=recepids,adminids=adminids,Fname=Fname,Lname=Lname)

#To Add Doctor
@views.route('/addDoctor', methods=['POST', 'GET'])
def addDoctor():
    if request.method == "POST":
            
        Lname = request.form.get('Lname')
        Fname = request.form.get('Fname')
        spec = request.form.get('spec')
        gender = request.form.get('gender')
        id = request.form.get('id')
        exp = request.form.get('exp')
        edu = request.form.get('edu')
        response = requests.post(url="http://localhost:8004/checknewdocid",json={'id': id})
        chkid=response.json()['val']
        if len(Lname)==0 or len(Fname)==0 or len(spec)==0 or gender=='Gender' or len(id)==0 or len(edu)==0:
            return 'failed'
        elif chkid!=1:
            return 'failed1'
        else:
            requests.post(url="http://localhost:8004/adddoc",json={'id': id,'Fname': Fname,'Lname': Lname,'spec': spec,'exp': exp,'gender': gender,'edu': edu})
            # Admin.addDoc(0,id,Fname,Lname,spec,exp,gender,edu)
            return 'success'

#To Update Doctor information
@views.route('/updateDoctor', methods=['POST', 'GET'])
def updateDoctor():
    if "admin_id" in session:
        admin_id=session["admin_id"]
    if request.method == "POST":
        flag= request.form.get('flag')
        if flag=='get':
            id = request.form.get('id')
            response = requests.post(url="http://localhost:8004/getdoc",json={'id': id})
            result=response.json()['val']
            # result=Admin.getDoctor(0,id)
            return jsonify(result)
        elif flag=='update':
            Lname = request.form.get('Lname')
            Fname = request.form.get('Fname')
            spec = request.form.get('spec')
            gender = request.form.get('gender')
            id = request.form.get('id')
            exp = request.form.get('exp')
            edu = request.form.get('edu')
            if len(Lname)==0 or len(Fname)==0 or len(spec)==0 or gender=='Gender' or len(id)==0 or len(edu)==0:
                return 'failed'
            else:
                requests.post(url="http://localhost:8004/updatedoc",json={'id': id,'Fname': Fname,'Lname': Lname,'spec': spec,'exp': exp,'gender': gender,'edu': edu})
                # Admin.updateDoc(0,id,Fname,Lname,spec,exp,gender,edu)
                return 'success'

#To delete Doctor
@views.route('/deleteDoctor', methods=['POST', 'GET'])
def deleteDoctor():
    if request.method == "POST":
        flag= request.form.get('flag')
        if flag=='get':
            id = request.form.get('id')
            response = requests.post(url="http://localhost:8004/getdoc",json={'id': id})
            result=response.json()['val']
            # result=Admin.getDoctor(0,id)
            return jsonify(result)
        elif flag=='delete':
            id = request.form.get('id')
            response = requests.post(url="http://localhost:8004/deletedoc",json={'id': id})
            # Admin.deleteDoc(0,id)
            return 'success'

#To add Receptionist
@views.route('/addReceptionist', methods=['POST', 'GET'])
def addReceptionist():
    if request.method == "POST":
        Lname = request.form.get('Lname')
        Fname = request.form.get('Fname')
        id = request.form.get('id')
        response = requests.post(url="http://localhost:8004/chknewrecep",json={'id': id})
        chkrecep=response.json()['val']
        if len(Lname)==0 or len(Fname)==0 or len(id)==0:
            return 'failed'
        elif chkrecep!=1:
            return 'failed1'
        else:
            requests.post(url="http://localhost:8004/addrecep",json={'id': id,'Fname': Fname,'Lname': Lname})
            # Admin.addReceptionist(0,id,Fname,Lname)
            return 'success'

#To delete Receptionist
@views.route('/deleteReceptionist', methods=['POST', 'GET'])
def deleteReceptionist():
    if request.method == "POST":
        flag= request.form.get('flag')
        if flag=='get':
            id = request.form.get('id')
            response=requests.post(url="http://localhost:8004/getrecep",json={'id': id})
            result=response.json()['val']
            return jsonify(result)
        elif flag=='delete':
            id = request.form.get('id')
            requests.post(url="http://localhost:8004/deleterecep",json={'id': id})
            # Admin.deleteReceptionist(0,id)
            return 'success'

#To Update the Credentials
@views.route('/updateCredentials',methods=['GET','POST'])
def updateCredentials():
    if request.method=="POST":
        CurrentPassword = request.form.get('CurrentPassword')
        Newpassword = request.form.get('Newpassword')
        Confirmpassword = request.form.get('Confirmpassword')
        if Newpassword!=Confirmpassword:
            return 'failed1'
        elif len(Newpassword)<6:
            return 'failed2'
        else:
            if "phno" in session:
                phno=session["phno"]
                response = requests.post(url="http://localhost:8002/updatecredentials",json={'CurrentPassword': CurrentPassword,'Newpassword': Newpassword,'phno': phno})
                if response.json()['val']==-1:
                    return 'failed'
                else:
                    return 'success'
            elif "admin_id" in session:
                admin_id=session["admin_id"]
                response = requests.post(url="http://localhost:8004/updatecredentials",json={'CurrentPassword': CurrentPassword,'Newpassword': Newpassword,'admin_id': admin_id})
                if response.json()['val']==-1:
                    return 'failed'
                else:
                    return 'success'
            elif "recep_id" in session:
                recep_id=session["recep_id"]
                response = requests.post(url="http://localhost:8003/updatecredentials",json={'CurrentPassword': CurrentPassword,'Newpassword': Newpassword,'recep_id': recep_id})
                if response.json()['val']==-1:
                    return 'failed'
                else:
                    return 'success'

#Logout 
@views.route('/logout')
def logout():
    if "phno" in session:
        session.pop("phno",None)
    elif "recep_id" in session:
        session.pop("recep_id",None)
    elif "admin_id" in session:
        session.pop("admin_id",None)
    return redirect('/')

