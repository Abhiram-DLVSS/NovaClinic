import mysql.connector
import os

DBhost = '172.24.0.6'
DBuser = 'root'
DBpassword = 'root'
DBname = 'nova'


class Admin:

    def __init__(self):
        pass

    # Verify the given Admin Credentials
    def verify(self, Admin_ID, Password):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = (
            "select * from admin where Admin_ID='{}' and Password=Sha2('{}',224);").format(Admin_ID, Password)
        if (Admin_ID == '' or Password == ''):
            return -1
        cursor.execute(query)
        vari = cursor.fetchall()
        if (len(vari) == 0):
            return 1
        else:
            return 0

    # Name of the Admin
    def getName(self, Admin_ID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select First_Name, Last_Name from admin where Admin_ID='{}';".format(
            Admin_ID)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # Verify whether the given Receptionist ID is unique or not

    def check_new_recep_id(self, Recep_ID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select * from receptionists where Recep_ID='{}';".format(
            Recep_ID)
        if (Recep_ID == None):
            return -1
        cursor.execute(query)
        vari = cursor.fetchall()
        # If a Receptionist with the same ID already exists return 0 else 1
        if (len(vari) == 0):
            return 1
        else:
            return 0

    # Add a new Receptionist
    def addReceptionist(self, Recep_ID, Fname, Lname):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = ("insert into receptionists(Recep_ID,First_Name,Last_Name) values('{}','{}','{}');").format(
            Recep_ID, Fname, Lname)
        cursor.execute(query)
        cursor.execute("commit")

    # Delete a Receptionist
    def deleteReceptionist(self, Recep_ID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "delete from receptionists where Recep_ID='{}';".format(
            Recep_ID)
        cursor.execute(query)
        cursor.execute("commit")

    # Update the credentials of the Admin
    def update_credentials(self, CurrentPassword, Newpassword, Admin_ID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select * from admin where Password=Sha2('{}',224) and Admin_ID='{}'".format(
            CurrentPassword, Admin_ID)
        cursor.execute(query)
        vari = cursor.fetchall()
        # If entered Password is incorrect
        if (len(vari) == 0):
            return -1
        query = "UPDATE admin SET Password=Sha2('{}',224) where Admin_ID='{}' and Password=Sha2('{}',224);".format(
            Newpassword, Admin_ID, CurrentPassword)
        cursor.execute(query)
        cursor.execute("commit")
        return 0

    # Returns the Information about a Receptionist to autofill delete Receptionist modal

    def getReceptionist(self, Recep_ID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select * from receptionists where Recep_ID='{}';".format(
            Recep_ID)
        cursor.execute(query)
        row = cursor.fetchall()
        return row

    # Returns ID,Name of the Receptionist
    def showReceptionists(self):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = ("select Recep_ID,First_Name,Last_Name from receptionists;")
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # Returns ID,Name of the Admin
    def showAdmins(self):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = ("select Admin_ID,First_Name,Last_Name from admin;")
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # Verify the given Receptionist Credentials
    def rverify(self, Recep_ID, Password):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = (
            "select * from receptionists where Recep_ID='{}' and Password=Sha2('{}',224);").format(Recep_ID, Password)
        if (Recep_ID == '' or Password == ''):
            return -1
        cursor.execute(query)
        vari = cursor.fetchall()
        # If the account exists return 0 else 1
        if (len(vari) == 0):
            return 1
        else:
            return 0

    # Name of the Receptionist
    def rgetName(self, Recep_ID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select First_Name, Last_Name from receptionists where Recep_ID='{}';".format(
            Recep_ID)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # Update the credentials of the Receptionist
    def rupdate_credentials(self, CurrentPassword, Newpassword, Recep_ID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()

        query = "select * from receptionists where Password=Sha2('{}',224) and Recep_ID='{}'".format(
            CurrentPassword, Recep_ID)
        cursor.execute(query)
        vari = cursor.fetchall()
        # If Entered Password is incorrect
        if (len(vari) == 0):
            return -1
        query = "UPDATE receptionists SET Password=Sha2('{}',224) where Recep_ID='{}' and Password=Sha2('{}',224);".format(
            Newpassword, Recep_ID, CurrentPassword)
        cursor.execute(query)
        cursor.execute("commit")
        return 0
