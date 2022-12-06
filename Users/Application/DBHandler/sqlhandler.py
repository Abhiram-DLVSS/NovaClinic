import mysql.connector
import os

DBhost = '172.24.0.4'
DBuser = 'root'
DBpassword = 'root'
DBname = 'nova'


class User:

    def __init__(self):
        pass

    # Verify the given User Credentials
    def verify(self, Phone_Number, Password):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = ("select Phone_Number from users where Phone_Number='{}' and Password=Sha2('{}',224);").format(
            Phone_Number, Password)
        if (Phone_Number == None and Password == None):
            return -1
        cursor.execute(query)
        vari = cursor.fetchall()
        # If the credentials are correct return 1 else 0
        if (len(vari) != 0):
            return 1
        else:
            return 0

    # Check whether the sign up Phone number is new
    def check_new_phno(self, Phone_Number):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = ("select Phone_Number from users where Phone_Number='{}';").format(
            Phone_Number)
        if (Phone_Number == None):
            return -1
        cursor.execute(query)
        vari = cursor.fetchall()
        # If the account with the same number already exists return 0 else 1
        if (len(vari) == 0):
            return 1
        else:
            return 0

    # Register User
    def add_user(self, First_Name, Last_Name, Date_Of_Birth, Gender, Phone_Number, Password):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = ("insert into users values('{}',Sha2('{}',224),'{}','{}','{}','{}');").format(
            Phone_Number, Password, First_Name, Last_Name, Date_Of_Birth, Gender)
        cursor.execute(query)
        cursor.execute("commit")

    # Update the User Information
    def update_info(self, First_Name, Last_Name, NewPhno, OldPhno):  # Uflag
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "UPDATE users SET First_Name='{}',Last_Name='{}',Phone_Number='{}' where Phone_Number='{}';".format(
            First_Name, Last_Name, NewPhno, OldPhno)
        cursor.execute(query)
        cursor.execute("commit")

    # Update the credentials of the User
    def update_credentials(self, p_CurrentPassword, p_Newpassword, Phone_Number):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select Phone_Number from users where Password=Sha2('{}',224) and Phone_Number='{}'".format(
            p_CurrentPassword, Phone_Number)
        cursor.execute(query)
        vari = cursor.fetchall()
        if (len(vari) == 0):
            return -1
        query = "UPDATE users SET Password=Sha2('{}',224) where Phone_Number='{}' and Password=Sha2('{}',224);".format(
            p_Newpassword, Phone_Number, p_CurrentPassword)
        cursor.execute(query)
        cursor.execute("commit")
        return 0

    # Name of the User
    def getName(self, Patient_ID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select First_Name, Last_Name from users where Phone_Number='{}';".format(
            Patient_ID)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # Details of the User
    def getUserDetails(self, Patient_ID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select First_Name, Last_Name,Date_Of_Birth,Gender from users where Phone_Number='{}';".format(
            Patient_ID)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # Details of the User
    def getAllUsers(self):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select First_Name, Last_Name,Phone_Number from users;"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
