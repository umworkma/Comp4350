-- MySQL dump 10.13  Distrib 5.5.29, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: appdb
-- ------------------------------------------------------
-- Server version	5.5.29-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (1,'1st Street','','','Winnipeg','Manitoba','Canada','R1A A1A',1,1),(2,'2nd Street','','','Winnipeg','Manitoba','Canada','B2B 2B2',2,1),(3,'3rd Street','','','Winnipeg','Manitoba','Canada','C3C 3C3',3,1),(4,'4th Street','','','Winnipeg','Manitoba','Canada','D4D 4D4',4,1),(5,'5th Street','','','Winnipeg','Manitoba','Canada','E5E 5E5',5,1),(6,'6th Street','','','Winnipeg','Manitoba','Canada','F6F 6F6',6,1),(7,'No fixed address','','','Winnipeg','Manitoba','Canada','R0H 0H0',7,1),(8,'55 Broadway','25th Floor','','New York','New York','United States','10006',8,1);
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (1,1,1,'204-555-1111',1),(2,1,2,'umnelso3@cc.umanitoba.ca',0),(3,2,1,'204-555-2222',1),(4,2,2,'umworkma@cc.umanitoba.ca',0),(5,3,1,'204-555-3333',1),(6,3,2,'umsungkf@cc.umanitoba.ca',0),(7,4,1,'204-555-4444',1),(8,4,2,'umcarrier@cc.umanitoba.ca',0),(9,5,1,'204-555-5555',1),(10,5,2,'umbetchaku@cc.umanitoba.ca',0),(11,6,1,'204-555-6666',1),(12,6,2,'umgalon@cc.umanitoba.ca',0),(13,7,1,'204-555-1234',1),(14,7,2,'info@ai-kon.org',0),(15,8,1,'1-866-364-2733',1),(16,8,2,'customer-service@fogcreek.com',0);
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `entity`
--

