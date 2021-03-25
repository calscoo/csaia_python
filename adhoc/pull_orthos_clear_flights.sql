INSERT INTO csaia_database.orthomosaics(`directory_location`, `image_extension`) SELECT directory_location, image_extension FROM csaia_database.images where (directory_location like '%ortho%' and directory_location not like '%with ortho%') or (directory_location like '%with ortho%' and image_extension like '%tif%');
UPDATE
	csaia_database.images as I
SET
	I.flight_id = NULL
WHERE
	I.id IN (SELECT * FROM(SELECT id FROM csaia_database.images where (directory_location like '%ortho%' and directory_location not like '%with ortho%') or (directory_location like '%with ortho%' and image_extension like '%tif%'))tableTmp);
    DELETE FROM csaia_database.images where flight_id is NULL;
UPDATE
	csaia_database.images as I
SET
	I.flight_id = NULL;
DELETE FROM csaia_database.flights;