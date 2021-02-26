from daos import image_dao
from os.path import basename
from pathlib import Path


directories = image_dao.select_all_images('*')
for result in directories:
    directory = str(result[3])
    parent_path = Path(directory).parent
    flight_name = basename(parent_path)
    print("\nflight name: " + str(flight_name))
    print("image parent path: " + str(parent_path))
    print("image extension: " + str(result[4]))