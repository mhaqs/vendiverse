-- --------------------------------------------------------
-- Sunucu:                       192.168.2.100
-- Sunucu versiyonu:             5.5.54-0+deb8u1 - (Debian)
-- Sunucu İşletim Sistemi:       debian-linux-gnu
-- HeidiSQL Sürüm:               8.3.0.4694
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- tablo yapısı dökülüyor macgal.parameter
CREATE TABLE IF NOT EXISTS `parameter` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `detail` varchar(60) NOT NULL,
  `type` int(1) unsigned NOT NULL,
  `value` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

-- Dumping data for table macgal.parameter: ~15 rows (yaklaşık)
/*!40000 ALTER TABLE `parameter` DISABLE KEYS */;
INSERT INTO `parameter` (`id`, `name`, `detail`, `type`, `value`) VALUES
	(1, 'PRODSUBS', 'Rafta urun yoksa baska raftan ver', 1, '1'),
	(2, 'SALESOUND', 'Satis yapilinca ses cal', 1, '0'),
	(3, 'MULTISALE', 'Bakiye varsa satisa devam et', 1, '0'),
	(4, 'NOCOINSALE', 'Para ustu yoksa satis yapma', 1, '1'),
	(5, 'NOCOINWARN', 'Para ustu yoksa uyar', 1, '1'),
	(6, 'MAINCLOCK', 'Ana ekranda saat goster', 1, '1'),
	(7, 'MAINDATE', 'Ana ekranda tarih goster', 1, '1'),
	(8, 'MAINMODEL', 'Ana ekranda marka/model goster', 1, '1'),
	(9, 'PSENSOR', 'URUN SENSORU', 1, '1'),
	(10, 'PSENSORT', 'SENSOR GORMEDIGINDE CEYREK TUR DONDER', 1, '1'),
	(11, 'MAXTEMP1', 'Birinci sensor ust sicaklik', 2, '28'),
	(12, 'MINTEMP1', 'Birinci sensor alt sicaklik', 2, '26'),
	(13, 'MAXTEMP2', 'Ikinci sensor ust sicaklik', 2, '8'),
	(14, 'MINTEMP2', 'Ikinci sensor alt sicaklik', 2, '3'),
	(15, 'MEANTEMP', 'Hedeflenen ortalama sicaklik', 2, '5');
/*!40000 ALTER TABLE `parameter` ENABLE KEYS */;


