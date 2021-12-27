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
	def verify(self,Phone_Number,Password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select Phone_Number from users where Phone_Number='{}' and Password=Sha2('{}',224);").format(Phone_Number,Password)
		if(Phone_Number==None and Password==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		#If the credentials are correct return 1 else 0
		if(len(vari)!=0):
			return 1
		else:
			return 0

	#Check whether the sign up Phone number is new
	def check_new_phno(self,Phone_Number):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select Phone_Number from users where Phone_Number='{}';").format(Phone_Number)
		if(Phone_Number==None):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()
		#If the account with the same number already exists return 0 else 1
		if(len(vari)==0):			
			return 1
		else:		
			return 0
	
	#Register User
	def add_user(self,First_Name,Last_Name,Date_Of_Birth,Gender,Phone_Number,Password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("insert into users values('{}',Sha2('{}',224),'{}','{}','{}','{}');").format(Phone_Number,Password,First_Name,Last_Name,Date_Of_Birth,Gender)
		cursor.execute(query)
		cursor.execute("commit")
	
	#Update the User Information
	def update_info(self,First_Name,Last_Name,NewPhno,OldPhno):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="UPDATE users SET First_Name='{}',Last_Name='{}',Phone_Number='{}' where Phone_Number='{}';".format(First_Name,Last_Name,NewPhno,OldPhno)
		cursor.execute(query)	
		query="UPDATE aptmnt SET Patient_ID='{}' where Patient_ID='{}';".format(NewPhno,OldPhno)
		cursor.execute(query)
		cursor.execute("commit")
	
	#Update the credentials of the User
	def update_credentials(self,p_CurrentPassword,p_Newpassword,Phone_Number):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()		
		query="select Phone_Number from users where Password=Sha2('{}',224) and Phone_Number='{}'".format(p_CurrentPassword,Phone_Number)
		cursor.execute(query)		
		vari=cursor.fetchall()
		if(len(vari)==0):
			return -1
		query="UPDATE users SET Password=Sha2('{}',224) where Phone_Number='{}' and Password=Sha2('{}',224);".format(p_Newpassword,Phone_Number,p_CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0
	
	#Show Upcoming Appointments for the user
	def show_aptmnt(self,Patient_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,users.First_Name,users.Last_Name,doctors.Specialization,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Patient_ID='{}' order by aptmnt.Date,aptmnt.Slot;".format(Patient_ID)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	#Name of the User
	def getName(self,Patient_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select First_Name, Last_Name from users where Phone_Number='{}';".format(Patient_ID)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows	

class Appointment:
	
	def __init__(self):
		pass
	
	#Show the list of Doctors with their information
	def aptmnt_doctors(self,identifier,spec,Gender,order):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		if identifier==0:
			query = "select * from doctors;"
		elif identifier==1:
			query = "select * from doctors order by Experience {};".format(order)
		elif identifier==2:			
			query = "select * from doctors where Specialization='{}';".format(spec)
		elif identifier==3:
			query = "select * from doctors where Gender='{}';".format(Gender)
		elif identifier==4:
			query = "select * from doctors where Specialization='{}' order by Experience {};".format(spec,order)
		elif identifier==5:
			query = "select * from doctors where Gender='{}' and Specialization='{}';".format(Gender,spec)
		elif identifier==6:
			query = "select * from doctors where Gender='{}' order by Experience {};".format(Gender,order)
		elif identifier==7:
			query = "select * from doctors where Gender='{}' and Specialization='{}' order by Experience {};".format(Gender,spec,order)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows

	#Data of a Doctors slots on a choosen Date
	def getSlot(self,docID,Date):		
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select Date,Doctor_ID,Time from slots where Doctor_ID='{}' and Date='{}';".format(docID,Date)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	#Time String in Slots Table - Availability
	def getSlottimestring(self,docID,Date):		
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select Time from slots where Doctor_ID='{}' and Date='{}';".format(docID,Date)
		cursor.execute(query)
		row=cursor.fetchall()
		return row

	#If the Slot isn't present, add the Slot
	def addSlot(self,docID,Date):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into slots values('{}','{}','000000000000000000000000');".format(Date,docID)
		cursor.execute(query)
		cursor.execute("commit")
		
	#Upon confirming an Appointment update the Slot
	def updateSlot(self,Time,index,docID,Date):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="select Time from slots where Doctor_ID='{}' and Date='{}';".format(docID,Date)
		cursor.execute(query)
		rows=cursor.fetchall()
		chk=rows[0][0][index]
		if chk=="1":
			return -1
		else:
			query="update slots set Time='{}' where Doctor_ID='{}' and Date='{}';".format(Time,docID,Date)
			cursor.execute(query)
			cursor.execute("commit")
			return 0
	
	#Confirming the Appointment
	def insertAptmnt(self,Phone_Number,docID,Date,Slot):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into aptmnt(Patient_ID,Doctor_ID,Date,Slot) values('{}','{}','{}','{}');".format(Phone_Number,docID,Date,Slot)
		cursor.execute(query)
		cursor.execute("commit")
	
	#Walk In Appointment Users(Patients)
	def addTempUser(self,p_Fname,p_Lname,Date,Gender,Phone_Number,Slot,docID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="insert into temp_users(First_Name,Last_Name,Date_Of_Birth,Gender,Phone_Number,Slot,Date,Doctor_ID) values('{}','{}','{}','{}','{}','{}','{}','{}');".format(p_Fname,p_Lname,Date,Gender,Phone_Number,Slot,Date,docID)
		cursor.execute(query)
		cursor.execute("commit")	
	
	#Delete all old Appointments
	def delete_old_aptmnt(self,Date):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="delete from aptmnt where Date<'{}';".format(Date)
		cursor.execute(query)
		query="delete from slots where Date<'{}';".format(Date)
		cursor.execute(query)
		query="delete from temp_users where Date<'{}';".format(Date)
		cursor.execute(query)
		cursor.execute("commit")
	
	#Cancel Appointment
	def delete_aptmnt(self,Aptmnt_ID,docID,Date,Time,phno,slot):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query="delete from aptmnt where Aptmnt_ID='{}';".format(Aptmnt_ID)
		cursor.execute(query)
		query="update slots set Time='{}' where Doctor_ID='{}' and Date='{}';".format(Time,docID,Date)
		cursor.execute(query)
		query="delete from temp_users where Phone_Number='{}' and Date='{}' and Doctor_ID='{}' and slot='{}';".format(phno,Date,docID,slot)
		cursor.execute(query)
		cursor.execute("commit")

class Receptionist:
	
	def __init__(self):
		pass

	#Verify the given Receptionist Credentials
	def verify(self,Recep_ID,Password):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		query = ("select * from receptionists where Recep_ID='{}' and Password=Sha2('{}',224);").format(Recep_ID,Password)
		if(Recep_ID=='' or Password==''):
			return -1
		cursor.execute(query)
		vari=cursor.fetchall()		
		#If the account exists return 0 else 1
		if(len(vari)==0):
			return 1
		else:
			return 0
	
	#Name of the Receptionist
	def getName(self,Recep_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()	
		query="select First_Name, Last_Name from receptionists where Recep_ID='{}';".format(Recep_ID)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	#Show Upcoming Appointments for the Receptionist
	def show_aptmnts(self,Date,speciality,identifier):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		if identifier==0:
			query="select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number from users union select First_Name,Last_Name,Phone_Number from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number order by aptmnt.Date,aptmnt.Slot"
		elif identifier==1:
			query="select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number from users union select First_Name,Last_Name,Phone_Number from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and doctors.Specialization='{}' order by aptmnt.Date,aptmnt.Slot;".format(speciality)
		elif identifier==2:
			query="select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number from users union select First_Name,Last_Name,Phone_Number from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date='{}' order by aptmnt.Date,aptmnt.Slot;".format(Date)
		elif identifier==3:
			query="select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number from users union select First_Name,Last_Name,Phone_Number from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date='{}' and doctors.Specialization='{}' order by aptmnt.Date,aptmnt.Slot;".format(Date,speciality)
		cursor.execute(query)
		rows=cursor.fetchall()
		return rows
	
	#Update the credentials of the Receptionist
	def update_credentials(self,CurrentPassword,Newpassword,Recep_ID):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()			
		
		query="select * from receptionists where Password=Sha2('{}',224) and Recep_ID='{}'".format(CurrentPassword,Recep_ID)
		cursor.execute(query)		
		vari=cursor.fetchall()
		#If Entered Password is incorrect
		if(len(vari)==0):
			return -1
		query="UPDATE receptionists SET Password=Sha2('{}',224) where Recep_ID='{}' and Password=Sha2('{}',224);".format(Newpassword,Recep_ID,CurrentPassword)
		cursor.execute(query)
		cursor.execute("commit")
		return 0

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