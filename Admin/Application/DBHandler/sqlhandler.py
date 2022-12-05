import mysql.connector
import os

# DBhost=os.environ.get('DBhost')
# DBuser=os.environ.get('DBuser')
# DBpassword=os.environ.get('DBpassword')
# DBname=os.environ.get('DBname')

DBhost='localhost'
DBuser='root'
DBpassword='sqlpassword'
DBname='nova'



class Admin:
	
	def __init__(self):
		pass

	#Verify the given Admin Credentials
	def verify(self,Admin_ID,Password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from admin where Admin_ID='{}' and Password=Sha2('{}',224);").format(Admin_ID,Password)
		if(Admin_ID=='' or Password==''):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		if(len(vari)==0):
			return 1
		else:
			return 0

	#Name of the Admin
	def getName(self,Admin_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select First_Name, Last_Name from admin where Admin_ID='{}';".format(Admin_ID)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	#Verify whether the given Doctor ID is unique or not
	def check_new_docid(self,Doctor_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from doctors where Doctor_ID='{}';".format(Doctor_ID)
		if(Doctor_ID==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		#If a doctor with the same ID already exists return 0 else 1
		if(len(vari)==0):
			return 1
		else:
			return 0
	
	#Verify whether the given Receptionist ID is unique or not
	def check_new_recep_id(self,Recep_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from receptionists where Recep_ID='{}';".format(Recep_ID)
		if(Recep_ID==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		#If a Receptionist with the same ID already exists return 0 else 1
		if(len(vari)==0):
			return 1
		else:
			return 0
	
	#Add a New Doctor
	def addDoc(self,Doctor_ID,Fname,Lname,spec,exp,Gender,edu):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into doctors values('{}','{}','{}','{}','{}','{}','{}','{}');").format(Doctor_ID,Fname,Lname,spec,exp,Gender,edu,"Doctor"+Gender)
		cursor.execute(query)
		cursor.execute("commit")

	#Update the information of a Doctor
	def updateDoc(self,Doctor_ID,Fname,Lname,spec,exp,Gender,edu):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("update doctors set First_Name='{}',Last_Name='{}',Specialization='{}',Experience='{}',Gender='{}',Education='{}' where Doctor_ID='{}';").format(Fname,Lname,spec,exp,Gender,edu,Doctor_ID)
		cursor.execute(query)
		cursor.execute("commit")

	#Delete a Doctor
	def deleteDoc(self,doctorID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "delete from doctors where Doctor_ID='{}';".format(doctorID)
		cursor.execute(query)
		cursor.execute("commit")

	#Add a new Receptionist
	def addReceptionist(self,Recep_ID,Fname,Lname):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into receptionists(Recep_ID,First_Name,Last_Name) values('{}','{}','{}');").format(Recep_ID,Fname,Lname)
		cursor.execute(query)
		cursor.execute("commit")

	#Delete a Receptionist
	def deleteReceptionist(self,Recep_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "delete from receptionists where Recep_ID='{}';".format(Recep_ID)
		cursor.execute(query)
		cursor.execute("commit")

	#Update the credentials of the Admin
	def update_credentials(self,CurrentPassword,Newpassword,Admin_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select * from admin where Password=Sha2('{}',224) and Admin_ID='{}'".format(CurrentPassword,Admin_ID)
		cursor.execute(query)		
		vari=cursor.fetchall()
		#If entered Password is incorrect
		if(len(vari)==0):	
			return -1
		query="UPDATE admin SET Password=Sha2('{}',224) where Admin_ID='{}' and Password=Sha2('{}',224);".format(Newpassword,Admin_ID,CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0

	#Returns the Information about a Doctor to autofill delete and update Doctor modals
	def getDoctor(self,doctorID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from doctors where Doctor_ID='{}';".format(doctorID)
		cursor.execute(query)
		row=cursor.fetchall()
		return row	

	#Returns the Information about a Receptionist to autofill delete Receptionist modal
	def getReceptionist(self,Recep_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = "select * from receptionists where Recep_ID='{}';".format(Recep_ID)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	#Returns ID,Name of the Receptionist
	def showReceptionists(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select Recep_ID,First_Name,Last_Name from receptionists;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	#Returns ID,Name of the Admin
	def showAdmins(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select Admin_ID,First_Name,Last_Name from admin;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	#Returns ID,Name and Specialization of the Doctor
	def showDoctors(self):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select Doctor_ID,First_Name,Last_Name,Specialization from doctors;")
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows