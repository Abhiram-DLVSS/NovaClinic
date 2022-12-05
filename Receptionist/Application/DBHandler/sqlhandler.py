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
	def show_aptmnts(self,Date,speciality,identifier,Today):
		cnx=mysql.connector.connect(host=DBhost,user=DBuser,password=DBpassword,database=DBname)
		cursor=cnx.cursor()
		if identifier==0:
			query="(select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d') as 'Date',aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number from users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date>='{}') union (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number,Slot,Doctor_ID,Date from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date=users.Date and aptmnt.Slot=users.Slot and aptmnt.Doctor_ID=users.Doctor_ID and aptmnt.Date>='{}') order by Date,Slot,Aptmnt_ID".format(Today,Today)
		elif identifier==1:
			query="(select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d') as 'Date',aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number from users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and doctors.Specialization='{}' and aptmnt.Date>='{}') union (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number,Slot,Doctor_ID,Date from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date=users.Date and aptmnt.Slot=users.Slot and aptmnt.Doctor_ID=users.Doctor_ID and doctors.Specialization='{}' and aptmnt.Date>='{}') order by Date,Slot,Aptmnt_ID".format(speciality,Today,speciality,Today)
		elif identifier==2:
			query="(select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d') as 'Date',aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number from users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date='{}' and aptmnt.Date>='{}') union (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number,Slot,Doctor_ID,Date from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date=users.Date and aptmnt.Slot=users.Slot and aptmnt.Doctor_ID=users.Doctor_ID and aptmnt.Date='{}' and aptmnt.Date>='{}') order by Date,Slot,Aptmnt_ID".format(Date,Today,Date,Today)
		elif identifier==3:
			query="(select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d') as 'Date',aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number from users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date='{}' and doctors.Specialization='{}' and aptmnt.Date>='{}') union (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number,Slot,Doctor_ID,Date from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date=users.Date and aptmnt.Slot=users.Slot and aptmnt.Doctor_ID=users.Doctor_ID and aptmnt.Date='{}' and doctors.Specialization='{}' and aptmnt.Date>='{}') order by Date,Slot,Aptmnt_ID".format(Date,speciality,Today,Date,speciality,Today)
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
