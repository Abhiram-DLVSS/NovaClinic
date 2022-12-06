import mysql.connector
import os

DBhost = '172.24.0.8'
DBuser = 'root'
DBpassword = 'root'
DBname = 'nova'


class Appointment:

    def __init__(self):
        pass

    def show_aptmnt(self, Patient_ID, Date, Fname, Lname):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,'{}','{}',doctors.Specialization,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d'),aptmnt.Slot from aptmnt,doctors where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID='{}' and aptmnt.Date>='{}' order by aptmnt.Date,aptmnt.Slot;".format(
            Fname, Lname, Patient_ID, Date)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # Show the list of Doctors with their information
    def aptmnt_doctors(self, identifier, spec, Gender, order):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        if identifier == 0:
            query = "select * from doctors;"
        elif identifier == 1:
            query = "select * from doctors order by Experience {};".format(
                order)
        elif identifier == 2:
            query = "select * from doctors where Specialization='{}';".format(
                spec)
        elif identifier == 3:
            query = "select * from doctors where Gender='{}';".format(Gender)
        elif identifier == 4:
            query = "select * from doctors where Specialization='{}' order by Experience {};".format(
                spec, order)
        elif identifier == 5:
            query = "select * from doctors where Gender='{}' and Specialization='{}';".format(
                Gender, spec)
        elif identifier == 6:
            query = "select * from doctors where Gender='{}' order by Experience {};".format(
                Gender, order)
        elif identifier == 7:
            query = "select * from doctors where Gender='{}' and Specialization='{}' order by Experience {};".format(
                Gender, spec, order)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # Data of a Doctors slots on a choosen Date
    def getSlot(self, docID, Date):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select Date,Doctor_ID,Time from slots where Doctor_ID='{}' and Date='{}';".format(
            docID, Date)
        cursor.execute(query)
        row = cursor.fetchall()
        return row

    # Time String in Slots Table - Availability
    def getSlottimestring(self, docID, Date):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select Time from slots where Doctor_ID='{}' and Date='{}';".format(
            docID, Date)
        cursor.execute(query)
        row = cursor.fetchall()
        return row

    # If the Slot isn't present, add the Slot
    def addSlot(self, docID, Date):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "insert into slots values('{}','{}','000000000000000000000000');".format(
            Date, docID)
        cursor.execute(query)
        cursor.execute("commit")

    # Upon confirming an Appointment update the Slot
    def updateSlot(self, Time, index, docID, Date):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select Time from slots where Doctor_ID='{}' and Date='{}';".format(
            docID, Date)
        cursor.execute(query)
        rows = cursor.fetchall()
        chk = rows[0][0][index]
        if chk == "1":
            return -1
        else:
            query = "update slots set Time='{}' where Doctor_ID='{}' and Date='{}';".format(
                Time, docID, Date)
            cursor.execute(query)
            cursor.execute("commit")
            return 0

    # Confirming the Appointment
    def insertAptmnt(self, Phone_Number, docID, Date, Slot):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "insert into aptmnt(Patient_ID,Doctor_ID,Date,Slot) values('{}','{}','{}','{}');".format(
            Phone_Number, docID, Date, Slot)
        cursor.execute(query)
        cursor.execute("commit")

    # Walk In Appointment Users(Patients)
    def addTempUser(self, p_Fname, p_Lname, Date, Gender, Phone_Number, Slot, docID):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "insert into temp_users(First_Name,Last_Name,Date_Of_Birth,Gender,Phone_Number,Slot,Date,Doctor_ID) values('{}','{}','{}','{}','{}','{}','{}','{}');".format(
            p_Fname, p_Lname, Date, Gender, Phone_Number, Slot, Date, docID)
        cursor.execute(query)
        cursor.execute("commit")

    # Delete all old Appointments
    def delete_old_aptmnt(self, Date):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "delete from aptmnt where Date<'{}';".format(Date)
        cursor.execute(query)
        query = "delete from slots where Date<'{}';".format(Date)
        cursor.execute(query)
        query = "delete from temp_users where Date<'{}';".format(Date)
        cursor.execute(query)
        cursor.execute("commit")

    # Cancel Appointment
    def delete_aptmnt(self, Aptmnt_ID, docID, Date, Time, phno, slot):
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "delete from aptmnt where Aptmnt_ID='{}';".format(Aptmnt_ID)
        cursor.execute(query)
        query = "update slots set Time='{}' where Doctor_ID='{}' and Date='{}';".format(
            Time, docID, Date)
        cursor.execute(query)
        query = "delete from temp_users where Phone_Number='{}' and Date='{}' and Doctor_ID='{}' and slot='{}';".format(
            phno, Date, docID, slot)
        cursor.execute(query)
        cursor.execute("commit")

    # Update the User Information
    def update_info(self, First_Name, Last_Name, NewPhno, OldPhno):  # Uflag
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "UPDATE aptmnt SET Patient_ID='{}' where Patient_ID='{}';".format(
            NewPhno, OldPhno)
        cursor.execute(query)
        cursor.execute("commit")

    # Verify whether the given Doctor ID is unique or not
    def check_new_docid(self, Doctor_ID):  # uflag
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select * from doctors where Doctor_ID='{}';".format(Doctor_ID)
        if (Doctor_ID == None):
            return -1
        cursor.execute(query)
        vari = cursor.fetchall()
        # If a doctor with the same ID already exists return 0 else 1
        if (len(vari) == 0):
            return 1
        else:
            return 0

    # Returns ID,Name and Specialization of the Doctor
    def showDoctors(self):  # uflag
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = ("select Doctor_ID,First_Name,Last_Name,Specialization from doctors;")
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    # Returns the Information about a Doctor to autofill delete and update Doctor modals
    def getDoctor(self, doctorID):  # uflag
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "select * from doctors where Doctor_ID='{}';".format(doctorID)
        cursor.execute(query)
        row = cursor.fetchall()
        return row

    # Add a New Doctor
    def addDoc(self, Doctor_ID, Fname, Lname, spec, exp, Gender, edu):  # uflag
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = ("insert into doctors values('{}','{}','{}','{}','{}','{}','{}','{}');").format(
            Doctor_ID, Fname, Lname, spec, exp, Gender, edu, "Doctor"+Gender)
        cursor.execute(query)
        cursor.execute("commit")

    # Update the information of a Doctor
    def updateDoc(self, Doctor_ID, Fname, Lname, spec, exp, Gender, edu):  # uflag
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = ("update doctors set First_Name='{}',Last_Name='{}',Specialization='{}',Experience='{}',Gender='{}',Education='{}' where Doctor_ID='{}';").format(
            Fname, Lname, spec, exp, Gender, edu, Doctor_ID)
        cursor.execute(query)
        cursor.execute("commit")

    # Delete a Doctor
    def deleteDoc(self, doctorID):  # uflag
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        query = "delete from doctors where Doctor_ID='{}';".format(doctorID)
        cursor.execute(query)
        cursor.execute("commit")

    # Show Upcoming Appointments for the Receptionist
    def show_aptmnts(self, Date, speciality, identifier, Today, usersData):
        rowdata = ''
        for i in usersData:
            rowdata = rowdata+"Row('{}','{}','{}'),".format(i[0], i[1], i[2])
        if (rowdata[-1] == ','):
            rowdata = rowdata[:-1]
        cnx = mysql.connector.connect(
            host=DBhost, user=DBuser, password=DBpassword, database=DBname)
        cursor = cnx.cursor()
        if identifier == 0:
            query = "(select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d') as 'Date',aptmnt.Slot from aptmnt,doctors,(select column_0 as 'First_Name',column_1 as 'Last_Name',column_2 as 'Phone_Number' from (values {} ) as users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date>='{}') union (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number,Slot,Doctor_ID,Date from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date=users.Date and aptmnt.Slot=users.Slot and aptmnt.Doctor_ID=users.Doctor_ID and aptmnt.Date>='{}') order by Date,Slot,Aptmnt_ID".format(rowdata, Today, Today)
        elif identifier == 1:
            query = "(select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d') as 'Date',aptmnt.Slot from aptmnt,doctors,(select column_0 as 'First_Name',column_1 as 'Last_Name',column_2 as 'Phone_Number' from (values {} ) as users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and doctors.Specialization='{}' and aptmnt.Date>='{}') union (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number,Slot,Doctor_ID,Date from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date=users.Date and aptmnt.Slot=users.Slot and aptmnt.Doctor_ID=users.Doctor_ID and doctors.Specialization='{}' and aptmnt.Date>='{}') order by Date,Slot,Aptmnt_ID".format(rowdata, speciality, Today, speciality, Today)
        elif identifier == 2:
            query = "(select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d') as 'Date',aptmnt.Slot from aptmnt,doctors,(select column_0 as 'First_Name',column_1 as 'Last_Name',column_2 as 'Phone_Number' from (values {} ) as users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date='{}' and aptmnt.Date>='{}') union (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number,Slot,Doctor_ID,Date from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date=users.Date and aptmnt.Slot=users.Slot and aptmnt.Doctor_ID=users.Doctor_ID and aptmnt.Date='{}' and aptmnt.Date>='{}') order by Date,Slot,Aptmnt_ID".format(rowdata, Date, Today, Date, Today)
        elif identifier == 3:
            query = "(select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d') as 'Date',aptmnt.Slot from aptmnt,doctors,(select column_0 as 'First_Name',column_1 as 'Last_Name',column_2 as 'Phone_Number' from (values {} ) as users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date='{}' and doctors.Specialization='{}' and aptmnt.Date>='{}') union (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number,Slot,Doctor_ID,Date from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date=users.Date and aptmnt.Slot=users.Slot and aptmnt.Doctor_ID=users.Doctor_ID and aptmnt.Date='{}' and doctors.Specialization='{}' and aptmnt.Date>='{}') order by Date,Slot,Aptmnt_ID".format(rowdata, Date, speciality, Today, Date, speciality, Today)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

