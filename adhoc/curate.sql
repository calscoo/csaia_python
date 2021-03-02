CREATE TABLE `csaia_database`.`curate` (
  `image_id` INT NOT NULL,
  `image_parent_location` TEXT NOT NULL
);

-- INSERT INTO csaia_database.curate(`image_id`, `image_parent_location`) SELECT id, SUBSTRING_INDEX(directory_location, SUBSTRING_INDEX(directory_location, '/' ,-1), 1) AS flight_name FROM csaia_database.images;
-- UPDATE csaia_database.images SET `flight_id` = (
SELECT csaia_database.images.id AS image_id, csaia_database.flights.id AS flight_id
FROM csaia_database.flights
INNER JOIN csaia_database.curate
ON csaia_database.flights.flight_name = csaia_database.curate.image_parent_location
INNER JOIN csaia_database.images
ON csaia_database.images.id = csaia_database.curate.image_id;

-- REMEMBER TO SET THE FLIGHT FIELDS TO NULLABLE AND ADJUST THE FLIGHT NAME TO TEXT BEFORE TESTING FURTHER