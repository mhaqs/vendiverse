-- MySQL dump 10.13  Distrib 5.5.54, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: macgal
-- ------------------------------------------------------
-- Server version	5.5.54-0+deb8u1

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
-- Table structure for table `_day`
--

DROP TABLE IF EXISTS `_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `_day` (
  `no` int(2) unsigned DEFAULT NULL,
  `dow` int(2) unsigned DEFAULT NULL,
  `d` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `_day`
--

LOCK TABLES `_day` WRITE;
/*!40000 ALTER TABLE `_day` DISABLE KEYS */;
INSERT INTO `_day` VALUES (1,2,'Pazartesi'),(2,3,'Sali'),(3,4,'Carsamba'),(4,5,'Persembe'),(5,6,'Cuma'),(6,7,'Cumartesi'),(7,1,'Pazar');
/*!40000 ALTER TABLE `_day` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `_hour`
--

DROP TABLE IF EXISTS `_hour`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `_hour` (
  `no` int(2) unsigned DEFAULT NULL,
  `h` int(2) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `_hour`
--

LOCK TABLES `_hour` WRITE;
/*!40000 ALTER TABLE `_hour` DISABLE KEYS */;
INSERT INTO `_hour` VALUES (1,8),(2,9),(3,10),(4,11),(5,12),(6,13),(7,14),(8,15),(9,16),(10,17),(11,18),(12,19),(13,20),(14,21),(15,22),(16,23),(17,0),(18,1),(19,2),(20,3),(21,4),(22,5),(23,6),(24,7);
/*!40000 ALTER TABLE `_hour` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `_month`
--

DROP TABLE IF EXISTS `_month`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `_month` (
  `no` int(2) unsigned NOT NULL,
  `m` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `_month`
--

LOCK TABLES `_month` WRITE;
/*!40000 ALTER TABLE `_month` DISABLE KEYS */;
INSERT INTO `_month` VALUES (1,'Ocak'),(2,'Subat'),(3,'Mart'),(4,'Nisan'),(5,'Mayis'),(6,'Haziran'),(7,'Temmuz'),(8,'Agustos'),(9,'Eylul'),(10,'Ekim'),(11,'Kasim'),(12,'Aralik');
/*!40000 ALTER TABLE `_month` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parameter`
--

DROP TABLE IF EXISTS `parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parameter` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `detail` varchar(60) NOT NULL,
  `type` int(1) unsigned NOT NULL,
  `value` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameter`
--

LOCK TABLES `parameter` WRITE;
/*!40000 ALTER TABLE `parameter` DISABLE KEYS */;
INSERT INTO `parameter` VALUES (1,'PRODSUBS','Rafta urun yoksa baska raftan ver',1,'1'),(2,'SALESOUND','Satis yapilinca ses cal',1,'0'),(3,'MULTISALE','Bakiye varsa satisa devam et',1,'0'),(4,'NOCOINSALE','Para ustu yoksa satis yapma',1,'0'),(5,'NOCOINWARN','Para ustu yoksa uyar',1,'1'),(6,'MAINCLOCK','Ana ekranda saat goster',1,'1'),(7,'MAINDATE','Ana ekranda tarih goster',1,'1'),(8,'MAINMODEL','Ana ekranda marka/model goster',1,'1'),(9,'PIRSOUND','Hareket alg?laninca ses cal',1,'0'),(10,'COINSOUND','Para atilinca ses cal',1,'0'),(11,'MAXTEMP1','Birinci sensor ust sicaklik',2,'10'),(12,'MINTEMP1','Birinci sensor alt sicaklik',2,'3'),(13,'MAXTEMP2','Ikinci sensor ust sicaklik',2,'8'),(14,'MINTEMP2','Ikinci sensor alt sicaklik',2,'3'),(15,'MEANTEMP','Hedeflenen ortalama sicaklik',2,'5');
/*!40000 ALTER TABLE `parameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `barcode` varchar(20) NOT NULL,
  `price` decimal(5,2) DEFAULT NULL,
  `vat` int(2) unsigned DEFAULT '0',
  `active` int(1) unsigned DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'COCA COLA KUTU 330cc','123456789',1.00,0,1),(2,'COCA COLA LIGHT KUTU 330cc','',1.75,0,1),(3,'COCA COLA ZERO KUTU 330cc','',1.75,0,1),(4,'NESTEA SEFTALI 330cc','',1.50,0,1),(5,'NESTEA LIMON 330cc','',1.50,0,1),(6,'DAMLA SU 500ml','',1.00,0,1),(7,'TADELLE CIKOLATA','',1.00,0,1),(8,'TADELLE BEYAZ CIKOLATA','',1.00,0,1),(9,'ULKER CUBUK KRAKER','',0.75,0,1),(10,'ULKER HAYLAYF','',1.00,0,1);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale`
--

DROP TABLE IF EXISTS `sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sale` (
  `id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(6) unsigned NOT NULL,
  `shelf_id` int(6) unsigned NOT NULL,
  `price` decimal(5,2) NOT NULL,
  `sale_dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `balance` decimal(5,2) NOT NULL,
  `remaining` decimal(5,2) NOT NULL,
  `sale_type` int(2) unsigned NOT NULL,
  `success` int(2) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale`
--

LOCK TABLES `sale` WRITE;
/*!40000 ALTER TABLE `sale` DISABLE KEYS */;
INSERT INTO `sale` VALUES (2,1,1,3.00,'2017-04-23 10:49:36',3.00,0.00,1,1),(3,1,1,1.00,'2017-04-23 11:05:07',2.00,1.00,1,1),(4,1,1,1.00,'2017-04-23 11:10:29',2.00,1.00,1,1),(5,1,1,1.00,'2017-04-23 11:13:19',2.00,1.00,1,1),(6,1,1,1.00,'2017-04-23 11:18:30',2.00,1.00,1,1),(7,1,1,1.00,'2017-04-23 11:19:14',2.00,1.00,1,1),(8,1,1,1.00,'2017-04-23 11:21:37',1.50,0.50,1,1),(9,1,1,1.00,'2017-04-23 11:30:54',2.00,1.00,1,1),(10,1,1,1.00,'2017-04-23 11:32:31',1.75,0.75,1,1),(11,1,1,1.00,'2017-04-23 11:33:31',1.75,0.75,1,1),(12,1,1,1.00,'2017-04-23 11:36:22',1.75,0.75,1,1),(13,1,1,1.00,'2017-04-23 11:37:33',1.75,0.75,1,1),(14,1,1,1.00,'2017-04-23 11:39:51',1.75,0.75,1,1),(15,1,1,1.00,'2017-04-23 11:41:10',1.75,0.75,1,1),(16,1,1,1.00,'2017-04-23 11:42:19',2.75,1.75,1,1),(17,1,1,1.00,'2017-04-23 12:15:28',1.50,0.50,1,1),(18,1,1,1.00,'2017-04-23 13:59:50',1.75,0.75,1,1),(19,1,1,1.50,'2017-04-23 15:47:07',1.75,0.25,1,1),(20,1,1,1.50,'2017-04-23 16:24:45',3.75,2.25,1,1),(21,1,1,1.50,'2017-04-23 17:38:48',6.50,5.00,1,1),(23,1,1,1.50,'2017-04-23 21:25:47',2.00,0.50,1,1),(24,1,1,1.50,'2017-04-24 13:19:52',2.00,0.50,1,1),(25,8,9,1.00,'2017-04-24 13:51:03',1.75,0.75,1,1),(26,6,7,1.00,'2017-04-24 14:01:09',2.00,1.00,1,1),(27,1,1,2.00,'2017-04-24 16:01:19',2.00,0.00,1,1),(28,2,3,1.75,'2017-04-24 16:01:36',2.00,0.25,1,1),(29,5,6,1.50,'2017-04-24 19:22:13',2.00,0.50,1,1),(30,5,6,1.50,'2017-04-24 19:23:48',2.00,0.50,1,1),(31,6,7,1.00,'2017-04-24 12:48:21',2.00,1.00,1,1),(32,5,6,1.50,'2017-04-24 12:56:54',2.00,0.50,1,1),(33,5,6,1.50,'2017-04-24 15:50:31',3.00,1.50,1,1),(34,5,6,1.50,'2017-04-24 15:51:31',1.50,0.00,1,1),(35,4,5,1.50,'2017-04-24 15:52:06',1.50,0.00,1,1),(36,7,8,1.00,'2017-04-24 15:52:29',1.50,0.50,1,1),(37,5,6,1.50,'2017-04-24 16:13:06',1.50,0.00,1,1),(38,2,3,1.75,'2017-04-24 16:17:00',2.00,0.25,1,1),(39,1,1,1.00,'2017-04-24 16:19:20',1.00,0.00,1,1),(40,1,1,1.00,'2017-04-24 16:28:19',1.00,0.00,1,1),(41,1,1,1.00,'2017-04-24 16:28:42',1.00,0.00,1,1),(42,1,1,1.00,'2017-04-24 16:30:45',1.00,0.00,1,1),(44,1,1,1.00,'2017-04-24 16:32:09',1.50,0.50,1,1),(45,1,1,1.00,'2017-04-24 12:47:35',1.00,0.00,1,1),(46,1,1,1.00,'2017-04-24 13:19:31',1.00,0.00,1,1),(47,1,1,1.00,'2017-04-24 13:00:37',1.00,0.00,1,1);
/*!40000 ALTER TABLE `sale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shelf`
--

DROP TABLE IF EXISTS `shelf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shelf` (
  `id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `shelf_no` varchar(3) NOT NULL,
  `rack_id` int(6) unsigned NOT NULL,
  `product_id` int(6) unsigned NOT NULL,
  `remaining` int(2) unsigned DEFAULT '0',
  `capacity` int(2) unsigned NOT NULL,
  `expire_dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `active` int(1) unsigned DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shelf`
--

LOCK TABLES `shelf` WRITE;
/*!40000 ALTER TABLE `shelf` DISABLE KEYS */;
INSERT INTO `shelf` VALUES (1,'10',1,1,2,6,'2017-04-24 13:00:37',1),(2,'11',1,1,6,6,'2017-04-23 20:58:14',1),(3,'12',1,2,4,6,'2017-04-24 16:17:00',1),(4,'13',1,3,6,6,'2017-04-23 20:58:14',1),(5,'14',1,4,5,6,'2017-04-24 15:52:06',1),(6,'15',1,5,0,6,'2017-04-24 16:13:06',1),(7,'16',1,6,4,6,'2017-04-24 12:48:21',1),(8,'17',1,7,5,6,'2017-04-24 15:52:29',1),(9,'18',1,8,19,20,'2017-04-24 13:51:03',1),(10,'19',1,9,20,20,'2017-04-23 20:58:30',1),(11,'20',1,10,20,20,'2017-04-23 20:58:30',1);
/*!40000 ALTER TABLE `shelf` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-24 15:32:31