LOCK TABLES `entity` WRITE;
/*!40000 ALTER TABLE `entity` DISABLE KEYS */;
INSERT INTO `entity` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1);
/*!40000 ALTER TABLE `entity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'Ai-kon 2013','Summer 2013. Anime convention including movie screenings, art exhibitions, cosplay contests, and more!','2013-07-12 10:00:00','2013-07-14 15:00:00',7,NULL,NULL),(2,'Ai-kon 2013 (Winter)','Annual get-together in December.','2013-12-13 10:00:00','2013-12-15 14:00:00',7,NULL,NULL),(3,'CodeConf 2013','Coding convention!','2013-04-25 18:00:00','2013-04-26 20:00:00',8,NULL,NULL);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,1,7),(2,1,8),(3,2,7),(4,3,7),(5,3,8),(6,4,8),(7,5,8),(8,6,7),(9,6,8);
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `organization`
--

LOCK TABLES `organization` WRITE;
/*!40000 ALTER TABLE `organization` DISABLE KEYS */;
INSERT INTO `organization` VALUES (7,'Ai-kon','Ai-kon organizaes an annual convention for anime enthusiasts. Volunteers are needed to make each convention a success!'),(8,'Fog Creek Software','Makers of agile project tracking software.');
/*!40000 ALTER TABLE `organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES (1,'Dan','Nelson','Dan','password'),(2,'Chris','Workman','Chris','password'),(3,'William','Sung','Billiam','password'),(4,'Diana','Carrier','Diana','password'),(5,'Ryoji','Betchaku','Ryoji','password'),(6,'Melanie','Galon','Mel','password');
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `privilege`
--

LOCK TABLES `privilege` WRITE;
/*!40000 ALTER TABLE `privilege` DISABLE KEYS */;
INSERT INTO `privilege` VALUES (1,'Create Organizations'),(2,'Edit Organizations'),(3,'Grant Privileges'),(4,'Revoke Privileges'),(5,'Create Events'),(6,'Assign Volunteers To Shifts'),(7,'Remove Volunteers From Shifts');
/*!40000 ALTER TABLE `privilege` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `privilege_member_bridge`
--

LOCK TABLES `privilege_member_bridge` WRITE;
/*!40000 ALTER TABLE `privilege_member_bridge` DISABLE KEYS */;
INSERT INTO `privilege_member_bridge` VALUES (2,1,3),(3,1,4),(4,1,5),(5,1,6),(6,1,7),(7,3,5),(8,3,6),(9,3,7),(10,1,2),(11,4,1),(12,4,4),(13,4,3),(14,4,2),(15,8,5),(16,8,6),(17,8,7),(18,2,7),(19,2,5),(20,2,6),(21,5,1),(22,5,2),(23,5,3),(24,5,4),(25,6,3),(26,6,4),(27,7,7),(28,7,6),(30,9,5),(31,9,6),(32,9,7);
/*!40000 ALTER TABLE `privilege_member_bridge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `privilege_person_bridge`
--

LOCK TABLES `privilege_person_bridge` WRITE;
/*!40000 ALTER TABLE `privilege_person_bridge` DISABLE KEYS */;
/*!40000 ALTER TABLE `privilege_person_bridge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `shift`
--

LOCK TABLES `shift` WRITE;
/*!40000 ALTER TABLE `shift` DISABLE KEYS */;
INSERT INTO `shift` VALUES (1,1,'2013-07-12 10:00:00','2013-07-12 11:00:00','location',1,999),(2,1,'2013-07-12 11:00:00','2013-07-12 12:00:00','location',1,999),(3,1,'2013-07-12 12:00:00','2013-07-12 13:00:00','location',1,999),(4,1,'2013-07-12 13:00:00','2013-07-12 14:00:00','location',1,999),(5,1,'2013-07-12 14:00:00','2013-07-12 15:00:00','location',1,999),(6,1,'2013-07-13 10:00:00','2013-07-13 11:00:00','location',1,999),(7,1,'2013-07-13 11:00:00','2013-07-13 12:00:00','location',1,999),(8,1,'2013-07-13 12:00:00','2013-07-13 13:00:00','location',1,999),(9,1,'2013-07-13 13:00:00','2013-07-13 14:00:00','location',1,999),(10,1,'2013-07-13 14:00:00','2013-07-13 15:00:00','location',1,999),(11,1,'2013-07-14 10:00:00','2013-07-14 11:00:00','location',1,999),(12,1,'2013-07-14 11:00:00','2013-07-14 12:00:00','location',1,999),(13,1,'2013-07-14 12:00:00','2013-07-14 13:00:00','location',1,999),(14,1,'2013-07-14 13:00:00','2013-07-14 14:00:00','location',1,999),(15,1,'2013-07-14 14:00:00','2013-07-14 15:00:00','location',1,999),(16,2,'2013-12-13 10:00:00','2013-12-13 11:00:00','location',1,999),(17,2,'2013-12-13 11:00:00','2013-12-13 12:00:00','location',1,999),(18,2,'2013-12-13 12:00:00','2013-12-13 13:00:00','location',1,999),(19,2,'2013-12-13 13:00:00','2013-12-13 14:00:00','location',1,999),(20,2,'2013-12-14 10:00:00','2013-12-14 11:00:00','location',1,999),(21,2,'2013-12-14 11:00:00','2013-12-14 12:00:00','location',1,999),(22,2,'2013-12-14 12:00:00','2013-12-14 13:00:00','location',1,999),(23,2,'2013-12-14 13:00:00','2013-12-14 14:00:00','location',1,999),(24,2,'2013-12-15 10:00:00','2013-12-15 11:00:00','location',1,999),(25,2,'2013-12-15 11:00:00','2013-12-15 12:00:00','location',1,999),(26,2,'2013-12-15 12:00:00','2013-12-15 13:00:00','location',1,999),(27,2,'2013-12-15 13:00:00','2013-12-15 14:00:00','location',1,999),(28,3,'2013-04-25 18:00:00','2013-04-25 19:00:00','location',1,999),(29,3,'2013-04-25 19:00:00','2013-04-25 20:00:00','location',1,999),(30,3,'2013-04-26 18:00:00','2013-04-26 19:00:00','location',1,999),(31,3,'2013-04-26 19:00:00','2013-04-26 20:00:00','location',1,999);
/*!40000 ALTER TABLE `shift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `shift_person_bridge`
--

LOCK TABLES `shift_person_bridge` WRITE;
/*!40000 ALTER TABLE `shift_person_bridge` DISABLE KEYS */;
INSERT INTO `shift_person_bridge` VALUES (1,1,1),(2,1,3),(3,2,6),(4,2,2),(5,3,2),(6,3,1),(7,3,6),(9,4,1);
/*!40000 ALTER TABLE `shift_person_bridge` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-24 17:59:42