# select First_Name,Last_Name,Phone_Number from users
# (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,DATE_FORMAT(aptmnt.Date,'%Y-%m-%d') as 'Date',aptmnt.Slot from aptmnt,doctors,(select column_0 as 'First_Name',column_1 as 'Last_Name',column_2 as 'Phone_Number' from (values Row('abhiram','de','9676611699')) as users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date>='2022-12-05') union (select aptmnt.Aptmnt_ID,aptmnt.Doctor_ID,doctors.First_Name,doctors.Last_Name,doctors.Specialization,users.First_Name,users.Last_Name,aptmnt.Patient_ID,aptmnt.Date,aptmnt.Slot from aptmnt,doctors,(select First_Name,Last_Name,Phone_Number,Slot,Doctor_ID,Date from temp_users) as users where aptmnt.Doctor_ID=doctors.Doctor_ID and aptmnt.Patient_ID=users.Phone_Number and aptmnt.Date=users.Date and aptmnt.Slot=users.Slot and aptmnt.Doctor_ID=users.Doctor_ID and aptmnt.Date>='2022-12-05') order by Date,Slot,Aptmnt_ID

# select column_0 as 'First_Name',column_1 as 'Last_Name',column_2 as 'Phone_Number' from (values Row('abhiram','de','9676611698')) as users
