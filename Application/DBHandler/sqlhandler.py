import mysql.connector
from .python_mysql_dbconfig import read_db_config

db=read_db_config()
cnx=mysql.connector.connect(user=db['user'],password=db['password'],database=db['database'])


class Mysqlhandler:	
	
	def __init__(self):
		pass

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