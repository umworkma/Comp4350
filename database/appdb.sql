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
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address` (
  `PK` int(11) NOT NULL AUTO_INCREMENT,
  `address1` varchar(45) DEFAULT NULL,
  `address2` varchar(45) DEFAULT NULL,
  `address3` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `province` varchar(45) DEFAULT NULL,
  `country` varchar(45) DEFAULT NULL,
  `postalcode` varchar(45) DEFAULT NULL,
  `entityFK` int(11) NOT NULL,
  `isprimary` int(11) DEFAULT NULL COMMENT '0 = False\\n1 = True',
  PRIMARY KEY (`PK`),
  KEY `Address_Entity_FK_idx` (`entityFK`),
  CONSTRAINT `Address_Entity_FK` FOREIGN KEY (`entityFK`) REFERENCES `entity` (`pk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Physical address of an entity.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact` (
  `PK` int(11) NOT NULL AUTO_INCREMENT,
  `entityFK` int(11) NOT NULL,
  `type` int(11) DEFAULT '2' COMMENT '1 = phone\\n2 = email',
  `value` varchar(45) DEFAULT NULL COMMENT 'Email address text, phone number as text, etc.',
  `isprimary` int(11) DEFAULT '0' COMMENT '0 = false\\n1 = true',
  PRIMARY KEY (`PK`),
  KEY `Contact_Entity_IDX_idx` (`entityFK`),
  CONSTRAINT `Contact_Entity_IDX` FOREIGN KEY (`entityFK`) REFERENCES `entity` (`pk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Simple contact types for entities such as email or telephone.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `entity`
--

DROP TABLE IF EXISTS `entity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entity` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) DEFAULT '2' COMMENT '1 = Organization\\n2 = Person',
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Represents a person or organization, and is used to link addresses and contact methods to people and organizations.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `startdate` datetime DEFAULT NULL,
  `enddate` datetime DEFAULT NULL,
  `organizationFK` int(11) DEFAULT NULL,
  `eventcol` varchar(45) DEFAULT NULL,
  `eventcol1` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `Starting_Date` (`startdate`),
  KEY `Organization` (`organizationFK`),
  CONSTRAINT `Event_Organization` FOREIGN KEY (`organizationFK`) REFERENCES `organization` (`entityFK`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='An event held by one or more organizations which require workers to work shifts in a schedule.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member` (
  `personentityFK` int(11) NOT NULL,
  `organizationentityFK` int(11) NOT NULL,
  PRIMARY KEY (`personentityFK`,`organizationentityFK`),
  KEY `Member_Person_IDX_idx` (`personentityFK`),
  KEY `Member_Org_IDX_idx` (`organizationentityFK`),
  CONSTRAINT `Member_Person_IDX` FOREIGN KEY (`personentityFK`) REFERENCES `person` (`entityFK`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Member_Org_IDX` FOREIGN KEY (`organizationentityFK`) REFERENCES `organization` (`entityFK`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Bridging table defining a many-to-many relationship for people and organizations. i.e. a person may volunteer for multiple organizations, and may be a supervisor in some, and/or an administrator overall. An organizations obviously could have many volunteers and supervisors. This is intended to allow a single user authentication to provide access to all organizations, schedules, and features that a user is entitled to, without maintaining multiple sets of credentials.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `organization`
--

DROP TABLE IF EXISTS `organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `organization` (
  `entityFK` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`entityFK`),
  CONSTRAINT `Org_Entity_IDX` FOREIGN KEY (`entityFK`) REFERENCES `entity` (`pk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='A group or company that runs conferences/exhibitions requiring shift scheduling. For example, a schedule for an event/conference would be attached to an organization. This is currently not intended to represent exhibitors within a particular conference/exhibition.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `entityFK` int(11) NOT NULL,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `firstname` varchar(45) DEFAULT NULL,
  `lastname` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`entityFK`),
  CONSTRAINT `Person_Entity_IDX` FOREIGN KEY (`entityFK`) REFERENCES `entity` (`pk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Represents a person. This can be an employee attached to one or more organizations, a supervisor who creates schedules, or an administrator that manages organizations.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `preferredcoworkers`
--

DROP TABLE IF EXISTS `preferredcoworkers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `preferredcoworkers` (
  `pk` int(11) NOT NULL,
  `personFK` int(11) NOT NULL,
  `friendFK` int(11) NOT NULL,
  PRIMARY KEY (`pk`),
  KEY `Person_idx` (`personFK`),
  KEY `Freind_idx` (`friendFK`),
  CONSTRAINT `Pref_Person` FOREIGN KEY (`personFK`) REFERENCES `person` (`entityFK`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Pref_Freind` FOREIGN KEY (`friendFK`) REFERENCES `person` (`entityFK`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='People that the given person prefers to have shifts with.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shift`
--

DROP TABLE IF EXISTS `shift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shift` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `eventFK` int(11) NOT NULL,
  `startdatetime` datetime DEFAULT NULL,
  `enddatetime` datetime DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `minWorkers` int(11) DEFAULT '0',
  `maxWorkers` int(11) DEFAULT '0',
  PRIMARY KEY (`pk`),
  KEY `Event` (`eventFK`),
  CONSTRAINT `Shift_Event` FOREIGN KEY (`eventFK`) REFERENCES `event` (`pk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='A timeframe within an event that requires workers to work together on some task.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shift_person_bridge`
--

DROP TABLE IF EXISTS `shift_person_bridge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shift_person_bridge` (
  `shiftFK` int(11) NOT NULL,
  `personFK` int(11) NOT NULL,
  PRIMARY KEY (`shiftFK`,`personFK`),
  KEY `Bridge_Shift_idx` (`shiftFK`),
  KEY `Bridge_Person_idx` (`personFK`),
  CONSTRAINT `Bridge_Shift` FOREIGN KEY (`shiftFK`) REFERENCES `shift` (`pk`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Bridge_Person` FOREIGN KEY (`personFK`) REFERENCES `person` (`entityFK`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Bridging table for many-to-many relationship between Person and Shift. More than one person can work on one shift, and a person can work on more than one shift.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unavaildates`
--

DROP TABLE IF EXISTS `unavaildates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unavaildates` (
  `pk` int(11) NOT NULL,
  `personFK` int(11) NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `Person_idx` (`personFK`),
  CONSTRAINT `Person` FOREIGN KEY (`personFK`) REFERENCES `person` (`entityFK`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Dates where the specified person is not avaiable for shifts.';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-02-13 17:48:33
