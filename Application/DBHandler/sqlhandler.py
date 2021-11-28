import mysql.connector
from .python_mysql_dbconfig import read_db_config

db=read_db_config()
cnx=mysql.connector.connect(user=db['user'],password=db['password'],database=db['database'])

class Mysqlhandler:	
	
	def __init__(self):
		pass
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

# def main():
# 	mysqlhandler=Mysqlhandler()
# 	print(mysqlhandler.add_user("testeteste","test","testet","mesaage"))


# if __name__=="__main__":
# 	main()