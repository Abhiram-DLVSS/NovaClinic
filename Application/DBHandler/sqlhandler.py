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
		
	def update_user_info(self,FName,LName,Phno):
		cursor=cnx.cursor()
		query="UPDATE user_info SET firstname='{}',lastname='{}' where phno='{}';".format(FName,LName,Phno) 
		cursor.execute(query)
		cursor.execute("commit")
		print("Updated User.")
		return
  
	def update_user_credentials(self,p_CurrentPassword,p_Newpassword):
		cursor=cnx.cursor()			
		query="UPDATE user_credentials SET password1='{}' where password1='{}';".format(p_Newpassword,p_CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		print("Updated User.")
		return
  
	def show_aptmnt(self,patient_id):
		print(patient_id)
		cursor=cnx.cursor()	
		query="select aptmnt.aptmntid,aptmnt.doctorid,doctors.name,user_info.firstname,user_info.lastname,aptmnt.patientid,aptmnt.date,aptmnt.slot from aptmnt,doctors,user_info where aptmnt.doctorid=doctors.id and aptmnt.patientid=user_info.phno and aptmnt.patientid='{}';".format(patient_id)
		# query="select * from aptmnt"
		cursor.execute(query)
		rows=cursor.fetchall()
		print(rows)
		return rows

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
		if(len(vari)!=0):
			# print("success")
			return 1
		else:
			# print("Failed")
			return 0
