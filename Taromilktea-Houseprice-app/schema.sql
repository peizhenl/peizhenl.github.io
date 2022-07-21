SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS db_gift;
CREATE DATABASE db_gift_store DEFAULT CHARSET UTF8;

-- -----------------------------------------------------
-- database db_gift_store
-- -----------------------------------------------------
USE `db_gift_store` ;

-- -----------------------------------------------------
-- Table `t_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(100) NOT NULL,
  `first_name` VARCHAR(100),
  `last_name` VARCHAR(100),
  `_password` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(100) NOT NULL,
  `gender` VARCHAR(10) DEFAULT 'Male',
  `avatar` VARCHAR(500),
  `is_admin` SMALLINT DEFAULT 0 COMMENT '0 is ordinary user, 1 is administrator', 
  `create_at` DATETIME NOT NULL DEFAULT NOW(),
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `t_user_address`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_user_address`;
CREATE TABLE `t_user_address` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `consignee_name` VARCHAR(100) DEFAULT NULL,
  `phone` VARCHAR(100) NOT NULL,
  `address` VARCHAR(500) NOT NULL,
  `remark` VARCHAR(500),
  `is_default` SMALLINT DEFAULT 1 COMMENT '0 is not default address, 1 is default address',
  `create_at` DATETIME NOT NULL DEFAULT NOW(),
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `t_user` (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `t_good_category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_good_category`;
CREATE TABLE `t_good_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(300) NOT NULL,
  `description` VARCHAR(500),
  `create_at` DATETIME NOT NULL DEFAULT NOW(),
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
-- insert initial good category data
INSERT INTO `t_good_category` (`id`,`name`,`description`,`create_at`,`update_at`) VALUES (6,'MON CHERI GIFTS FOR HER - Fashion ','MON CHERI GIFTS FOR HER - Fashion ','2020-09-13 21:48:25','2020-09-13 21:48:25'),(7,'MON CHERI GIFTS FOR HER - Beauty','MON CHERI GIFTS FOR HER - Beauty','2020-09-13 21:48:46','2020-09-13 21:48:46'),(8,'MON CHERI GIFTS FOR HIM - Fashion','MON CHERI GIFTS FOR HIM - Fashion','2020-09-13 21:49:15','2020-09-13 21:49:15'),(9,'MON CHERI GIFTS FOR HIM - Beauty','MON CHERI GIFTS FOR HIM - Beauty','2020-09-13 21:49:31','2020-09-13 21:49:31'),(10,'MON CHERI GIFTS FOR US - Matching Sets','MON CHERI GIFTS FOR US - Matching Sets','2020-09-13 21:49:54','2020-09-13 21:49:54'),(11,'MON CHERI GIFTS FOR US - Gourmet Hampers ','MON CHERI GIFTS FOR US - Gourmet Hampers ','2020-09-13 21:50:09','2020-09-13 21:50:09'),(12,'MON CHERI GIFTS FOR US - Hotel Packages','MON CHERI GIFTS FOR US - Hotel Packages','2020-09-13 21:50:32','2020-09-13 21:50:32');

-- -----------------------------------------------------
-- Table `t_good`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_good`;
CREATE TABLE `t_good` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `good_category_id` INT NOT NULL,
  `name` VARCHAR(300) NOT NULL,
  `color` VARCHAR(200),
  `size` VARCHAR(200),
  `description` TEXT,
  `price` DECIMAL(20,2) NOT NULL,
  `discout_rate` DECIMAL(10,3) NOT NULL DEFAULT 1.0,
  `stock` INT DEFAULT 0,
  `purchase_number` INT DEFAULT 0,
  `image_url` VARCHAR(500) DEFAULT '/img/goods/default_good.png',
  `can_refund` SMALLINT DEFAULT 0 COMMENT '0 can not refund,1 can refund',
  `status` SMALLINT DEFAULT 1 COMMENT '0 indicate off the shelf,1 indicate on the shelf',
  `create_at` DATETIME NOT NULL DEFAULT NOW(),
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`good_category_id`)
    REFERENCES `t_good_category` (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `t_cart`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_cart`;
CREATE TABLE `t_cart` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `good_id` INT NOT NULL,
  `quantity` INT NOT NULL DEFAULT 1,
  `create_at` DATETIME NOT NULL DEFAULT NOW(),
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
    FOREIGN KEY (`good_id`)
    REFERENCES `t_good` (`id`),
    FOREIGN KEY (`user_id`)
    REFERENCES `t_user` (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `t_order_item`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_order_item`;
CREATE TABLE `t_order_item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `good_id` INT NOT NULL,
  `unit_price` DECIMAL(20,2) DEFAULT 0.0,
  `quantity` INT NOT NULL,
  `good_price` DECIMAL(20,2) DEFAULT 0.0,
  `create_at` DATETIME NOT NULL DEFAULT NOW(),
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
    FOREIGN KEY (`good_id`)
    REFERENCES `t_good` (`id`),
    FOREIGN KEY (`order_id`)
    REFERENCES `t_order` (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `t_order`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_order`;
CREATE TABLE `t_order` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `order_number` VARCHAR(100) NOT NULL,
  `user_id` INT NOT NULL,
  `pay_price` DECIMAL(20,2),
  `pay_status` INT DEFAULT 0 COMMENT '0 is unpaid,1 is paid, 2 is refunding',
  `is_refund` SMALLINT DEFAULT 0 COMMENT '0 can not refund, 1 can refund',
  `create_at` DATETIME NOT NULL DEFAULT NOW(),
  `expire_at` DATETIME,
  `update_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`)
    REFERENCES `t_user` (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `t_receipt_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_receipt_info`;
CREATE TABLE `t_receipt_info` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `order_id` INT NOT NULL,
    `user_address_id` INT NOT NULL,
    `create_at` DATETIME NOT NULL DEFAULT NOW(),
    `update_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`order_id`) REFERENCES `t_order` (`id`),
    FOREIGN KEY (`user_address_id`) REFERENCES `t_user_address` (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `t_payment_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_payment_info`;
CREATE TABLE `t_payment_info` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `order_id` INT NOT NULL,
    `card_no` VARCHAR(100) NOT NULL,
    `remark` VARCHAR(500),
    `create_at` DATETIME NOT NULL DEFAULT NOW(),
    `update_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`order_id`) REFERENCES `t_order` (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `t_refund`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `t_refund_info`;
CREATE TABLE `t_refund_info` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `order_id` INT NOT NULL,
    `refund_reason` VARCHAR(500),
    `is_approve` SMALLINT DEFAULT 0 COMMENT '0 is unprocessed, 1 is not approved, 2 is approved',
    `refund_at` DATETIME NOT NULL DEFAULT NOW(),
    `update_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`order_id`) REFERENCES `t_order` (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;

