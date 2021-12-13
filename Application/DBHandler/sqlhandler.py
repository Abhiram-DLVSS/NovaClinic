import mysql.connector
import os

DB_URL = os.environ.get('CLEARDB_DATABASE_URL')
DBhost=DB_URL[32:59]
DBuser=DB_URL[8:22]
DBpassword=DB_URL[23:31]
DBname=DB_URL[60:82]

# DBhost='localhost'
# DBuser='root'
# DBpassword='YOUR_MySQL_PASSWORD'
# DBname='nova'


class User:
	
	def __init__(self):
		pass

	#Verify the given User Credentials
	def verify(self,phno,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select phno from users where phno='{}' and password=Sha2('{}',224);").format(phno,password)
		if(phno==None and password==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		#If the credentials are correct return 1 else 0
		if(len(vari)!=0):
			return 1
		else:
			return 0

	#Check whether the sign up Phone number is new
	def check_new_phno(self,phno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select phno from users where phno='{}';").format(phno)
		if(phno==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		#If the account with the same number already exists return 0 else 1
		if(len(vari)==0):			
			return 1
		else:		
			return 0
	
	#Register User
	def add_user(self,FName,LName,dob,gender,phno,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into users values('{}',Sha2('{}',224),'{}','{}','{}','{}');").format(phno,password,FName,LName,dob,gender)
		cursor.execute(query)
		cursor.execute("commit")
	
	#Update the User Information
	def update_info(self,FName,LName,NewPhno,OldPhno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="UPDATE users SET FName='{}',LName='{}',phno='{}' where phno='{}';".format(FName,LName,NewPhno,OldPhno)
		cursor.execute(query)	
		query="UPDATE aptmnt SET patient_id='{}' where patient_id='{}';".format(NewPhno,OldPhno)
		cursor.execute(query)
		cursor.execute("commit")
	
	#Update the credentials of the User
	def update_credentials(self,p_CurrentPassword,p_Newpassword,phno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()		
		query="select phno from users where password=Sha2('{}',224) and phno='{}'".format(p_CurrentPassword,phno)
		cursor.execute(query)		
		vari=cursor.fetchall()
		if(len(vari)==0):
			return -1
		query="UPDATE users SET password=Sha2('{}',224) where phno='{}' and password=Sha2('{}',224);".format(p_Newpassword,phno,p_CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0
	
	#Show Upcoming Appointments for the user
	def show_aptmnt(self,patient_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,users.FName,users.LName,doctors.doctor_specialization,aptmnt.date,aptmnt.slot from aptmnt,doctors,users where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=users.phno and aptmnt.patient_id='{}' order by aptmnt.date,aptmnt.slot;".format(patient_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	#Name of the User
	def getName(self,patient_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select FName, LName from users where phno='{}';".format(patient_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows	

class Appointment:
	
	def __init__(self):
		pass
	
	#Show the list of Doctors with their information
	def aptmnt_doctors(self,identifier,spec,gender,order):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		if identifier==0:
			query = "select * from doctors;"
		elif identifier==1:
			query = "select * from doctors order by doctor_experience {};".format(order)
		elif identifier==2:			
			query = "select * from doctors where doctor_specialization='{}';".format(spec)
		elif identifier==3:
			query = "select * from doctors where gender='{}';".format(gender)
		elif identifier==4:
			query = "select * from doctors where doctor_specialization='{}' order by doctor_experience {};".format(spec,order)
		elif identifier==5:
			query = "select * from doctors where gender='{}' and doctor_specialization='{}';".format(gender,spec)
		elif identifier==6:
			query = "select * from doctors where gender='{}' order by doctor_experience {};".format(gender,order)
		elif identifier==7:
			query = "select * from doctors where gender='{}' and doctor_specialization='{}' order by doctor_experience {};".format(gender,spec,order)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	#Data of a Doctors slots on a choosen date
	def getSlot(self,docID,date):		
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select date,doctor_id,time from slots where doctor_id='{}' and date='{}';".format(docID,date)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	#Time String in Slots Table - Availability
	def getSlottimestring(self,docID,date):		
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select time from slots where doctor_id='{}' and date='{}';".format(docID,date)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	#If the slot isn't present, add the slot
	def addSlot(self,docID,date):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into slots values('{}','{}','000000000000000000000000');".format(date,docID)
		cursor.execute(query)
		cursor.execute("commit")
		
	#Upon confirming an Appointment update the slot
	def updateSlot(self,time,index,docID,date):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select time from slots where doctor_id='{}' and date='{}';".format(docID,date)
		cursor.execute(query)
		rows=cursor.fetchall()
		chk=rows[0][0][index]
		if chk=="1":
			return -1
		else:
			query="update slots set time='{}' where doctor_id='{}' and date='{}';".format(time,docID,date)
			cursor.execute(query)
			cursor.execute("commit")
			return 0
	
	#Confirming the Appointment
	def insertAptmnt(self,phno,docID,date,slot):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into aptmnt(patient_id,doctor_id,date,slot) values('{}','{}','{}','{}');".format(phno,docID,date,slot)
		cursor.execute(query)
		cursor.execute("commit")
	
	#Walk In Appointment Users(Patients)
	def addTempUser(self,p_Fname,p_Lname,date,gender,phno,slot):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into temp_users(FName,LName,dob,gender,phno,slot,date) values('{}','{}','{}','{}','{}','{}','{}');".format(p_Fname,p_Lname,date,gender,phno,slot,date)
		cursor.execute(query)
		cursor.execute("commit")	
	
	#Delete all old Appointments
	def delete_old_aptmnt(self,date):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="delete from aptmnt where date<'{}';".format(date)
		cursor.execute(query)
		query="delete from slots where date<'{}';".format(date)
		cursor.execute(query)
		query="delete from temp_users where date<'{}';".format(date)
		cursor.execute(query)
		cursor.execute("commit")
	
	#Cancel Appointment
	def delete_aptmnt(self,aptmnt_id,docID,date,time):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="delete from aptmnt where aptmnt_id='{}';".format(aptmnt_id)
		cursor.execute(query)
		query="update slots set time='{}' where doctor_id='{}' and date='{}';".format(time,docID,date)
		cursor.execute(query)
		cursor.execute("commit")

class Receptionist:
	
	def __init__(self):
		pass

	#Verify the given Receptionist Credentials
	def verify(self,recep_id,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from receptionists where recep_id='{}' and password=Sha2('{}',224);").format(recep_id,password)
		if(recep_id=='' or password==''):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()		
		#If the account exists return 0 else 1
		if(len(vari)==0):
			return 1
		else:
			return 0
	
	#Name of the Receptionist
	def getName(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select FName, LName from receptionists where recep_id='{}';".format(recep_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	#Show Upcoming Appointments for the Receptionist
	def show_aptmnts(self,date,speciality,identifier):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		if identifier==0:
			query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,doctors.doctor_specialization,users.FName,users.LName,aptmnt.patient_id,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select FName,LName,phno from users union select FName,LName,phno from temp_users) as users where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=users.phno order by aptmnt.date,aptmnt.slot"
		elif identifier==1:
			query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,doctors.doctor_specialization,users.FName,users.LName,aptmnt.patient_id,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select FName,LName,phno from users union select FName,LName,phno from temp_users) as users where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=users.phno and doctors.doctor_specialization='{}' order by aptmnt.date,aptmnt.slot;".format(speciality)
		elif identifier==2:
			query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,doctors.doctor_specialization,users.FName,users.LName,aptmnt.patient_id,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select FName,LName,phno from users union select FName,LName,phno from temp_users) as users where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=users.phno and aptmnt.date='{}' order by aptmnt.date,aptmnt.slot;".format(date)
		elif identifier==3:
			query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,doctors.doctor_specialization,users.FName,users.LName,aptmnt.patient_id,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select FName,LName,phno from users union select FName,LName,phno from temp_users) as users where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=users.phno and aptmnt.date='{}' and doctors.doctor_specialization='{}' order by aptmnt.date,aptmnt.slot;".format(date,speciality)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	#Update the credentials of the Receptionist
	def update_credentials(self,CurrentPassword,Newpassword,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()			
		
		query="select * from receptionists where password=Sha2('{}',224) and recep_id='{}'".format(CurrentPassword,recep_id)
		cursor.execute(query)		
		vari=cursor.fetchall()
		#If Entered password is incorrect
		if(len(vari)==0):
			return -1
		query="UPDATE receptionists SET password=Sha2('{}',224) where recep_id='{}' and password=Sha2('{}',224);".format(Newpassword,recep_id,CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0

class Admin:
	
	def __init__(self):
		pass

	#Verify the given Admin Credentials
	def verify(self,admin_id,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from admin where admin_id='{}' and password=Sha2('{}',224);").format(admin_id,password)
		if(admin_id=='' or password==''):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):
			return 1
		else:
			return 0

	#Name of the Admin
	def getName(self,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select FName, LName from admin where admin_id='{}';".format(admin_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	#Verify whether the given Doctor ID is unique or not
	def check_new_docid(self,doctor_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from doctors where doctor_id='{}';".format(doctor_id)
		if(doctor_id==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		#If a doctor with the same ID already exists return 0 else 1
		if(len(vari)==0):
			return 1
		else:
			return 0
	
	#Verify whether the given Receptionist ID is unique or not
	def check_new_recep_id(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from receptionists where recep_id='{}';".format(recep_id)
		if(recep_id==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		#If a Receptionist with the same ID already exists return 0 else 1
		if(len(vari)==0):
			return 1
		else:
			return 0
	
	#Add a New Doctor
	def addDoc(self,doctor_id,Fname,Lname,spec,exp,gender,edu):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into doctors values('{}','{}','{}','{}','{}','{}','{}','{}');").format(doctor_id,Fname,Lname,spec,exp,gender,edu,"Doctor"+gender)
		cursor.execute(query)
		cursor.execute("commit")

	#Update the information of a Doctor
	def updateDoc(self,doctor_id,Fname,Lname,spec,exp,gender,edu):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("update doctors set FName='{}',LName='{}',doctor_specialization='{}',doctor_experience='{}',gender='{}',doctor_education='{}' where doctor_id='{}';").format(Fname,Lname,spec,exp,gender,edu,doctor_id)
		cursor.execute(query)
		cursor.execute("commit")

	#Delete a Doctor
	def deleteDoc(self,doctorID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "delete from doctors where doctor_id='{}';".format(doctorID)
		cursor.execute(query)
		cursor.execute("commit")

	#Add a new Receptionist
	def addReceptionist(self,recep_id,Fname,Lname):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into receptionists(recep_id,FName,LName) values('{}','{}','{}');").format(recep_id,Fname,Lname)
		cursor.execute(query)
		cursor.execute("commit")

	#Delete a Receptionist
	def deleteReceptionist(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "delete from receptionists where recep_id='{}';".format(recep_id)
		cursor.execute(query)
		cursor.execute("commit")

	#Update the credentials of the Admin
	def update_credentials(self,CurrentPassword,Newpassword,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select * from admin where password=Sha2('{}',224) and admin_id='{}'".format(CurrentPassword,admin_id)
		cursor.execute(query)		
		vari=cursor.fetchall()
		#If entered password is incorrect
		if(len(vari)==0):	
			return -1
		query="UPDATE admin SET password=Sha2('{}',224) where admin_id='{}' and password=Sha2('{}',224);".format(Newpassword,admin_id,CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0

	#Returns the Information about a Doctor to autofill delete and update Doctor modals
	def getDoctor(self,doctorID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from doctors where doctor_id='{}';".format(doctorID)
		cursor.execute(query)
		row=cursor.fetchall()
		return row	

	#Returns the Information about a Receptionist to autofill delete Receptionist modal
	def getReceptionist(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from receptionists where recep_id='{}';".format(recep_id)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	#Returns ID,Name of the Receptionist
	def showReceptionists(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select recep_id,FName,LName from receptionists;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	#Returns ID,Name of the Admin
	def showAdmins(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select admin_id,FName,LName from admin;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	#Returns ID,Name and Specialization of the Doctor
	def showDoctors(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select doctor_id,FName,LName,doctor_specialization from doctors;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows