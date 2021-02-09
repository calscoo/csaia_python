import os
import exifread
from GPSPhoto import gpsphoto

for root, subdirs, files in os.walk('C:\\Users\\Caleb\\Downloads'):
    oneImage = False
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in ('.jpg', '.jpeg', '.tif', '.tiff'):
            # This flag stops the iteration on the first image, uncomment this to iterate over the entire directory provided
            oneImage = True
            imgPath = os.path.join(root, file)
            f = open(imgPath, 'rb')
            tags = exifread.process_file(f)
            gpsData = gpsphoto.getGPSData(imgPath)
            print(gpsData)
            for tag in tags.keys():
                print(tag, ":", tags[tag])
        if oneImage:
            break
    if oneImage:
        break
