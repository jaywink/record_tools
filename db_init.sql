
delimiter $$

CREATE DATABASE `generic` /*!40100 DEFAULT CHARACTER SET utf8 */$$

delimiter $$

CREATE TABLE `for_sale` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1000) COLLATE utf8_swedish_ci NOT NULL,
  `price` int(4) DEFAULT NULL,
  `condition` varchar(30) COLLATE utf8_swedish_ci DEFAULT NULL,
  `type` int(5) NOT NULL,
  `link` varchar(300) COLLATE utf8_swedish_ci DEFAULT NULL,
  `picture` varchar(300) COLLATE utf8_swedish_ci DEFAULT NULL,
  `media` varchar(300) COLLATE utf8_swedish_ci DEFAULT NULL,
  `notes` text COLLATE utf8_swedish_ci,
  `sub_type` varchar(300) COLLATE utf8_swedish_ci DEFAULT NULL,
  `changed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` int(2) NOT NULL DEFAULT '1',
  `discogs_id` int(11) DEFAULT NULL,
  `bought_by` varchar(300) COLLATE utf8_swedish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=226 DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci$$

delimiter $$

CREATE TABLE `item_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_type_u` (`item_id`,`type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=109 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `type` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `description` varchar(80) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=utf8$$


INSERT INTO `type` (`id`,`description`) VALUES (1,'Vinyl');
INSERT INTO `type` (`id`,`description`) VALUES (2,'Garage');
INSERT INTO `type` (`id`,`description`) VALUES (3,'Breakbeat');
INSERT INTO `type` (`id`,`description`) VALUES (4,'Drum''n''bass');
INSERT INTO `type` (`id`,`description`) VALUES (5,'House');
INSERT INTO `type` (`id`,`description`) VALUES (6,'Broken Beat');
INSERT INTO `type` (`id`,`description`) VALUES (7,'Techno');
INSERT INTO `type` (`id`,`description`) VALUES (8,'Books');
INSERT INTO `type` (`id`,`description`) VALUES (9,'RPG');
INSERT INTO `type` (`id`,`description`) VALUES (10,'Wargames');
INSERT INTO `type` (`id`,`description`) VALUES (11,'Electronics');
INSERT INTO `type` (`id`,`description`) VALUES (12,'Phone');
INSERT INTO `type` (`id`,`description`) VALUES (13,'CD');
INSERT INTO `type` (`id`,`description`) VALUES (14,'Metal');
INSERT INTO `type` (`id`,`description`) VALUES (15,'Club');
INSERT INTO `type` (`id`,`description`) VALUES (16,'Nu jazz');
INSERT INTO `type` (`id`,`description`) VALUES (17,'Downtempo');
INSERT INTO `type` (`id`,`description`) VALUES (18,'Jazzdance');
INSERT INTO `type` (`id`,`description`) VALUES (19,'Trance');
INSERT INTO `type` (`id`,`description`) VALUES (20,'Hard House');
INSERT INTO `type` (`id`,`description`) VALUES (21,'Drum n Bass');
INSERT INTO `type` (`id`,`description`) VALUES (22,'UK Garage');
INSERT INTO `type` (`id`,`description`) VALUES (23,'Pop Rock');
INSERT INTO `type` (`id`,`description`) VALUES (24,'Easy Listening');
INSERT INTO `type` (`id`,`description`) VALUES (25,'Electro');
INSERT INTO `type` (`id`,`description`) VALUES (26,'Breaks');
INSERT INTO `type` (`id`,`description`) VALUES (27,'Big Beat');
INSERT INTO `type` (`id`,`description`) VALUES (28,'Hardcore');
INSERT INTO `type` (`id`,`description`) VALUES (29,'Deep House');
INSERT INTO `type` (`id`,`description`) VALUES (30,'Jungle');
INSERT INTO `type` (`id`,`description`) VALUES (31,'Tech House');
INSERT INTO `type` (`id`,`description`) VALUES (32,'RnB/Swing');
INSERT INTO `type` (`id`,`description`) VALUES (33,'Dub');
INSERT INTO `type` (`id`,`description`) VALUES (34,'Hip Hop');
