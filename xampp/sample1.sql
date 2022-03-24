CREATE DATABASE IF NOT EXISTS test;

USE test;

DROP TABLE IF EXISTS sample1;

CREATE TABLE `sample1` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `DATE` varchar(10) ,
  `DESCRIPTION` varchar(200),
  `ORIGINAL_DESCRIPTION` varchar(200) ,
  `AMOUNT` varchar(30) ,
  `TRANSACTION_TYPE` varchar(10) ,
  `CATEGORY` varchar(100) ,
  `ACCOUNT_NAME` varchar(100) ,
  `LABELS` varchar(100) ,
  `NOTES` varchar(100) 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

