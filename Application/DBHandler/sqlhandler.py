import mysql.connector
from .python_mysql_dbconfig import read_db_config

db=read_db_config()
cnx=mysql.connector.connect(user=db['user'],password=db['password'],database=db['database'])


class Mysqlhandler:
		
	
	def __init__(self):
		pass
	def add_user(self,name,phno,email,message):
		cursor=cnx.cursor()
		query = ("insert into test values('{}',{},'{}','{}');".format(name,phno,email,message))
		cursor.execute(query)
		cursor.execute("commit")
		print("Added User.")
		cursor=cnx.cursor()
		query = ("select * from test;")
		cursor.execute(query)
		return
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
	

# def main():
# 	mysqlhandler=Mysqlhandler()
# 	print(mysqlhandler.add_user("testeteste","test","testet","mesaage"))


# if __name__=="__main__":
# 	main()