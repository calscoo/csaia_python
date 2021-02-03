import os
from PIL import Image, ExifTags

for root, subdirs, files in os.walk('C:\\Users\\Caleb\\Downloads\\CCAST_CSAIA2'):
    oneImage = False
    for file in files:
        if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
            # This flag stops the iteration on the first image, uncomment this to iterate over the entire directory provided
            oneImage = True
            imgPath = os.path.join(root, file)
            img = Image.open(imgPath)
            exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
            print(imgPath)
            for mdChunk in exif:
                print(mdChunk, ':', exif[mdChunk])
        if oneImage:
            break
    if oneImage:
        break
