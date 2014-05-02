LOCK TABLES `entity` WRITE;
/*!40000 ALTER TABLE `entity` DISABLE KEYS */;
INSERT INTO `entity` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1);
/*!40000 ALTER TABLE `entity` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES (1,'F. Demo','L. Demo','demo','demo'),(5,'Chris','Workman','user0','password0'),(6,'R','B','user1','password1'),(7,'Dan','Nelson','user2','password2');
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (1,1,1,NULL,1),(2,1,2,'demo@demo.demo',0),(3,2,1,'204-474-9341',1),(4,2,2,'demo@email.com',0),(5,3,1,'18004321960',1),(6,3,2,'info@cc.umanitoba.ca',0),(7,4,1,'204-123-4567',1),(8,4,2,'info@ai-kon.org',0),(9,5,1,NULL,1),(10,5,2,'umworkma@cc.umanitoba.ca',0),(11,6,1,NULL,1),(12,6,2,'rb@ryoji.com',0),(13,7,1,NULL,1),(14,7,2,'dan@nelson.ca',0);
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (1,'demo st','','','comp4350','www','CS','A1B2C3',1,1),(2,'E2-350','EITC','','Winnipeg','Manitoba','Canada','R3T2N2',2,1),(3,'66 Chancellors Circle','','','Winnipeg','Manitoba','Canada','R3T2N2',3,1),(4,'123 Vroom Street','','','Winnipeg','Manitoba','Canada','A1A1A1',4,1),(5,'2116 - 991D Markham Rd','','','Winnipeg','Manitoba','Canada','R3K 5J1',5,1),(6,'2194 Pembina Hwy','','','Winnipeg','Manitoba','Canada','R1G 5V4',6,1),(7,'123 Main St','','','Selkirk','Manitoba','Canada','1V1 F2F',7,1);
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `privilege` WRITE;
/*!40000 ALTER TABLE `privilege` DISABLE KEYS */;
INSERT INTO `privilege` VALUES (1,'REGISTER NEW ORGANIZATION'),(2,'MODIFY ORGANIZATION'),(3,'DELETE ORGANIZATION'),(4,'VIEW ALL ORGANIZATIONS'),(5,'VIEW ALL EMPLOYEES IN ORG'),(6,'ASSIGN EMPS TO SHIFTS'),(7,'SOME OTHER EMP PRIVILEGE'),(8,'YET ANOTHER EMP PRIVILEGE');
/*!40000 ALTER TABLE `privilege` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `organization` WRITE;
/*!40000 ALTER TABLE `organization` DISABLE KEYS */;
INSERT INTO `organization` VALUES (2,'SE2 - Group 1','We make cool things.'),(3,'University of Manitoba','The University of Manitoba, is a public university in the province of Manitoba, Canada. Located in Winnipeg, it is Manitoba\'s largest, most comprehensive, and only research-intensive post-secondary educational institution.'),(4,'Ai-Kon','Ai-Kon Anime Convention');
/*!40000 ALTER TABLE `organization` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,1,2),(2,1,3),(3,1,4),(4,5,2),(5,5,3),(6,6,2),(7,6,4),(8,7,2),(9,7,3);
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `privilege_member_bridge` WRITE;
/*!40000 ALTER TABLE `privilege_member_bridge` DISABLE KEYS */;
INSERT INTO `privilege_member_bridge` VALUES (1,1,1),(2,1,2);
/*!40000 ALTER TABLE `privilege_member_bridge` ENABLE KEYS */;
UNLOCK TABLES;
