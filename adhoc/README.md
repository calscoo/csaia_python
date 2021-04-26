# adhoc
These python scripts and queries were used to iterate over an curate the images on the CCAST system. What follows is outdated instructions on how to run these scripts to curate a collection of images into images and flights. They're outdated, simply because once the data was curated, the schema had changed a few times, and the adhoc scripts were not updated to reflect the new changes.
1. Drop your current DB schema and pull the latest schema from the backend repo
2. Run the MySQL/database_schema.sql to setup the database
3. Using MySQL command line, execute each bulk_image_insert_query_201X.sql
	- This can be done by typing 'source C:/path/to/sql/file/query.sql'
4. Again, using MySQL command line, execute adhoc/infer_flights_query.sql
	- This can be found in the adhoc folder of the backend repo
5. Lastly, Using your IDE of choice, execute 'adhoc/flight_curator.py'
	- This can be done by changing whatever you use on the backend to execute 'main.py' for testing to 'adhoc/flight_curator.py'
6. You should now have all of the CCAST drone data on your local database, complete with full image and flight metadata.