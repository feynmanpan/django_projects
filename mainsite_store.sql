-- MySQL dump 10.13  Distrib 8.0.19, for Linux (x86_64)
--
-- Host: localhost    Database: pydb
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `mainsite_store`
--

DROP TABLE IF EXISTS `mainsite_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mainsite_store` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `url` varchar(200) NOT NULL,
  `url_logo` varchar(200) NOT NULL,
  `create_dt` datetime(6) NOT NULL,
  `url_href` varchar(100) NOT NULL,
  `code` varchar(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mainsite_store`
--

LOCK TABLES `mainsite_store` WRITE;
/*!40000 ALTER TABLE `mainsite_store` DISABLE KEYS */;
INSERT INTO `mainsite_store` VALUES (1,'博客來','https://www.books.com.tw/','https://www.books.com.tw/csss/images/books_logo.png','2020-02-19 03:11:00.000000','','01'),(2,'誠品','http://www.eslite.com/','http://www.eslite.com/images/index/logo.png','2020-02-19 03:19:00.000000','','02'),(3,'金石堂','https://www.kingstone.com.tw/','','2020-02-19 03:20:00.000000','mystatic/images/ks_logo.png','03'),(4,'讀冊生活','https://www.taaze.tw/index.html','https://www.taaze.tw/new_ec/rwd/include/images/A_image/btn/logo@2x.png','2020-02-19 03:23:00.000000','','04'),(5,'露天拍賣','https://www.ruten.com.tw/','','2020-02-19 16:26:00.000000','mystatic/images/ruten_logo.png','09'),(6,'茉莉','http://www.mollie.com.tw/News_List.asp','http://www.mollie.com.tw/images/M-main_r1_c2.gif','2020-02-19 14:42:00.000000','','06'),(7,'天瓏','https://www.tenlong.com.tw/','','2020-02-19 15:42:00.000000','mystatic/images/tenlong_logo.png','07'),(8,'時報悅讀網','http://www.readingtimes.com.tw/ReadingTimes/default.aspx','','2020-02-19 16:10:00.000000','mystatic/images/RT_logo.png','08'),(9,'灰熊愛讀書','https://www.iread.com.tw/index.aspx','https://www.iread.com.tw/images/iRead_Logo.jpg','2020-02-19 03:24:00.000000','','05'),(10,'Yahoo奇摩拍賣','https://tw.bid.yahoo.com/','https://s.yimg.com/ma/auc/logo/uh_logo_auction.png','2020-02-22 15:21:00.000000','','10'),(11,'momo摩天商城','https://www.momoshop.com.tw/main/Main.jsp','','2020-02-22 15:25:00.000000','/mystatic/images/momo_logo.png','11'),(12,'PChome線上購物','https://shopping.pchome.com.tw/','','2020-02-22 15:29:00.000000','mystatic/images/pchome_logo.png','12'),(13,'kobo樂天','https://www.kobo.com/tw/zh','https://kbstatic1-a.akamaihd.net/1.0.0.6372/Images/logos/rakuten-kobo-landscape.svg','2020-02-22 15:30:00.000000','','13'),(14,'蝦皮','https://shopee.tw/','','2020-02-22 15:32:00.000000','mystatic/images/shopee_logo.png','14'),(15,'郵政商城','https://www.postmall.com.tw/','','2020-02-22 15:33:00.000000','mystatic/images/postmall_logo.png','15'),(16,'ETMall東森購物','https://www.etmall.com.tw/','https://media.etmall.com.tw/Promo/Image/Kanban/9/11673/8ae452ef-7dc7-431f-905a-f4e686e11123.png','2020-02-22 15:34:00.000000','','16'),(17,'三民','https://www.sanmin.com.tw/','','2020-02-22 15:36:00.000000','mystatic/images/sanmin_logo.png','17'),(18,'udn','https://shopping.udn.com/mall/Cc1a00.do','https://img.udn.com/image/banner/20200130112627_s59115.gif?t=20200220205201','2020-02-22 15:38:00.000000','','18'),(19,'Readmoo讀墨','https://readmoo.com/','https://cdn.readmoo.com/images/store/logo-xl@2x.png','2020-02-22 15:39:00.000000','','19'),(20,'umall森森','https://www.u-mall.com.tw/','https://www.u-mall.com.tw/xml/Promo/Image/Kanban/9/9175/7e2ceba6-90e8-4afc-988c-8e61fb75bb61.jpg','2020-02-22 15:40:00.000000','','20');
/*!40000 ALTER TABLE `mainsite_store` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-23  1:38:44