-- tablo yapısı dökülüyor macgal.product
CREATE TABLE IF NOT EXISTS `product` (
  `id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `barcode` varchar(20) NOT NULL,
  `price` decimal(5,2) DEFAULT NULL,
  `vat` int(2) unsigned DEFAULT '0',
  `active` int(1) unsigned DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

-- Dumping data for table macgal.product: ~16 rows (yaklaşık)
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` (`id`, `name`, `barcode`, `price`, `vat`, `active`) VALUES
	(1, 'COCA COLA KUTU 330cc', '123456789', 2.00, 0, 1),
	(2, 'COCA COLA LIGHT KUTU 330cc', '', 1.75, 0, 1),
	(3, 'COCA COLA ZERO KUTU 330cc', '', 1.75, 0, 1),
	(4, 'NESTEA SEFTALI 330cc', '', 1.50, 0, 1),
	(5, 'NESTEA LIMON 330cc', '', 1.50, 0, 1),
	(6, 'DAMLA SU 500ml', '', 1.00, 0, 1),
	(7, 'TADELLE CIKOLATA', '', 1.00, 0, 1),
	(8, 'TADELLE BEYAZ CIKOLATA', '', 1.00, 0, 1),
	(9, 'ULKER CUBUK KRAKER', '', 0.75, 0, 1),
	(10, 'ULKER HAYLAYF', '', 1.00, 0, 1),
	(11, 'ULKER CIKOLATALI GOFRET', '', 1.00, 0, 1),
	(12, 'NESTLE SU 500mL', '', 1.00, 0, 1),
	(13, 'AKMINA SODA 330mL', '', 1.00, 0, 1),
	(14, 'FRUTOLA INCIRLI', '', 2.00, 0, 1),
	(15, 'ETI POPKEK CIKOLATALI', '', 1.00, 0, 1),
	(16, 'ULKER IKRAM CIKOLATALI BISKUVI', '', 1.00, 0, 1);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;


-- tablo yapısı dökülüyor macgal.sale
CREATE TABLE IF NOT EXISTS `sale` (
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
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=latin1;

-- Dumping data for table macgal.sale: ~127 rows (yaklaşık)
/*!40000 ALTER TABLE `sale` DISABLE KEYS */;
INSERT INTO `sale` (`id`, `product_id`, `shelf_id`, `price`, `sale_dt`, `balance`, `remaining`, `sale_type`, `success`) VALUES
	(2, 1, 1, 3.00, '2017-04-23 12:49:36', 3.00, 0.00, 1, 1),
	(3, 1, 1, 1.00, '2017-04-23 13:05:07', 2.00, 1.00, 1, 1),
	(4, 1, 1, 1.00, '2017-04-23 13:10:29', 2.00, 1.00, 1, 1),
	(5, 1, 1, 1.00, '2017-04-23 13:13:19', 2.00, 1.00, 1, 1),
	(6, 1, 1, 1.00, '2017-04-23 13:18:30', 2.00, 1.00, 1, 1),
	(7, 1, 1, 1.00, '2017-04-23 13:19:14', 2.00, 1.00, 1, 1),
	(8, 1, 1, 1.00, '2017-04-23 13:21:37', 1.50, 0.50, 1, 1),
	(9, 1, 1, 1.00, '2017-04-23 13:30:54', 2.00, 1.00, 1, 1),
	(10, 1, 1, 1.00, '2017-04-23 13:32:31', 1.75, 0.75, 1, 1),
	(11, 1, 1, 1.00, '2017-04-23 13:33:31', 1.75, 0.75, 1, 1),
	(12, 1, 1, 1.00, '2017-04-23 13:36:22', 1.75, 0.75, 1, 1),
	(13, 1, 1, 1.00, '2017-04-23 13:37:33', 1.75, 0.75, 1, 1),
	(14, 1, 1, 1.00, '2017-04-23 13:39:51', 1.75, 0.75, 1, 1),
	(15, 1, 1, 1.00, '2017-04-23 13:41:10', 1.75, 0.75, 1, 1),
	(16, 1, 1, 1.00, '2017-04-23 13:42:19', 2.75, 1.75, 1, 1),
	(17, 1, 1, 1.00, '2017-04-23 14:15:28', 1.50, 0.50, 1, 1),
	(18, 1, 1, 1.00, '2017-04-23 15:59:50', 1.75, 0.75, 1, 1),
	(19, 1, 1, 1.50, '2017-04-23 17:47:07', 1.75, 0.25, 1, 1),
	(20, 1, 1, 1.50, '2017-04-23 18:24:45', 3.75, 2.25, 1, 1),
	(21, 1, 1, 1.50, '2017-04-23 19:38:48', 6.50, 5.00, 1, 1),
	(23, 1, 1, 1.50, '2017-04-23 23:25:47', 2.00, 0.50, 1, 1),
	(24, 1, 1, 1.50, '2017-04-24 15:19:52', 2.00, 0.50, 1, 1),
	(25, 8, 9, 1.00, '2017-04-24 15:51:03', 1.75, 0.75, 1, 1),
	(26, 6, 7, 1.00, '2017-04-24 16:01:09', 2.00, 1.00, 1, 1),
	(27, 1, 1, 2.00, '2017-04-24 18:01:19', 2.00, 0.00, 1, 1),
	(28, 2, 3, 1.75, '2017-04-24 18:01:36', 2.00, 0.25, 1, 1),
	(29, 5, 6, 1.50, '2017-04-24 21:22:13', 2.00, 0.50, 1, 1),
	(30, 5, 6, 1.50, '2017-04-24 21:23:48', 2.00, 0.50, 1, 1),
	(31, 6, 7, 1.00, '2017-04-24 14:48:21', 2.00, 1.00, 1, 1),
	(32, 5, 6, 1.50, '2017-04-24 14:56:54', 2.00, 0.50, 1, 1),
	(33, 5, 6, 1.50, '2017-04-24 17:50:31', 3.00, 1.50, 1, 1),
	(34, 5, 6, 1.50, '2017-04-24 17:51:31', 1.50, 0.00, 1, 1),
	(35, 4, 5, 1.50, '2017-04-24 17:52:06', 1.50, 0.00, 1, 1),
	(36, 7, 8, 1.00, '2017-04-24 17:52:29', 1.50, 0.50, 1, 1),
	(37, 5, 6, 1.50, '2017-04-24 18:13:06', 1.50, 0.00, 1, 1),
	(38, 2, 3, 1.75, '2017-04-24 18:17:00', 2.00, 0.25, 1, 1),
	(39, 1, 1, 1.00, '2017-04-24 18:19:20', 1.00, 0.00, 1, 1),
	(40, 1, 1, 1.00, '2017-04-24 18:28:19', 1.00, 0.00, 1, 1),
	(41, 1, 1, 1.00, '2017-04-24 18:28:42', 1.00, 0.00, 1, 1),
	(42, 1, 1, 1.00, '2017-04-24 18:30:45', 1.00, 0.00, 1, 1),
	(44, 1, 1, 1.00, '2017-04-24 18:32:09', 1.50, 0.50, 1, 1),
	(45, 1, 1, 1.00, '2017-04-24 14:47:35', 1.00, 0.00, 1, 1),
	(46, 1, 1, 1.00, '2017-04-24 15:19:31', 1.00, 0.00, 1, 1),
	(47, 1, 1, 1.00, '2017-04-24 15:00:37', 1.00, 0.00, 1, 1),
	(48, 1, 1, 1.00, '2017-04-24 14:48:01', 1.00, 0.00, 1, 1),
	(49, 1, 1, 1.00, '2017-04-24 14:53:35', 1.00, 0.00, 1, 1),
	(50, 1, 1, 1.00, '2017-04-24 14:53:53', 1.00, 0.00, 1, 1),
	(51, 1, 1, 1.00, '2017-04-24 15:44:24', 1.00, 0.00, 1, 1),
	(52, 1, 1, 1.00, '2017-04-24 15:44:40', 1.00, 0.00, 1, 1),
	(53, 1, 1, 1.00, '2017-04-24 15:45:01', 1.00, 0.00, 1, 1),
	(54, 2, 3, 1.75, '2017-04-24 15:10:32', 1.75, 0.00, 1, 1),
	(56, 1, 1, 2.00, '2017-04-24 15:01:03', 3.00, 1.00, 1, 1),
	(57, 1, 1, 2.00, '2017-04-24 14:52:03', 2.00, 0.00, 1, 1),
	(58, 1, 2, 2.00, '2017-04-24 14:52:37', 2.00, 0.00, 1, 1),
	(59, 1, 2, 2.00, '2017-04-24 14:53:24', 2.00, 0.00, 1, 1),
	(60, 1, 2, 2.00, '2017-04-24 14:54:00', 3.00, 1.00, 1, 1),
	(61, 3, 4, 1.75, '2017-04-24 14:56:04', 3.00, 1.25, 1, 1),
	(62, 3, 4, 1.75, '2017-04-24 14:56:38', 3.00, 1.25, 1, 1),
	(63, 3, 4, 1.75, '2017-04-24 15:03:03', 3.00, 1.25, 1, 1),
	(64, 1, 1, 2.00, '2017-05-17 17:36:21', 2.00, 0.00, 1, 1),
	(65, 1, 1, 2.00, '2017-05-17 17:38:29', 2.00, 0.00, 1, 1),
	(66, 1, 1, 2.00, '2017-04-16 12:14:55', 2.00, 0.00, 1, 1),
	(67, 1, 1, 2.00, '2017-05-18 19:09:20', 2.00, 0.00, 1, 1),
	(68, 1, 2, 2.00, '2017-05-18 19:09:40', 2.00, 0.00, 1, 1),
	(69, 3, 4, 1.75, '2017-05-18 19:10:15', 2.00, 0.25, 1, 1),
	(70, 4, 5, 1.50, '2017-05-18 19:10:43', 2.00, 0.50, 1, 1),
	(71, 5, 6, 1.50, '2017-05-18 19:11:10', 2.00, 0.50, 1, 1),
	(72, 6, 7, 1.00, '2017-05-18 19:11:27', 1.00, 0.00, 1, 1),
	(73, 7, 8, 1.00, '2017-05-18 19:11:41', 1.00, 0.00, 1, 1),
	(74, 1, 2, 2.00, '2017-05-18 19:13:36', 2.00, 0.00, 1, 1),
	(75, 3, 4, 1.75, '2017-05-18 19:14:04', 2.00, 0.25, 1, 1),
	(76, 2, 3, 1.75, '2017-05-18 19:14:28', 2.00, 0.25, 1, 1),
	(77, 5, 6, 1.50, '2017-05-18 19:22:47', 3.50, 2.00, 1, 1),
	(78, 5, 6, 1.50, '2017-05-18 19:23:21', 2.00, 0.50, 1, 1),
	(79, 4, 5, 1.50, '2017-05-18 19:26:14', 4.00, 2.50, 1, 1),
	(80, 5, 6, 1.50, '2017-05-18 19:26:33', 2.00, 0.50, 1, 1),
	(81, 6, 7, 1.00, '2017-05-18 19:29:58', 1.00, 0.00, 1, 1),
	(82, 6, 7, 1.00, '2017-05-18 19:31:08', 1.00, 0.00, 1, 1),
	(83, 5, 6, 1.50, '2017-05-18 19:55:37', 1.50, 0.00, 1, 1),
	(84, 2, 3, 1.75, '2017-04-18 23:29:38', 3.00, 1.25, 1, 1),
	(85, 3, 4, 1.75, '2017-04-18 23:30:45', 3.00, 1.25, 1, 1),
	(86, 2, 3, 1.75, '2017-04-18 23:31:24', 3.00, 1.25, 1, 1),
	(87, 1, 2, 2.00, '2017-05-19 20:22:05', 2.75, 0.75, 1, 1),
	(88, 2, 3, 1.75, '2017-04-18 20:25:37', 2.00, 0.25, 1, 1),
	(89, 6, 7, 1.00, '2017-04-18 20:59:37', 1.00, 0.00, 1, 1),
	(90, 5, 6, 1.50, '2017-04-18 22:21:24', 2.00, 0.50, 1, 1),
	(91, 6, 7, 1.00, '2017-04-18 21:51:58', 1.00, 0.00, 1, 1),
	(92, 6, 7, 1.00, '2017-05-20 18:21:25', 1.00, 0.00, 1, 1),
	(93, 3, 4, 1.75, '2017-04-20 12:45:45', 2.00, 0.25, 1, 1),
	(94, 1, 1, 2.00, '2017-05-20 19:00:52', 2.00, 0.00, 1, 1),
	(95, 1, 1, 2.00, '2017-05-20 19:01:20', 2.00, 0.00, 1, 1),
	(96, 1, 1, 2.00, '2017-05-20 19:04:56', 2.00, 0.00, 1, 1),
	(97, 1, 1, 2.00, '2017-05-20 19:10:12', 2.00, 0.00, 1, 1),
	(98, 1, 1, 2.00, '2017-05-20 19:10:23', 2.00, 0.00, 1, 1),
	(99, 1, 1, 2.00, '2017-05-20 19:16:33', 2.00, 0.00, 1, 1),
	(100, 1, 1, 2.00, '2017-05-20 19:17:14', 2.00, 0.00, 1, 1),
	(101, 4, 5, 1.50, '2017-05-20 19:17:53', 2.00, 0.50, 1, 1),
	(102, 4, 5, 1.50, '2017-05-20 19:18:11', 2.00, 0.50, 1, 1),
	(103, 4, 5, 1.50, '2017-05-20 19:18:59', 2.00, 0.50, 1, 1),
	(104, 1, 1, 2.00, '2017-05-20 19:19:23', 2.00, 0.00, 1, 1),
	(105, 1, 1, 2.00, '2017-05-20 19:20:09', 2.00, 0.00, 1, 1),
	(106, 4, 5, 1.50, '2017-05-20 19:20:41', 2.00, 0.50, 1, 1),
	(107, 4, 5, 1.50, '2017-05-20 19:24:36', 2.00, 0.50, 1, 1),
	(108, 4, 5, 1.50, '2017-05-27 17:00:03', 2.00, 0.50, 1, 1),
	(109, 1, 1, 2.00, '2017-05-27 17:00:21', 2.00, 0.00, 1, 1),
	(110, 1, 1, 2.00, '2017-05-27 17:13:53', 2.00, 0.00, 1, 1),
	(111, 1, 1, 2.00, '2017-05-27 17:14:20', 2.00, 0.00, 1, 1),
	(112, 1, 1, 2.00, '2017-05-27 17:16:16', 2.00, 0.00, 1, 1),
	(113, 1, 1, 2.00, '2017-05-27 17:16:38', 2.00, 0.00, 1, 1),
	(114, 1, 1, 2.00, '2017-05-27 17:17:26', 2.00, 0.00, 1, 1),
	(115, 11, 1, 1.00, '2017-04-26 12:24:12', 1.00, 0.00, 1, 1),
	(116, 11, 1, 1.00, '2017-04-26 12:25:06', 1.00, 0.00, 1, 1),
	(117, 12, 2, 1.00, '2017-04-26 12:25:34', 1.00, 0.00, 1, 1),
	(118, 11, 1, 1.00, '2017-04-26 12:26:49', 1.00, 0.00, 1, 1),
	(119, 14, 4, 2.00, '2017-04-26 12:28:09', 2.00, 0.00, 1, 1),
	(120, 14, 4, 2.00, '2017-04-26 12:41:00', 2.00, 0.00, 1, 1),
	(121, 16, 7, 1.00, '2017-04-26 12:41:44', 1.50, 0.50, 1, 1),
	(122, 14, 4, 2.00, '2017-04-26 12:23:06', 2.00, 0.00, 1, 1),
	(123, 11, 1, 1.00, '2017-04-26 12:24:20', 2.00, 1.00, 1, 1),
	(124, 15, 6, 1.00, '2017-04-26 12:18:11', 2.00, 1.00, 1, 1),
	(125, 14, 4, 2.00, '2017-04-26 12:19:23', 3.00, 1.00, 1, 1),
	(126, 14, 4, 2.00, '2017-04-26 12:20:52', 3.00, 1.00, 1, 1),
	(127, 14, 4, 2.00, '2017-04-26 12:21:42', 3.50, 1.50, 1, 1),
	(128, 13, 3, 1.00, '2017-04-26 12:24:22', 2.00, 1.00, 1, 1),
	(129, 11, 1, 1.00, '2017-06-01 18:52:56', 2.00, 1.00, 1, 1),
	(130, 11, 1, 1.00, '2017-06-01 18:56:10', 1.00, 0.00, 1, 1),
	(131, 11, 1, 1.00, '2017-06-01 19:04:44', 1.00, 0.00, 1, 1);
/*!40000 ALTER TABLE `sale` ENABLE KEYS */;


-- tablo yapısı dökülüyor macgal.shelf
CREATE TABLE IF NOT EXISTS `shelf` (
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

-- Dumping data for table macgal.shelf: ~11 rows (yaklaşık)
/*!40000 ALTER TABLE `shelf` DISABLE KEYS */;
INSERT INTO `shelf` (`id`, `shelf_no`, `rack_id`, `product_id`, `remaining`, `capacity`, `expire_dt`, `active`) VALUES
	(1, '10', 3, 11, 3, 6, '2017-06-01 19:04:44', 1),
	(2, '11', 3, 12, 6, 6, '2017-06-01 18:52:39', 1),
	(3, '12', 3, 13, 6, 6, '2017-06-01 18:52:39', 1),
	(4, '13', 3, 14, 6, 6, '2017-06-01 18:52:39', 1),
	(5, '14', 3, 14, 6, 6, '2017-06-01 18:52:39', 1),
	(6, '15', 3, 15, 6, 6, '2017-06-01 18:52:39', 1),
	(7, '16', 3, 16, 6, 6, '2017-06-01 18:52:39', 1),
	(8, '17', 3, 1, 6, 6, '2017-06-01 18:52:39', 1),
	(9, '18', 3, 8, 20, 20, '2017-06-01 18:52:39', 1),
	(10, '19', 3, 9, 20, 20, '2017-06-01 18:52:39', 1),
	(11, '20', 3, 10, 20, 20, '2017-06-01 18:52:39', 1);
/*!40000 ALTER TABLE `shelf` ENABLE KEYS */;


-- tablo yapısı dökülüyor macgal._day
CREATE TABLE IF NOT EXISTS `_day` (
  `no` int(2) unsigned DEFAULT NULL,
  `dow` int(2) unsigned DEFAULT NULL,
  `d` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table macgal._day: ~7 rows (yaklaşık)
/*!40000 ALTER TABLE `_day` DISABLE KEYS */;
INSERT INTO `_day` (`no`, `dow`, `d`) VALUES
	(1, 2, 'Pazartesi'),
	(2, 3, 'Sali'),
	(3, 4, 'Carsamba'),
	(4, 5, 'Persembe'),
	(5, 6, 'Cuma'),
	(6, 7, 'Cumartesi'),
	(7, 1, 'Pazar');
/*!40000 ALTER TABLE `_day` ENABLE KEYS */;


-- tablo yapısı dökülüyor macgal._hour
CREATE TABLE IF NOT EXISTS `_hour` (
  `no` int(2) unsigned DEFAULT NULL,
  `h` int(2) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table macgal._hour: ~24 rows (yaklaşık)
/*!40000 ALTER TABLE `_hour` DISABLE KEYS */;
INSERT INTO `_hour` (`no`, `h`) VALUES
	(1, 8),
	(2, 9),
	(3, 10),
	(4, 11),
	(5, 12),
	(6, 13),
	(7, 14),
	(8, 15),
	(9, 16),
	(10, 17),
	(11, 18),
	(12, 19),
	(13, 20),
	(14, 21),
	(15, 22),
	(16, 23),
	(17, 0),
	(18, 1),
	(19, 2),
	(20, 3),
	(21, 4),
	(22, 5),
	(23, 6),
	(24, 7);
/*!40000 ALTER TABLE `_hour` ENABLE KEYS */;


-- tablo yapısı dökülüyor macgal._month
CREATE TABLE IF NOT EXISTS `_month` (
  `no` int(2) unsigned NOT NULL,
  `m` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table macgal._month: ~12 rows (yaklaşık)
/*!40000 ALTER TABLE `_month` DISABLE KEYS */;
INSERT INTO `_month` (`no`, `m`) VALUES
	(1, 'Ocak'),
	(2, 'Subat'),
	(3, 'Mart'),
	(4, 'Nisan'),
	(5, 'Mayis'),
	(6, 'Haziran'),
	(7, 'Temmuz'),
	(8, 'Agustos'),
	(9, 'Eylul'),
	(10, 'Ekim'),
	(11, 'Kasim'),
	(12, 'Aralik');
/*!40000 ALTER TABLE `_month` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
