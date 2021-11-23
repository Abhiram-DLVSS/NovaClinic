import mysql.connector
from flask import jsonify

class Mysqlhandler:	
	
	def __init__(self):
		pass
	def add_user(self,name,docname,spec,message):
		cnx=mysql.connector.connect(user='root',password='1431',database='testdb')
		cursor=cnx.cursor()
		query = ("insert into greviance values('{}','{}','{}','{}');".format(name,docname,spec,message))
		cursor.execute(query)
		cursor.execute("commit")
		print("Added User.")
		cursor=cnx.cursor()
		query = ("select * from greviance;")
		cursor.execute(query)
		return

# def main():
# 	mysqlhandler=Mysqlhandler()
# 	print(mysqlhandler.add_user("testeteste","test","testet","mesaage"))


# if __name__=="__main__":
# 	main()