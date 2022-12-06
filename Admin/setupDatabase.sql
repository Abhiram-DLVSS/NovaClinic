-- Login to MySQL (mysql -u root -p)
CREATE DATABASE nova;
USE nova;

-- Create Tables

CREATE TABLE `receptionists` (
  `Recep_ID` char(10) NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Password` char(56) NOT NULL DEFAULT '43c21023f40197a9e0e122d3d191fb2c101f664bf4a1cb4ca886dff7',
  PRIMARY KEY (`Recep_ID`)
);

CREATE TABLE `admin` (
  `Admin_ID` varchar(10) NOT NULL,
  `Password` char(56) NOT NULL,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  PRIMARY KEY (`Admin_ID`)
);

-- Add a Receptionist
INSERT INTO `nova`.`receptionists` (`Recep_ID`,`First_Name`,`Last_Name`,`Password`) VALUES ('Nova001','Clawhauser','O',Sha2('Test@1234',224));

-- Add a Admin
INSERT INTO `nova`.`admin` (`Admin_ID`, `Password`, `First_Name`, `Last_Name`) VALUES ('Admin001',Sha2('Test@1234',224),'Elliot','Alderson');