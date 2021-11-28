from Application.DBHandler import Mysqlhandler
from flask import Blueprint,render_template,request,flash

auth = Blueprint('auth',__name__)


@auth.route('/homepage',methods=['GET','POST'])
def homepage():
    result=Mysqlhandler.show_aptmnt(0,'9676611699')#need to be changed
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
    return render_template("home.html",result=result)



@auth.route('/updateInfo',methods=['GET','POST'])
def updateInfo():
    if request.method=="POST":
        FName = request.form.get('p_FName')
        LName = request.form.get('p_LName')
        Phno = request.form.get('Phno')
        print(FName)
        Mysqlhandler.update_user_info(0,FName,LName,Phno)
        return 'Success'
    return 'Failed'

@auth.route('/updateCredentials',methods=['GET','POST'])
def updateCredentials():
    if request.method=="POST":
        p_CurrentPassword = request.form.get('p_CurrentPassword')
        p_Newpassword = request.form.get('p_Newpassword')
        p_Confirmpassword = request.form.get('p_Confirmpassword')
        print(p_Confirmpassword)
        if p_Newpassword==p_Confirmpassword:
            Mysqlhandler.update_user_credentials(0,p_CurrentPassword,p_Newpassword)
        else:
            print("FAAAAAAAAILED")
        return 'Success'
    return 'Failed'




@auth.route('/Our specializations',methods=['GET','POST'])
def specialization():
    return render_template("spec.html")



@auth.route('/logout')
def logout():
    return "<p>Logout</p>"