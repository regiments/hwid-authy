CREATE DATABASE IF NOT EXISTS `hwidauth`;
USE `hwidauth`;


CREATE TABLE IF NOT EXISTS `license-keys` (
  `key_id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) DEFAULT NULL,
  `used` int(1) DEFAULT 0,
  KEY `Index 1` (`key_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(16) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `hwid` varchar(36) DEFAULT NULL,
  `uuid` varchar(36) DEFAULT NULL,
  `key_owned` int(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
