delimiter $$

DROP TABLE `shift_person_bridge`$$
CREATE TABLE `shift_person_bridge` (
  `pk` int(11) NOT NULL,
  `shiftFK` int(11) NOT NULL,
  `personFK` int(11) NOT NULL,
  PRIMARY KEY (`pk`),
  KEY `Bridge_Shift_idx` (`shiftFK`),
  KEY `Bridge_Person_idx` (`personFK`),
  CONSTRAINT `Bridge_Person` FOREIGN KEY (`personFK`) REFERENCES `person` (`entityFK`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Bridge_Shift` FOREIGN KEY (`shiftFK`) REFERENCES `shift` (`pk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Bridging table for many-to-many relationship between Person and Shift. More than one person can work on one shift, and a person can work on more than one shift.'$$

