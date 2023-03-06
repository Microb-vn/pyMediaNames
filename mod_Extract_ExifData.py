# With courtesy of -Unknown-
# I did not write this code myself. Found it in a knowledge article. I changed the code into a function that 
# returns (most of the) Exif data in a Python dictiionary.
# Most of the sources for this module were found on Stakcoverflow.com
# 
# -----------------------------------------------------------------
# Load this file in your script with this command:
# . <(full-)path-to-whatever-you-call-this-file>
# and use the function call
# Extract_ExifData <(full-)path-to-your-photo-file>
#
# If all goes wel, a custom object is returned with the EXIF details
# When errors are found, a variable of type String is returned
from PIL import Image, ExifTags

def Extract_ExifData(imagename):
    imgFile=imagename

    try:
        img = Image.open(imgFile)
    except:
        return('Cannot open the image file; invalid file format.')

    try: 
        img_exif = img.getexif()
    except:
        return('Image has no exif data.')

    exifObject={}
    for key, val in img_exif.items():
         if key in ExifTags.TAGS:
            #print(f'{ExifTags.TAGS[key]}:{val}')
            exifObject[ExifTags.TAGS[key]] = val

    return(exifObject)

# for fast testing
if __name__ == "__main__":
    file="/home/rob/Documenten/GitHub/pyMediaNames/ProcessFolder/Mapjje2/2023-0206 124720 - [20230206_124720].jpg"
    results = Extract_ExifData(file)
    print(f"Result for {file}")
    for result in results:
        value=results[f"{result}"]
        print(f"{result}: {value}")

