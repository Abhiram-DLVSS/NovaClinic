-- Login to MySQL (mysql -u root -p)
CREATE DATABASE nova;
USE nova;

-- Create Tables
CREATE TABLE `doctors` (
  `Doctor_ID` varchar(10) NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Specialization` varchar(20) NOT NULL,
  `Experience` int NOT NULL,
  `Gender` varchar(6) NOT NULL,
  `Education` varchar(40) NOT NULL,
  `Image` varchar(20) NOT NULL,
  PRIMARY KEY (`Doctor_ID`)
);

CREATE TABLE `aptmnt` (
  `Aptmnt_ID` int NOT NULL AUTO_INCREMENT,
  `Patient_ID` char(10) NOT NULL,
  `Doctor_ID` varchar(10) NOT NULL,
  `Date` Date NOT NULL,
  `Slot` char(11) NOT NULL,
  PRIMARY KEY (`Aptmnt_ID`),
  KEY `Doctor_ID` (`Doctor_ID`),
  CONSTRAINT `aptmnt_ibfk_2` FOREIGN KEY (`Doctor_ID`) REFERENCES `doctors` (`Doctor_ID`)
);

CREATE TABLE `receptionists` (
  `Recep_ID` char(10) NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Password` char(56) NOT NULL DEFAULT '43c21023f40197a9e0e122d3d191fb2c101f664bf4a1cb4ca886dff7',
  PRIMARY KEY (`Recep_ID`)
);

CREATE TABLE `slots` (
  `Date` char(10) NOT NULL,
  `Doctor_ID` varchar(10) NOT NULL,
  `Time` char(24) NOT NULL DEFAULT '000000000000000000000000',
  PRIMARY KEY (`Date`,`Doctor_ID`),
  KEY `Doctor_ID` (`Doctor_ID`),
  CONSTRAINT `slots_ibfk_1` FOREIGN KEY (`Doctor_ID`) REFERENCES `doctors` (`Doctor_ID`)
);

CREATE TABLE `temp_users` (
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Date_Of_Birth` Date NOT NULL,
  `Gender` varchar(6) NOT NULL,
  `Phone_Number` char(10) NOT NULL,
  `Slot` char(11) NOT NULL,
  `Date` Date NOT NULL,
  PRIMARY KEY (`Slot`,`Date`,`Phone_Number`)
);

CREATE TABLE `users` (
  `Phone_Number` char(10) NOT NULL,
  `Password` char(56) NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Date_Of_Birth` Date NOT NULL,
  `Gender` varchar(6) NOT NULL,
  PRIMARY KEY (`Phone_Number`)
);

CREATE TABLE `admin` (
  `Admin_ID` varchar(10) NOT NULL,
  `Password` char(56) NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  PRIMARY KEY (`Admin_ID`)
);

-- Add Doctors
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc001','Hemant','Madan','Cardiology',20,'Male','M.D.,D.M','DoctorMale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc002','Subhash','Chandra','Cardiology',35,'Male','M.D.,D.M','DoctorMale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc003','Anantha','Subramaniam','General Physician',30,'Male','MBBS, DNB','DoctorMale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc004','Rohith','Batra','Dermatology',20,'Male','MBBS, MD','DoctorMale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc005','T.S.','Kanaka','Neurology',34,'Female','MBBS, MCh','DoctorFemale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc006','Gagan','Sabharwal','Dentist',25,'Male','BDS, MDS','DoctorMale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc007','Mukul','Varma','Neurology',26,'Male','MBBS, MS','DoctorMale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc008','Indira','Hinduja','General Physician',27,'Female','MBBS','DoctorFemale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc009','Kalpesh','Thakur','Dermatology',35,'Male','MBBS, MD','DoctorMale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc010','Tarun','Giroti','Dentist',38,'Male','BDS, MDS','DoctorMale');
INSERT INTO `nova`.`doctors` (`Doctor_ID`,`First_Name`,`Last_Name`,`Specialization`,`Experience`,`Gender`,`Education`,`Image`) VALUES ('Doc011','Padmavati','Iyer','General Physician',25,'Female','MBBS, DNB','DoctorFemale');

-- Add a Receptionist
INSERT INTO `nova`.`receptionists` (`Recep_ID`,`First_Name`,`Last_Name`,`Password`) VALUES ('Nova001','Clawhauser','O',Sha2('Test@1234',224));

-- Add a Admin
INSERT INTO `nova`.`admin` (`Admin_ID`, `Password`, `First_Name`, `Last_Name`) VALUES ('Admin001',Sha2('Test@1234',224),'Elliot','Alderson');