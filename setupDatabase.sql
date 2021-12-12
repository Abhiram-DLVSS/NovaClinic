-- login to myql
CREATE DATABASE nova;
use nova;

-- Create Tables

CREATE TABLE `aptmnt` (
  `aptmnt_id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` char(10) NOT NULL,
  `doctor_id` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `slot` char(11) NOT NULL,
  PRIMARY KEY (`aptmnt_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `aptmnt_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`)
);


CREATE TABLE `doctors` (
  `doctor_id` varchar(10) NOT NULL,
  `FName` varchar(20) NOT NULL,
  `LName` varchar(20) NOT NULL,
  `doctor_specialization` varchar(20) NOT NULL,
  `doctor_experience` int(11) NOT NULL,
  `gender` varchar(6) NOT NULL,
  `doctor_education` varchar(40) NOT NULL,
  `doctor_image` varchar(20) NOT NULL,
  PRIMARY KEY (`doctor_id`)
);

CREATE TABLE `receptionists` (
  `recep_id` char(10) NOT NULL,
  `FName` varchar(20) NOT NULL,
  `LName` varchar(20) NOT NULL,
  `password` char(56) NOT NULL DEFAULT '43c21023f40197a9e0e122d3d191fb2c101f664bf4a1cb4ca886dff7',
  PRIMARY KEY (`recep_id`)
);


CREATE TABLE `slots` (
  `date` char(10) NOT NULL,
  `doctor_id` varchar(10) NOT NULL,
  `time` char(24) NOT NULL DEFAULT '000000000000000000000000',
  PRIMARY KEY (`date`,`doctor_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `slots_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`)
);


CREATE TABLE `temp_users` (
  `FName` varchar(20) NOT NULL,
  `LName` varchar(20) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(6) NOT NULL,
  `phno` char(10) NOT NULL,
  `slot` char(11) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`slot`,`date`,`phno`)
);


CREATE TABLE `users` (
  `phno` char(10) NOT NULL,
  `password` char(56) NOT NULL,
  `FName` varchar(20) NOT NULL,
  `LName` varchar(20) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(6) NOT NULL,
  PRIMARY KEY (`phno`)
);


CREATE TABLE `admin` (
  `admin_id` varchar(10) NOT NULL,
  `password` char(56) NOT NULL,
  `FName` varchar(20) NOT NULL,
  `LName` varchar(20) NOT NULL,
  PRIMARY KEY (`admin_id`)
);



-- Add Doctors
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc001','Hemant','Madan','Cardiology',20,'Male','M.D.,D.M','DoctorMale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc002','Subhash','Chandra','Cardiology',35,'Male','M.D.,D.M','DoctorMale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc003','Anantha','Subramaniam','General Physician',30,'Male','MBBS, DNB','DoctorMale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc004','Rohith','Batra','Dermatology',20,'Male','MBBS, MD','DoctorMale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc005','T.S.','Kanaka','Neurology',34,'Female','MBBS, MCh','DoctorFemale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc006','Gagan','Sabharwal','Dentist',25,'Male','BDS, MDS','DoctorMale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc007','Mukul','Varma','Neurology',26,'Male','MBBS, MS','DoctorMale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc008','Indira','Hinduja','General Physician',27,'Female','MBBS','DoctorFemale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc009','Kalpesh','Thakur','Dermatology',35,'Male','MBBS, MD','DoctorMale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc010','Tarun','Giroti','Dentist',38,'Male','BDS, MDS','DoctorMale');
INSERT INTO `` (`doctor_id`,`FName`,`LName`,`doctor_specialization`,`doctor_experience`,`gender`,`doctor_education`,`doctor_image`) VALUES ('Doc011','Padmavati','Iyer','General Physician',25,'Female','MBBS, DNB','DoctorFemale');

-- Add a Receptionist
INSERT INTO `` (`recep_id`,`FName`,`LName`,`password`) VALUES ('Nova001','Clawhauser','O',Sha2('Test@1234',224));

-- Add a Admin
INSERT INTO `nova`.`admin` (`admin_id`, `password`, `FName`, `LName`) VALUES ('Admin001',Sha2('Test@1234',224),'Elliot','Alderson');
