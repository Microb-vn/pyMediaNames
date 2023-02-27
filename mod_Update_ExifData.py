from PIL import Image as PillowImage
from PIL.ExifTags import TAGS

def Update_ExifData(imageName, Updates):
    # Build reverse TAGS list (soyou can access/set TAGS 'by name')
    # _TAGS_r = dict(((v, k) for k, v in TAGS.items())) 

    imgFile=imageName
    # First try to read the existing exif Data
    img = PillowImage.open(imgFile) # We do not check, bcos the file is read/detected by the caller
    img_exif = img.getexif()
    # Update
    for update in Updates:
        img_exif[update.propertyNr] = update.propertyValue

    img.save(imgFile, exif=img_exif)
    return "Ok"  
    
# TEST CODE
if __name__ == '__main__':
    
    class exifObject():
        def __init__(self, propertyNr, propertyValue):
            self.propertyNr = propertyNr
            self.propertyValue = propertyValue

    exifObjects = []
        
    exifObjects.append(exifObject(271, "ADDED BY SCRIPT"))
    exifObjects.append(exifObject(272, "UNKNOWN"))
#    newExifDate = fileNameDate.strftime(%Y:%m;%d %H:%M:%S)
#    exifObjects.append(exifObject(36868, newExifDate))

    result=Update_ExifData("/home/rob/Documenten/GitHub/pyMediaNames/out.jpg", exifObjects)
    

