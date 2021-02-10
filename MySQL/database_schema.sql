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
	`flight_name` VARCHAR(100) NOT NULL,
	`manual_notes` VARCHAR(255) NOT NULL,
	`address` VARCHAR(255) NOT NULL,
	`field_name` VARCHAR(100),
	`crop_name` VARCHAR(100),
	`average_latitude` DECIMAL(14, 10) NOT NULL,
	`average_longitude` DECIMAL(14, 10) NOT NULL,
	`average_altitude` DECIMAL(10, 4) NOT NULL,
	`flight_start_time` DATETIME NOT NULL,
	`flight_end_time` DATETIME NOT NULL,
	`hardware_make` VARCHAR(100),
	`hardware_model` VARCHAR(100),
	PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`id`)
);
CREATE TABLE `csaia_database`.`images` (
	`id` BIGINT NOT NULL AUTO_INCREMENT,
	`flight_id` BIGINT,
	`directory_location` TEXT NOT NULL,
	`image_extension` VARCHAR(25),
	`datetime` DATETIME NOT NULL,
	`latitude` DECIMAL(14, 10) NOT NULL,
	`longitude` DECIMAL(14, 10) NOT NULL,
	`altitude` DECIMAL(10, 4) NOT NULL,
	`image_width` SMALLINT,
	`image_height` SMALLINT,
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
	`bits_per_sample` SMALLINT,
	`exif_version` VARCHAR(50),
	`software_version` VARCHAR(100),
	`hardware_make` VARCHAR(100),
	`hardware_model` VARCHAR(100),
	`hardware_serial_number` VARCHAR(255),
	PRIMARY KEY (`id`),
    FOREIGN KEY (`flight_id`) REFERENCES flights(`id`)
);