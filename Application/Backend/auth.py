from Application.DBHandler import Mysqlhandler
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for

auth = Blueprint('auth',__name__)

@auth.route('/home',methods=['GET','POST'])
def home():        
    return "Welcome to Home page"


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':

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
            return redirect('/home')
    return render_template("login.html")

@auth.route('/signup',methods=['GET','POST'])
def user_info():
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
            return redirect('/home')

    return render_template("signup.html")
