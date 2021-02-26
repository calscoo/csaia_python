from daos import image_dao

directories = image_dao.select_all_images('id, directory_location')
for result in directories:
    print(result)