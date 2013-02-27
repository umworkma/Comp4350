delimiter $$

DROP TABLE IF EXISTS `privileges`;$$
CREATE TABLE `privileges` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `privilege` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Lookup table of all application privileges.'$$


delimiter $$
DROP TABLE IF EXISTS `privileges_member_bridge`;$$
CREATE TABLE `privileges_member_bridge` (
  `pk` int(11) NOT NULL AUTO_INCREMENT,
  `personentityFK` int(11) NOT NULL,
  `privilegeFK` int(11) NOT NULL,
  `organizationentityFK` int(11) DEFAULT NULL,
  PRIMARY KEY (`pk`),
  KEY `privilege_idx` (`privilegeFK`),
  KEY `person_idx` (`personentityFK`),
  KEY `organization_member_idx` (`organizationentityFK`),
  CONSTRAINT `privileges` FOREIGN KEY (`privilegeFK`) REFERENCES `privileges` (`pk`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `person_member` FOREIGN KEY (`personentityFK`) REFERENCES `member` (`personentityFK`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `organization_member` FOREIGN KEY (`organizationentityFK`) REFERENCES `member` (`organizationentityFK`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Links privileges with specific individuals, allowing that individual to puse the given privilege. If an organization is not attached, then the privilege is global, but this is only valid if the feature that uses the privilege bahaves in that manner.'$$

