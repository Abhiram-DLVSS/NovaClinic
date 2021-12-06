import mysql.connector
import os

DB_URL = os.environ.get('CLEARDB_DATABASE_URL')
DBhost=DB_URL[32:59]
DBuser=DB_URL[8:22]
DBpassword=DB_URL[23:31]
DBname=DB_URL[60:82]

class User:
	
	def __init__(self):
		pass

	def verify(self,phno,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from user_credentials where phno='{}' and password=Sha2('{}',224);").format(phno,password)
		if(phno==None and password==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)!=0):
			return 1
		else:
			return 0

	def check_new_phno(self,phno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from user_credentials where phno='{}';").format(phno)
		if(phno==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):# Account doesn't exist			
			return 1
		else:			 # Account already exists			
			return 0

	def add_info(self,FName,LName,dob,gender,phno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into user_info values('{}','{}','{}','{}','{}');").format(FName,LName,dob,gender,phno)
		cursor.execute(query)
		cursor.execute("commit")
	
	def add_credentials(self,phno,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into user_credentials values('{}',Sha2('{}',224));").format(phno,password)
		cursor.execute(query)
		cursor.execute("commit")
		
	def update_info(self,FName,LName,NewPhno,OldPhno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="UPDATE user_info SET FName='{}',LName='{}',phno='{}' where phno='{}';".format(FName,LName,NewPhno,OldPhno)
		cursor.execute(query)
		query="UPDATE user_credentials SET phno='{}' where phno='{}';".format(NewPhno,OldPhno)
		cursor.execute(query)		
		query="UPDATE aptmnt SET patient_id='{}' where patient_id='{}';".format(NewPhno,OldPhno)
		cursor.execute(query)
		cursor.execute("commit")
  
	def update_credentials(self,p_CurrentPassword,p_Newpassword,phno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()		
		query="select * from user_credentials where password=Sha2('{}',224) and phno='{}'".format(p_CurrentPassword,phno)
		cursor.execute(query)		
		vari=cursor.fetchall()
		if(len(vari)==0):
			return -1
		query="UPDATE user_credentials SET password=Sha2('{}',224) where phno='{}' and password=Sha2('{}',224);".format(p_Newpassword,phno,p_CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0
  
	def show_aptmnt(self,patient_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,user_info.FName,user_info.LName,doctors.spec,aptmnt.date,aptmnt.slot from aptmnt,doctors,user_info where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=user_info.phno and aptmnt.patient_id='{}' order by aptmnt.date,aptmnt.slot;".format(patient_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	def getName(self,patient_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select FName, LName from user_info where phno='{}';".format(patient_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows	

class Appointment:
	
	def __init__(self):
		pass

	def showDoctors(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from doctors;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	def getSlot(self,docID,date):		
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select * from slots where doctor_id='{}' and date='{}';".format(docID,date)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	def addSlot(self,docID,date):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into slots values('{}','{}',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);".format(date,docID)
		cursor.execute(query)
		cursor.execute("commit")
		
		
	def updateSlot(self,sqlslot,docID,date):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		
		query="select {} from slots where doctor_id='{}' and date='{}';".format(sqlslot,docID,date)
		cursor.execute(query)
		rows=cursor.fetchall()
			
		if rows[0][0]==1:
			return -1
		

		query="update slots set {}=1 where doctor_id='{}' and date='{}';".format(sqlslot,docID,date)
		cursor.execute(query)
		cursor.execute("commit")
		return 0
	
	def insertAptmnt(self,phno,docID,date,slot):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into aptmnt(patient_id,doctor_id,date,slot) values('{}','{}','{}','{}');".format(phno,docID,date,slot)
		cursor.execute(query)
		cursor.execute("commit")
	
	def addTempUser(self,p_Fname,p_Lname,date,gender,phno,slot):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into temp_users(FName,LName,dob,gender,phno,slot,date) values('{}','{}','{}','{}','{}','{}','{}');".format(p_Fname,p_Lname,date,gender,phno,slot,date)
		cursor.execute(query)
		cursor.execute("commit")	
	
	def aptmnt_doctors(self,identifier,spec,gender,order):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		if identifier==0:
			query = "select * from doctors;"
		elif identifier==1:
			query = "select * from doctors order by exp {};".format(order)
		elif identifier==2:			
			query = "select * from doctors where spec='{}';".format(spec)
		elif identifier==3:
			query = "select * from doctors where gender='{}';".format(gender)
		elif identifier==4:
			query = "select * from doctors where spec='{}' order by exp {};".format(spec,order)
		elif identifier==5:
			query = "select * from doctors where gender='{}' and spec='{}';".format(gender,spec)
		elif identifier==6:
			query = "select * from doctors where gender='{}' order by exp {};".format(gender,order)
		elif identifier==7:
			query = "select * from doctors where gender='{}' and spec='{}' order by exp {};".format(gender,spec,order)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	def delete_old_aptmnt(self,date):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="delete from aptmnt where date<'{}';".format(date)
		cursor.execute(query)
		query="delete from slots where date<'{}';".format(date)
		cursor.execute(query)
		query="delete from temp_users where date<'{}';".format(date)
		cursor.execute(query)
		# query="delete from slots where (09$00_09$15 + 09$15_09$30 + 09$30_09$45 + 09$45_10$00 + 10$00_10$15 + 10$15_10$30 + 10$30_10$45 + 10$45_11$00 + 11$00_11$15 + 11$15_11$30 + 11$30_11$45 + 11$45_12$00 + 18$00_18$15 + 18$15_18$30 + 18$30_18$45 + 18$45_19$00 + 19$00_19$15 + 19$15_19$30 + 19$30_19$45 + 19$45_20$00 + 20$00_20$15 + 20$15_20$30 + 20$30_20$45 + 20$45_21$00)=0;"
		# cursor.execute(query)
		cursor.execute("commit")

class Receptionist:
	
	def __init__(self):
		pass

	def verify(self,recep_id,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from receptionists where recep_id='{}' and password=Sha2('{}',224);").format(recep_id,password)
		if(recep_id=='' or password==''):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):	#Account doesn't exist
			return 1
		else:				# Account already exists
			return 0
	
	def getName(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select FName, LName from receptionists where recep_id='{}';".format(recep_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	def show_aptmnts(self,date,speciality,identifier):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		if identifier==0:
			query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,doctors.spec,users.FName,users.LName,aptmnt.patient_id,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select FName,LName,phno from user_info union select FName,LName,phno from temp_users) as users where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=users.phno order by aptmnt.date,aptmnt.slot"
		elif identifier==1:
			query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,doctors.spec,users.FName,users.LName,aptmnt.patient_id,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select FName,LName,phno from user_info union select FName,LName,phno from temp_users) as users where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=users.phno and doctors.spec='{}' order by aptmnt.date,aptmnt.slot;".format(speciality)
		elif identifier==2:
			query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,doctors.spec,users.FName,users.LName,aptmnt.patient_id,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select FName,LName,phno from user_info union select FName,LName,phno from temp_users) as users where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=users.phno and aptmnt.date='{}' order by aptmnt.date,aptmnt.slot;".format(date)
		elif identifier==3:
			query="select aptmnt.aptmnt_id,aptmnt.doctor_id,doctors.FName,doctors.LName,doctors.spec,users.FName,users.LName,aptmnt.patient_id,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select FName,LName,phno from user_info union select FName,LName,phno from temp_users) as users where aptmnt.doctor_id=doctors.doctor_id and aptmnt.patient_id=users.phno and aptmnt.date='{}' and doctors.spec='{}' order by aptmnt.date,aptmnt.slot;".format(date,speciality)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
		
	def update_credentials(self,CurrentPassword,Newpassword,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()			
		
		query="select * from receptionists where password=Sha2('{}',224) and recep_id='{}'".format(CurrentPassword,recep_id)
		cursor.execute(query)		
		vari=cursor.fetchall()
		if(len(vari)==0): # Entered password is incorrect
			return -1
		query="UPDATE receptionists SET password=Sha2('{}',224) where recep_id='{}' and password=Sha2('{}',224);".format(Newpassword,recep_id,CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0

class Admin:
	
	def __init__(self):
		pass

	def verify(self,recep_id,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from admin where admin_id='{}' and password=Sha2('{}',224);").format(recep_id,password)
		if(recep_id=='' or password==''):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):
			return 1
		else:
			return 0

	def getName(self,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select FName, LName from admin where admin_id='{}';".format(admin_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	def check_new_docid(self,doctor_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from doctors where doctor_id='{}';".format(doctor_id)
		if(doctor_id==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0): # Account doesn't exist
			return 1
		else:			  #Account already exists
			return 0
		
	def check_new_recep_id(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from receptionists where recep_id='{}';".format(recep_id)
		if(recep_id==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0): # Account doesn't exist
			return 1
		else:			  # Account already exists
			return 0
	
	def addDoc(self,doctor_id,Fname,Lname,spec,exp,gender,edu,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into doctors values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');").format(doctor_id,Fname,Lname,spec,exp,gender,edu,"Doctor"+gender,Fname,admin_id)
		cursor.execute(query)
		cursor.execute("commit")

	def updateDoc(self,doctor_id,Fname,Lname,spec,exp,gender,edu,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("update doctors set FName='{}',LName='{}',spec='{}',exp='{}',gender='{}',edu='{}',name='{}',admin_id='{}' where doctor_id='{}';").format(Fname,Lname,spec,exp,gender,edu,Fname,admin_id,doctor_id)
		cursor.execute(query)
		cursor.execute("commit")

	def deleteDoc(self,doctorID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "delete from doctors where doctor_id='{}';".format(doctorID)
		cursor.execute(query)
		cursor.execute("commit")

	def addReceptionist(self,recep_id,Fname,Lname,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into receptionists(recep_id,FName,LName,admin_id) values('{}','{}','{}','{}');").format(recep_id,Fname,Lname,admin_id)
		cursor.execute(query)
		cursor.execute("commit")

	def deleteReceptionist(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "delete from receptionists where recep_id='{}';".format(recep_id)
		cursor.execute(query)
		cursor.execute("commit")

	def getDoctor(self,doctorID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from doctors where doctor_id='{}';".format(doctorID)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	def update_credentials(self,CurrentPassword,Newpassword,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select * from admin where password=Sha2('{}',224) and admin_id='{}'".format(CurrentPassword,admin_id)
		cursor.execute(query)		
		vari=cursor.fetchall()
		if(len(vari)==0):	#Entered password is incorrect
			return -1
		query="UPDATE admin SET password=Sha2('{}',224) where admin_id='{}' and password=Sha2('{}',224);".format(Newpassword,admin_id,CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0
	def getReceptionist(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from receptionists where recep_id='{}';".format(recep_id)
		cursor.execute(query)
		row=cursor.fetchall()
		return row
	def showReceptionists(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select recep_id,FName,LName from receptionists;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	def showAdmins(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select admin_id from admin;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	def showDoctors(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select doctor_id,FName,LName,spec from doctors;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows