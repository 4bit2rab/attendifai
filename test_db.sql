CREATE DATABASE  IF NOT EXISTS `attendifai_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `attendifai_db`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: attendifai_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity_threshold`
--

DROP TABLE IF EXISTS `activity_threshold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_threshold` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idle_time_out` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_activity_threshold_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_threshold`
--

LOCK TABLES `activity_threshold` WRITE;
/*!40000 ALTER TABLE `activity_threshold` DISABLE KEYS */;
INSERT INTO `activity_threshold` VALUES (1,10);
/*!40000 ALTER TABLE `activity_threshold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `employee_id` varchar(50) NOT NULL,
  `employee_name` varchar(100) DEFAULT NULL,
  `employee_email` varchar(100) DEFAULT NULL,
  `employee_phone` varchar(20) NOT NULL,
  `shift_code` varchar(30) NOT NULL,
  PRIMARY KEY (`employee_id`),
  UNIQUE KEY `ix_employee_employee_phone` (`employee_phone`),
  UNIQUE KEY `ix_employee_employee_email` (`employee_email`),
  KEY `ix_employee_employee_name` (`employee_name`),
  KEY `ix_employee_employee_id` (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES ('6dfc4dfd-d6f7-41ff-904b-3f3ca5414f2','Angel','angel@gmail.com','234567891','M-123'),('6dfc4dfd-d6f7-41ff-904b-3f3ca5414f44','John','john@gmail.com','9876543211','M-456'),('6dfc4dfd-d6f7-41ff-904b-3f3ca5414hsbd','Mary','mary@gmail.com','2637257388','M-123');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_activity_log`
--

DROP TABLE IF EXISTS `employee_activity_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_activity_log` (
  `employee_id` varchar(50) NOT NULL,
  `log_date` date NOT NULL,
  `productive_time` int NOT NULL,
  `idle_time` int NOT NULL,
  `over_time` int NOT NULL,
  `overtime_approval` tinyint(1) DEFAULT NULL,
  `per_day_base_salary` int NOT NULL,
  PRIMARY KEY (`employee_id`,`log_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_activity_log`
--

LOCK TABLES `employee_activity_log` WRITE;
/*!40000 ALTER TABLE `employee_activity_log` DISABLE KEYS */;
INSERT INTO `employee_activity_log` VALUES ('6dfc4dfd-d6f7-41ff-904b-3f3ca5414f2','2026-01-01',8000,3000,2000,1,401),('6dfc4dfd-d6f7-41ff-904b-3f3ca5414f2','2026-01-02',10000,500,2000,1,518),('6dfc4dfd-d6f7-41ff-904b-3f3ca5414f44','2026-01-01',9000,3000,0,0,250),('6dfc4dfd-d6f7-41ff-904b-3f3ca5414f44','2026-01-02',7000,2000,3000,1,360);
/*!40000 ALTER TABLE `employee_activity_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_base_salary`
--

DROP TABLE IF EXISTS `employee_base_salary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_base_salary` (
  `employee_id` varchar(50) NOT NULL,
  `hourly_salary` float NOT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_base_salary`
--

LOCK TABLES `employee_base_salary` WRITE;
/*!40000 ALTER TABLE `employee_base_salary` DISABLE KEYS */;
INSERT INTO `employee_base_salary` VALUES ('6dfc4dfd-d6f7-41ff-904b-3f3ca5414f2',120),('6dfc4dfd-d6f7-41ff-904b-3f3ca5414f44',100);
/*!40000 ALTER TABLE `employee_base_salary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_token`
--

DROP TABLE IF EXISTS `employee_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_token` (
  `token` varchar(255) NOT NULL,
  `employee_id` varchar(50) DEFAULT NULL,
  `created_at` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`token`),
  KEY `ix_employee_token_employee_id` (`employee_id`),
  KEY `ix_employee_token_token` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_token`
--

LOCK TABLES `employee_token` WRITE;
/*!40000 ALTER TABLE `employee_token` DISABLE KEYS */;
INSERT INTO `employee_token` VALUES ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbXBsb3llZV9pZCI6IjZkZmM0ZGZkLWQ2ZjctNDFmZi05MDRiLTNmM2NhNTQxNGY0NCJ9.44uGacKNRaExr9xPibB0_x-cIWj1NgbBqBf8ksJBK3w','6dfc4dfd-d6f7-41ff-904b-3f3ca5414f44','2025-12-30 07:28:56.191474');
/*!40000 ALTER TABLE `employee_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager_details`
--

DROP TABLE IF EXISTS `manager_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager_details` (
  `manager_id` varchar(50) NOT NULL,
  `manager_name` varchar(100) DEFAULT NULL,
  `manager_email` varchar(100) NOT NULL,
  `manager_phone` varchar(20) NOT NULL,
  `department` varchar(100) NOT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`manager_id`),
  UNIQUE KEY `ix_manager_details_manager_email` (`manager_email`),
  UNIQUE KEY `ix_manager_details_manager_phone` (`manager_phone`),
  KEY `ix_manager_details_manager_id` (`manager_id`),
  KEY `ix_manager_details_manager_name` (`manager_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_details`
--

LOCK TABLES `manager_details` WRITE;
/*!40000 ALTER TABLE `manager_details` DISABLE KEYS */;
INSERT INTO `manager_details` VALUES ('39e44add-beb5-4705-8855-04dd0a6a5eb5','ann','ann@gmail.com','2345678221','IT','$argon2id$v=19$m=65536,t=3,p=4$KAVAiPGe815LiTGm9N57rw$5vVlc5iOQZ/EqwUg+D4MD3Mw1sf7rtCuQMjKXLY1xD8'),('d4373448-9deb-40a0-a9f0-5e1d1b0e3607','Harry','harry@gmail.com','2345678901','IT','$argon2id$v=19$m=65536,t=3,p=4$xLhXqvXeu/c+h3AuZez9/w$5s1Wbg7NGKDE6CIG0GLQgdT0a8EhemJrGS8spxBuPX8');
/*!40000 ALTER TABLE `manager_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager_employee_map`
--

DROP TABLE IF EXISTS `manager_employee_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager_employee_map` (
  `id` int NOT NULL AUTO_INCREMENT,
  `manager_id` varchar(50) NOT NULL,
  `employee_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_manager_employee` (`manager_id`,`employee_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `manager_employee_map_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `manager_details` (`manager_id`),
  CONSTRAINT `manager_employee_map_ibfk_2` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_employee_map`
--

LOCK TABLES `manager_employee_map` WRITE;
/*!40000 ALTER TABLE `manager_employee_map` DISABLE KEYS */;
INSERT INTO `manager_employee_map` VALUES (2,'39e44add-beb5-4705-8855-04dd0a6a5eb5','6dfc4dfd-d6f7-41ff-904b-3f3ca5414f2'),(1,'39e44add-beb5-4705-8855-04dd0a6a5eb5','6dfc4dfd-d6f7-41ff-904b-3f3ca5414f44');
/*!40000 ALTER TABLE `manager_employee_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shift_details`
--

DROP TABLE IF EXISTS `shift_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shift_details` (
  `shift_code` varchar(30) NOT NULL,
  `shift_start` time NOT NULL,
  `shift_end` time NOT NULL,
  PRIMARY KEY (`shift_code`),
  KEY `ix_shift_details_shift_code` (`shift_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shift_details`
--

LOCK TABLES `shift_details` WRITE;
/*!40000 ALTER TABLE `shift_details` DISABLE KEYS */;
INSERT INTO `shift_details` VALUES ('M-123','09:00:00','18:30:00'),('M-456','10:00:00','19:00:00');
/*!40000 ALTER TABLE `shift_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-26 18:04:09
