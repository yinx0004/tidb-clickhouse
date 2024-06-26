CREATE DATABASE IF NOT EXISTS `test`;

CREATE DATABASE IF NOT EXISTS `sherry`;

CREATE TABLE IF NOT EXISTS `test`.`felix` (
    `id` INT NOT NULL DEFAULT 100,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `test`.`my_first_table` (
    `user_id` INT UNSIGNED NOT NULL,
    `message` TEXT NOT NULL,
    `timestamp` DATETIME NOT NULL,
    `metric` FLOAT NOT NULL,
    PRIMARY KEY (user_id, timestamp)
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `test`.`nullable` (
    `n` INT UNSIGNED
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `test`.`stock` (
    `s_i_id` INT NOT NULL,
    `s_w_id` INT NOT NULL,
    `s_quantity` INT,
    `s_dist_01` VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (s_i_id, s_w_id)
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `test`.`users_a` (
    `uid` SMALLINT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `age` SMALLINT NOT NULL,
    `name_len` TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (name, name_len)
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `test`.`yy` (
    `name` CHAR(10) NOT NULL,
    PRIMARY KEY (name)
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `test`.`zz` (
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`asynchronous_inserts` (
    `query` VARCHAR(255) NOT NULL,
    `database` VARCHAR(255) NOT NULL,
    `table` VARCHAR(255) NOT NULL,
    `format` VARCHAR(255) NOT NULL,
    `first_update` DATETIME NOT NULL,
    `total_bytes` BIGINT UNSIGNED NOT NULL,
    `entries.query_id` UNKNOWN NOT NULL,
    `entries.bytes` UNKNOWN NOT NULL,
    PRIMARY KEY (query)
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`certificates` (
    `version` INT NOT NULL,
    `serial_number` VARCHAR(255),
    `signature_algo` VARCHAR(255),
    `issuer` VARCHAR(255),
    `not_before` VARCHAR(255),
    `not_after` VARCHAR(255),
    `subject` VARCHAR(255),
    `pkey_algo` VARCHAR(255),
    `path` VARCHAR(255) NOT NULL,
    `default` TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (version)
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`dt` (
    `timestamp` DATETIME NOT NULL,
    `event_id` TINYINT UNSIGNED NOT NULL
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`dt64` (
    `timestamp` DATETIME NOT NULL,
    `event_id` TINYINT UNSIGNED NOT NULL
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`float_vs_decimal` (
    `my_float` DOUBLE NOT NULL,
    `my_decimal` DECIMAL(18, 3) NOT NULL
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`json` (
    `o` JSON NOT NULL
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`order_info` (
    `oid` BIGINT UNSIGNED NOT NULL,
    `buyer_nick` VARCHAR(255) NOT NULL,
    `seller_nick` VARCHAR(255) NOT NULL,
    `payment` DECIMAL(18, 4) NOT NULL,
    `order_status` TINYINT UNSIGNED NOT NULL,
    `gmt_order_create` DATETIME NOT NULL,
    `gmt_order_pay` DATETIME NOT NULL,
    `gmt_update_time` DATETIME NOT NULL,
    PRIMARY KEY (seller_nick, gmt_order_create),
    INDEX `oid_idx` (oid),
    INDEX `idx_seller_nick` (seller_nick),
    INDEX `idx_seller_nick_order_status` (seller_nick, order_status)
    ) ENGINE=InnoDB -- partition key toYYYYMMDD(gmt_order_create)
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`secondary` (
    `oid` BIGINT UNSIGNED NOT NULL,
    `buyer_nick` VARCHAR(255) NOT NULL,
    `order_status` TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (oid),
    INDEX `order_status_idx` (order_status)
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`t_enum` (
    `x` ENUM('hello','world') NOT NULL
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`test_bool` (
    `A` BIGINT NOT NULL,
    `B` BOOLEAN NOT NULL
    ) ENGINE=InnoDB
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`visits` (
    `VisitDate` DATE NOT NULL,
    `Hour` TINYINT UNSIGNED NOT NULL,
    `ClientID` TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (Hour)
    ) ENGINE=InnoDB -- partition key toYYYYMM(VisitDate)
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`visits2` (
    `VisitDate` DATE NOT NULL,
    `Hour` TINYINT UNSIGNED NOT NULL,
    `ClientID` TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (Hour)
    ) ENGINE=InnoDB -- partition key toYYYYMM(VisitDate)
    ;
    
CREATE TABLE IF NOT EXISTS `sherry`.`was` (
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
    ) ENGINE=InnoDB
    ;
    
