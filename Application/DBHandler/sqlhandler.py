import mysql.connector
# from .python_mysql_dbconfig import read_db_config
import os

# db=read_db_config()
# cnx=mysql.connector.connect(user=db['user'],password=db['password'],database=db['database'])
# cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)

DB_URL = os.environ.get('CLEARDB_DATABASE_URL')


DBhost=DB_URL[32:59]
DBuser=DB_URL[8:22]
DBpassword=DB_URL[23:31]
DBname=DB_URL[60:82]



class Mysqlhandler:	
	
	def __init__(self):
		pass
  
	def show_doctors_as_requested(query):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	def check_user(self,phno,password):
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
			cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)

		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):
			# Account doesn't exist
			return 1
		else:
			# Account already exists
			return 0

	def add_user_info(self,firstname,lastname,dob,gender,phno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into user_info values('{}','{}','{}','{}','{}');").format(firstname,lastname,dob,gender,phno)
		cursor.execute(query)
		cursor.execute("commit")
		return
	
	def add_user_credentials(self,phno,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into user_credentials values('{}',Sha2('{}',224));").format(phno,password)
		cursor.execute(query)
		cursor.execute("commit")
		return
		
		
	def update_user_info(self,FName,LName,NewPhno,OldPhno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="UPDATE user_info SET firstname='{}',lastname='{}',phno='{}' where phno='{}';".format(FName,LName,NewPhno,OldPhno)
		cursor.execute(query)
		query="UPDATE user_credentials SET phno='{}' where phno='{}';".format(NewPhno,OldPhno)
		cursor.execute(query)		
		query="UPDATE aptmnt SET patientid='{}' where patientid='{}';".format(NewPhno,OldPhno)
		cursor.execute(query)
		cursor.execute("commit")
		return
  
	def update_user_credentials(self,p_CurrentPassword,p_Newpassword,phno):
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
  
	def show_aptmnt_for_patient(self,patient_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.FName,doctors.LName,user_info.firstname,user_info.lastname,doctors.spec,aptmnt.date,aptmnt.slot from aptmnt,doctors,user_info where aptmnt.doctorid=doctors.id and aptmnt.patientid=user_info.phno and aptmnt.patientid='{}' order by aptmnt.date,aptmnt.slot;".format(patient_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	def show_aptmnt_for_recep(self,date,speciality,identifier):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		if identifier==0:
			query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.FName,doctors.LName,doctors.spec,users.firstname,users.lastname,aptmnt.patientid,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select firstname,lastname,phno from user_info union select firstname,lastname,phno from temp_users) as users where aptmnt.doctorid=doctors.id and aptmnt.patientid=users.phno order by aptmnt.date,aptmnt.slot"
		elif identifier==1:
			query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.FName,doctors.LName,doctors.spec,users.firstname,users.lastname,aptmnt.patientid,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select firstname,lastname,phno from user_info union select firstname,lastname,phno from temp_users) as users where aptmnt.doctorid=doctors.id and aptmnt.patientid=users.phno and doctors.spec='{}' order by aptmnt.date,aptmnt.slot;".format(speciality)
		elif identifier==2:
			query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.FName,doctors.LName,doctors.spec,users.firstname,users.lastname,aptmnt.patientid,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select firstname,lastname,phno from user_info union select firstname,lastname,phno from temp_users) as users where aptmnt.doctorid=doctors.id and aptmnt.patientid=users.phno and aptmnt.date='{}' order by aptmnt.date,aptmnt.slot;".format(date)
		elif identifier==3:
			query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.FName,doctors.LName,doctors.spec,users.firstname,users.lastname,aptmnt.patientid,aptmnt.date,aptmnt.slot from aptmnt,doctors,(select firstname,lastname,phno from user_info union select firstname,lastname,phno from temp_users) as users where aptmnt.doctorid=doctors.id and aptmnt.patientid=users.phno and aptmnt.date='{}' and doctors.spec='{}' order by aptmnt.date,aptmnt.slot;".format(date,speciality)
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

   
	def getNameofUser(self,patient_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select firstname, lastname from user_info where phno='{}';".format(patient_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	def getNameofReceptionist(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select FName, LName from receptionists where recep_id='{}';".format(recep_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	def getNameofAdmin(self,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select FName, LName from admin_credentials where admin_id='{}';".format(admin_id)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	def check_new_docid(self,id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from user_credentials where phno='{}';".format(id)
		if(id==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):
			# Account doesn't exist
			return 1
		else:
			#Account already exists
			return 0
		
	def check_new_recep_id(self,id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from receptionists where recep_id='{}';".format(id)
		if(id==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):
			# Account doesn't exist
			return 1
		else:
			# Account already exists
			return 0

    
	def check_receptionist(self,recep_id,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from receptionists where recep_id='{}' and password=Sha2('{}',224);").format(recep_id,password)
		if(recep_id=='' or password==''):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):
			#Account doesn't exist
			return 1
		else:
			# Account already exists
			return 0
	
	def check_admin(self,recep_id,password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from admin_credentials where admin_id='{}' and password=Sha2('{}',224);").format(recep_id,password)
		if(recep_id=='' or password==''):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):
			return 1
		else:
			return 0

	def showDoctors(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from doctors;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
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
		query = ("select admin_id from admin_credentials;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	def getDoctor(self,doctorID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from doctors where id='{}';".format(doctorID)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	def getReceptionist(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from receptionists where recep_id='{}';".format(recep_id)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	def getSlot(self,docID,date):		
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select * from slots where doctorid='{}' and date='{}';".format(docID,date)
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
		query="update slots set {}=1 where doctorid='{}' and date='{}';".format(sqlslot,docID,date)
		cursor.execute(query)
		cursor.execute("commit")
	
	def insertAptmnt(self,phno,docID,date,slot):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into aptmnt(patientid,doctorid,date,slot) values('{}','{}','{}','{}');".format(phno,docID,date,slot)
		cursor.execute(query)
		cursor.execute("commit")
	
	def addTempUser(self,p_Fname,p_Lname,date,gender,phno,slot):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into temp_users(firstname,lastname,dob,gender,phno,slot,date) values('{}','{}','{}','{}','{}','{}','{}');".format(p_Fname,p_Lname,date,gender,phno,slot,date)
		cursor.execute(query)
		cursor.execute("commit")
	
	# def aptmntcommit():
	# 	cnx.reconnect()
	# 	cursor=cnx.cursor()
	# 	cursor.execute("commit")
	# def aptmntrollback():
	# 	cnx.reconnect()
	# 	cursor=cnx.cursor()
	# 	cursor.execute("rollback")



	def addDoc(self,id,Fname,Lname,spec,exp,gender,edu,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into doctors values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');").format(id,Fname,Lname,spec,exp,gender,edu,"Doctor"+gender,Fname,admin_id)
		cursor.execute(query)
		cursor.execute("commit")
		return

	def updateDoc(self,id,Fname,Lname,spec,exp,gender,edu,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("update doctors set FName='{}',LName='{}',spec='{}',exp='{}',gender='{}',edu='{}',name='{}',admin_id='{}' where id='{}';").format(Fname,Lname,spec,exp,gender,edu,Fname,admin_id,id)
		cursor.execute(query)
		cursor.execute("commit")
		return

	def deleteDoc(self,doctorID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "delete from doctors where id='{}';".format(doctorID)
		cursor.execute(query)
		cursor.execute("commit")

	def addReceptionist(self,id,Fname,Lname,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into receptionists(recep_id,FName,LName,admin_id) values('{}','{}','{}','{}');").format(id,Fname,Lname,admin_id)
		cursor.execute(query)
		cursor.execute("commit")
		return

	def deleteReceptionist(self,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "delete from receptionists where recep_id='{}';".format(recep_id)
		cursor.execute(query)
		cursor.execute("commit")

	def update_receptionists(self,CurrentPassword,Newpassword,recep_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()			
		
		query="select * from receptionists where password=Sha2('{}',224) and recep_id='{}'".format(CurrentPassword,recep_id)
		cursor.execute(query)		
		vari=cursor.fetchall()
		if(len(vari)==0):
			# Entered password is incorrect
			return -1
		query="UPDATE receptionists SET password=Sha2('{}',224) where recep_id='{}' and password=Sha2('{}',224);".format(Newpassword,recep_id,CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0
	
	def update_admin_credentials(self,CurrentPassword,Newpassword,admin_id):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()			
		
		query="select * from admin_credentials where password=Sha2('{}',224) and admin_id='{}'".format(CurrentPassword,admin_id)
		cursor.execute(query)		
		vari=cursor.fetchall()
		if(len(vari)==0):
			#Entered password is incorrect
			return -1
		query="UPDATE admin_credentials SET password=Sha2('{}',224) where admin_id='{}' and password=Sha2('{}',224);".format(Newpassword,admin_id,CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0
	
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
