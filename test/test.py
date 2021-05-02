import os

from enums.role import roles
from enums.privacy import privacy
from objects.image import image
from objects.range import range as Range
from managers import flight_manager, users_manager, image_manager, shared_flight_manager


# Creates a user without admin credentials, this can't be done via the api
users_manager.create_user_testing("user1", "pass", roles.Admin)

# Creates a user the standard way, with admin id and password credentials
users_manager.create_user("user_email", "user_pass", roles.Admin, 1, "admin_pass")

# Allows an admin to update a user role
users_manager.update_user_role(1, roles.Admin, 1, "admin_pass")

# Allows a user to update their own password
users_manager.update_user_pass(1, "old_pass", "new_pass")

# Allows an admin to updates a users password
users_manager.admin_update_user_pass(1, "new_pass", 1, "admin_pass")

# Fetches users role based on the passed id
users_manager.fetch_user_role(1)

# Returns true if the api key matches any api keys in the system
users_manager.verify_api_key("vsRV7QBUP3EQGaD4wPbMjzUC2")

# Returns the api key of the user via id and password
users_manager.fetch_user_api_key(1, "pass")

# generates and returns an api key for the user
users_manager.generate_user_api_key(1, "pass")

# returns all users
users_manager.fetch_all_users()

# Fetches users based on a list of ids, email, password and role. Any of these are optional.
users_manager.fetch_users([1, 2, 3, 4], "email", "password", roles.Admin)

# Returns whether the email is used in the system or not
users_manager.does_user_exist("email")

# Returns -1 if the validation failed, or the user id if the validation succeeded.
users_manager.validate_login_credentials("email", "password")

# Builds a flight. This inserts the images, calculates and inserts the image and flight metadata
flight_manager.build_flight(1, "/path/to/images/", "flight_name", "manual_notes", "field_name", "crop_name", privacy.Private, [1, 2, 3, 4])

# Fetch flight objects via a number of optional params
flight_manager.fetch_flights(1, [1, 2, 3, 4], [1, 2, 3, 4], "flight_name", "manual_notes", "address", "field_name", "crop_name", Range(1234, 5678), Range(1234, 5678), Range(1234, 5678), Range(1234, 5678), Range(1234, 5678), "make", "model")

# Removes the flight by id
flight_manager.remove_flight(1)

# calculate and return the flight address
flight_manager.flight_address(1234, 5678)

# inserts image objects into the database
image_manager.upload_images([image()])

# Fetch image and flight objects via a number of optional params
image_manager.fetch_images_and_flights(1, [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], "/image/file/path", [".jpg", ".tif"], Range(1234, 5678), Range(1234, 5678), Range(1234, 5678), Range(1234, 5678), "make", "model", "hash", None, None, None, None, None)

# Remove images
image_manager.remove_images([1, 2, 3, 4, 5], 1, "admin_pass")

# Shares a flight to a list of users
shared_flight_manager.share_flight(1, [1, 2, 3, 4, 5])

# Returns user ids that are shared on a flight
shared_flight_manager.fetch_shared_flight_user_ids(1)

# Returns flight ids that are shared with a user
shared_flight_manager.fetch_users_shared_flight_ids(1)
