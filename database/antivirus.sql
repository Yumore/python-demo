/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MariaDB
 Source Server Version : 100509
 Source Host           : localhost:3306
 Source Schema         : test

 Target Server Type    : MariaDB
 Target Server Version : 100509
 File Encoding         : 65001

 Date: 06/07/2021 21:20:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for antivirus
-- ----------------------------
DROP TABLE IF EXISTS `antivirus`;
CREATE TABLE `antivirus`
(
    `id`               int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
    `version_code`     varchar(255) DEFAULT NULL,
    `version_name`     varchar(255) DEFAULT NULL,
    `app_name`         varchar(255) DEFAULT NULL,
    `package_name`     varchar(255) NOT NULL,
    `app_signature_v2` varchar(255) DEFAULT NULL,
    `update_time`      bigint(50) DEFAULT NULL,
    `app_signature_v3` varchar(255) DEFAULT NULL,
    `target_sdk`       varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1376
  DEFAULT CHARSET = utf8mb4;

-- ----------------------------
-- Records of antivirus
-- ----------------------------
BEGIN;

COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
