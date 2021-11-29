import mysql.connector
from .python_mysql_dbconfig import read_db_config

db=read_db_config()
cnx=mysql.connector.connect(user=db['user'],password=db['password'],database=db['database'])

class Mysqlhandler:	
	
	def __init__(self):
		pass
  
	def show_doctors():
		cursor=cnx.cursor()
		query = ("select * from doctors;")
		cursor.execute(query)
		rows=cursor.fetchall()
		# print(rows)
		return rows
  
	def show_doctors_as_requested(query):
		cursor=cnx.cursor()
		cursor.execute(query)
		rows=cursor.fetchall()
		# print(rows)
		return rows

	def check_user(self,phno,password):
		cursor=cnx.cursor()
		# print("phno="+phno)
		# print("password="+password)
		query = ("select * from user_credentials where phno='{}' and password1='{}';").format(phno,password)
		if(phno==None and password==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		# print(vari[0][0])
		if(len(vari)!=0):
			# print("success")
			return 1
		else:
			# print("Failed")
			return 0

	def check_new_phno(self,phno):
		cursor=cnx.cursor()
		# print("phno="+phno)
		# print("password="+password)
		query = ("select * from user_credentials where phno='{}';").format(phno)
		if(phno==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		# print(vari[0][0])
		if(len(vari)==0):
			# print("Account doesn't exist")
			return 1
		else:
			# print("Account already exists")
			return 0

	def add_user_info(self,firstname,lastname,dob,gender,phno):
		cursor=cnx.cursor()
		query = ("insert into user_info values('{}','{}','{}','{}','{}');").format(firstname,lastname,dob,gender,phno)
		cursor.execute(query)
		cursor=cnx.cursor()
		cursor.execute("commit")
		# print("Added User.")
		return
	
	def add_user_credentials(self,phno,password1):
		cursor=cnx.cursor()
		query = ("insert into user_credentials values('{}','{}');").format(phno,password1)
		cursor.execute(query)
		cursor=cnx.cursor()
		cursor.execute("commit")
		# print("Added User.")
		return

	def add_greviance(self,name,docname,spec,message):
		cursor=cnx.cursor()
		query = ("insert into greviance values('{}','{}','{}','{}');".format(name,docname,spec,message))
		cursor.execute(query)
		cursor.execute("commit")
		print("Added User.")
		return
		
	def update_user_info(self,FName,LName,NewPhno,OldPhno):
		cursor=cnx.cursor()
		query="UPDATE user_info SET firstname='{}',lastname='{}',phno='{}' where phno='{}';".format(FName,LName,NewPhno,OldPhno)
		cursor.execute(query)
		query="UPDATE user_credentials SET phno='{}' where phno='{}';".format(NewPhno,OldPhno)
		cursor.execute(query)
		cursor.execute("commit")
		print("Updated User.")
		return
  
	def update_user_credentials(self,p_CurrentPassword,p_Newpassword,phno):
		cursor=cnx.cursor()			
		
		query="select * from user_credentials where password1='{}' and phno='{}'".format(p_CurrentPassword,phno)
		cursor.execute(query)		
		vari=cursor.fetchall()
		if(len(vari)==0):
			# print("Entered password is incorrect")
			return -1

		query="UPDATE user_credentials SET password1='{}' where phno='{}' and password1='{}';".format(p_Newpassword,phno,p_CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		print("Updated User.")
		return 0
  
	def show_aptmnt(self,patient_id):
		print(patient_id)
		cursor=cnx.cursor()	
		query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.FName,doctors.LName,user_info.firstname,user_info.lastname,doctors.spec,aptmnt.date,aptmnt.slot from aptmnt,doctors,user_info where aptmnt.doctorid=doctors.id and aptmnt.patientid=user_info.phno and aptmnt.patientid='{}';".format(patient_id)
		# query="select * from aptmnt"
		cursor.execute(query)
		rows=cursor.fetchall()
		print(rows)
		return rows


	def delete_old_aptmnt(self,date):
		cursor=cnx.cursor()
		query="delete from aptmnt where date<'{}';".format(date)
		query="delete from slots where date<'{}';".format(date)
		# query="select * from aptmnt"
		cursor.execute(query)
		cursor.execute("commit")

   
	def getName(self,patient_id):
		print(patient_id)
		cursor=cnx.cursor()	
		query="select firstname, lastname from user_info where phno='{}';".format(patient_id)
		# query="select * from aptmnt"
		cursor.execute(query)
		rows=cursor.fetchall()
		print(rows)
		return rows
	def addDoc(self,id,Fname,Lname,spec,exp,gender,edu,rid):
		cursor=cnx.cursor()
		query = ("insert into doctors values('{}','{}','{}','{}','{}','{}','{}','defaultprofilepic','{}','{}');").format(id,Fname,Lname,spec,exp,gender,edu,Fname,rid)
		cursor.execute(query)
		# print("Added User.")
		return
	def commit():		
		cursor=cnx.cursor()
		cursor.execute("commit")

	def check_new_docid(self,id):
		cursor=cnx.cursor()
		# print("phno="+phno)
		# print("password="+password)
		query = "select * from user_credentials where phno='{}';".format(id)
		if(id==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		# print(vari[0][0])
		if(len(vari)==0):
			# print("Account doesn't exist")
			return 1
		else:
			# print("Account already exists")
			return 0

    
	def check_receptionist(self,recep_id,password):
		cursor=cnx.cursor()
		# print("recep_id="+recep_id)
		# print("password="+password)
		query = ("select * from receptionist_credentials where recep_id='{}' and password='{}';").format(recep_id,password)
		if(recep_id==None and password==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		# print(vari[0][0])

		if(len(vari)==0):
			# print("Account doesn't exist")
			return 1
		else:
			# print("Account already exists")
			return 0

	def showDoctors(self):
		cursor=cnx.cursor()
		query = ("select * from doctors;")
		cursor.execute(query)
		rows=cursor.fetchall()
		print(rows)
		return rows

	def getDoctor(self,doctorID):
		cursor=cnx.cursor()
		query = "select * from doctors where id='{}';".format(doctorID)
		cursor.execute(query)
		row=cursor.fetchall()
		print(row)
		return row

	def updateDoc(self,id,Fname,Lname,spec,exp,gender,edu,rid):
		cursor=cnx.cursor()
		query = ("update doctors set FName='{}',LName='{}',spec='{}',exp='{}',gender='{}',edu='{}',name='{}',rid='{}' where id='{}';").format(Fname,Lname,spec,exp,gender,edu,Fname,rid,id)
		print(query)
		cursor.execute(query)
		# print("Added User.")
		return

	def deleteDoc(self,doctorID):
		cursor=cnx.cursor()
		query = "delete from doctors where id='{}';".format(doctorID)
		cursor.execute(query)

	def update_receptionist_credentials(self,CurrentPassword,Newpassword,recep_id):
		cursor=cnx.cursor()			
		
		query="select * from receptionist_credentials where password='{}' and recep_id='{}'".format(CurrentPassword,recep_id)
		cursor.execute(query)		
		vari=cursor.fetchall()
		if(len(vari)==0):
			# print("Entered password is incorrect")
			return -1

		query="UPDATE receptionist_credentials SET password='{}' where recep_id='{}' and password='{}';".format(Newpassword,recep_id,CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		print("Updated User.")
		return 0
	
	def aptmnt_doctors(self,identifier,spec,gender,order):
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

		# print(query)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
