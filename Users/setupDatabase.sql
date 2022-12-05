-- Login to MySQL (mysql -u root -p)
CREATE DATABASE user;
USE user;

CREATE TABLE `users` (
  `Phone_Number` char(10) NOT NULL,
  `Password` char(56) NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Date_Of_Birth` Date NOT NULL,
  `Gender` varchar(6) NOT NULL,
  PRIMARY KEY (`Phone_Number`)
);