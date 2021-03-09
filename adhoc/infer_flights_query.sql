CREATE TEMPORARY TABLE `csaia_database`.`curate` (
  `image_id` INT NOT NULL,
  `image_parent_location` TEXT NOT NULL
);

INSERT INTO csaia_database.curate(`image_id`, `image_parent_location`) SELECT id, SUBSTRING_INDEX(directory_location, SUBSTRING_INDEX(directory_location, '\\' ,-1), 1) AS flight_name FROM csaia_database.images;
INSERT INTO csaia_database.flights(`flight_name`) SELECT DISTINCT SUBSTRING_INDEX(directory_location, SUBSTRING_INDEX(directory_location, '\\' ,-1), 1) from csaia_database.images;

CREATE TABLE `csaia_database`.`images_to_flight`
SELECT csaia_database.images.id AS image_id, csaia_database.flights.id AS flight_id
FROM csaia_database.flights
INNER JOIN csaia_database.curate
ON csaia_database.flights.flight_name = csaia_database.curate.image_parent_location
INNER JOIN csaia_database.images
ON csaia_database.images.id = csaia_database.curate.image_id;

UPDATE
	csaia_database.images I,
	csaia_database.images_to_flight ITF
SET
	I.flight_id = ITF.flight_id
WHERE
	I.id = ITF.image_id;

DROP TEMPORARY TABLE csaia_database.curate;
DROP TEMPORARY TABLE csaia_database.images_to_flight;