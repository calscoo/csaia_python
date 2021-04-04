-- This schema represents our current db model and allows for ease of setup on new machines.
SET GLOBAL max_allowed_packet=1073741824;
CREATE DATABASE `csaia_database`;
CREATE TABLE `csaia_database`.`users` (
	`id` BIGINT NOT NULL AUTO_INCREMENT,
	`email` VARCHAR(100) NOT NULL,
	`password` VARCHAR(255) NOT NULL,
	`role` TINYINT NOT NULL,
	PRIMARY KEY (`id`)
);
CREATE TABLE `csaia_database`.`flights` (
	`id` BIGINT NOT NULL AUTO_INCREMENT,
	`user_id` BIGINT,
	`flight_name` TEXT,
	`manual_notes` VARCHAR(255),
	`address` VARCHAR(255),
	`field_name` VARCHAR(100),
	`crop_name` VARCHAR(100),
	`average_latitude` DECIMAL(14, 10),
	`average_longitude` DECIMAL(14, 10),
	`average_altitude` DECIMAL(10, 4),
	`flight_start_time` DATETIME,
	`flight_end_time` DATETIME,
	`hardware_make` VARCHAR(100),
	`hardware_model` VARCHAR(100),
	`privacy` TINYINT NOT NULL,
	PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`id`)
);
CREATE TABLE `csaia_database`.`images` (
	`id` BIGINT NOT NULL AUTO_INCREMENT,
	`user_id` BIGINT,
	`flight_id` BIGINT,
	`directory_location` TEXT NOT NULL,
	`image_extension` VARCHAR(25),
	`datetime` DATETIME,
	`latitude` DECIMAL(14, 10),
	`longitude` DECIMAL(14, 10),
	`altitude` DECIMAL(10, 4),
	`image_width` INT,
	`image_height` INT,
	`exposure_time` VARCHAR(50),
	`f_number` VARCHAR(50),
	`iso_speed` INT,
	`metering_mode` VARCHAR(50),
	`focal_length` VARCHAR(50),
	`light_source` VARCHAR(50),
	`exposure_mode` VARCHAR(50),
	`white_balance` VARCHAR(50),
	`gain_control` VARCHAR(50),
	`contrast` VARCHAR(50),
	`saturation` VARCHAR(50),
	`sharpness` VARCHAR(50),
	`image_compression` VARCHAR(100),
	`exif_version` VARCHAR(50),
	`software_version` VARCHAR(100),
	`hardware_make` VARCHAR(100),
	`hardware_model` VARCHAR(100),
	`hardware_serial_number` VARCHAR(255),
    `md5_hash` VARCHAR(32),
	PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    FOREIGN KEY (`flight_id`) REFERENCES flights(`id`) ON DELETE CASCADE
);
CREATE TABLE `csaia_database`.`orthomosaics` (
	`id` BIGINT NOT NULL AUTO_INCREMENT,
	`directory_location` TEXT NOT NULL,
	`image_extension` VARCHAR(25),
	PRIMARY KEY (`id`)
);
CREATE TABLE `csaia_database`.`shared_flights` (
	`user_id` BIGINT NOT NULL,
	`flight_id` BIGINT NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    FOREIGN KEY (`flight_id`) REFERENCES flights(`id`)
);