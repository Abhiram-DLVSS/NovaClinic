# Nova Clinic

This is a web application that helps health centers provide users with an easy way to book a doctor’s appointment online. It also allows the health centers to manage their appointments.

## Table of contents
- [Live Demo](#Live-Demo)
- [Technologies used](#Technologies-used)
- [Setup & Installation](#Setup--Installation)
- [Running The App](#Running-The-App)
- [Viewing The App](#Viewing-The-App)
## Live Demo

You can view our Web Application deployed on Heroku here:

- [NovaClinic](https://nova-clinic.herokuapp.com/)

## Technologies used
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [MySQL](https://www.mysql.com/)
- HTML
- CSS
- JavaScript

## Setup & Installation

Make sure you have Python and MySQL installed.

- Clone the repository
    ```bash
    git clone https://github.com/Abhiram-DLVSS/NovaClinic
    ```

- Install the required Python packages
    ```bash
    pip install -r requirements.txt
    ```

- Run the [setupDatabase.sql](setupDatabase.sql) script file in your MySQL terminal to create the Database (Database Name-nova)

    ```mysql
    mysql -u root -p
    source [Repository_Directory]//NovaClinic//setupDatabase.sql;
    ```

- Go to the "sqlhandler.py" file in NovaClinic/Application/DBHandler/


    Replace 
    ```py
    DB_URL = os.environ.get('CLEARDB_DATABASE_URL')
    DBhost=DB_URL[32:59]
    DBuser=DB_URL[8:22]
    DBpassword=DB_URL[23:31]
    DBname=DB_URL[60:82]
    ```
    with

    ```py
    DBhost='localhost'
    DBuser='root'
    DBpassword='YOUR_MySQL_PASSWORD'
    DBname='nova'
    ```

- Go to the "\_\_init__.py" file in NovaClinic/Application/

    Replace 
    ```py
    app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
    ```
    with
    ```py
    app.config['SECRET_KEY']="RandomSecretString"
    ```
    


## Running The App

```bash
python main.py
```

## Viewing The App

- [Welcome Page](http://127.0.0.1:5000/)
- [User's Homepage](http://127.0.0.1:5000/home)
    - Create a new account as a user
- [Receptionist Page](http://127.0.0.1:5000/receptionist)
    - Receptionist Credentials-
        Username:Nova001
        Password:Test@1234
- [Admin Page](http://127.0.0.1:5000/admin)
    - Admin Credentials-
        Username:Admin001
        Password:Test@1234
- Note:
    - One must logout from one portal(Admin,Receptionist,User) before visiting another
