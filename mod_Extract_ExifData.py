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

    img = Image.open(imgFile)
    img_exif = img.getexif()
#    print(type(img_exif))

    if img_exif is None:
        return('Sorry, image has no exif data.')
    else:
        exifObject={}
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
#                print(f'{ExifTags.TAGS[key]}:{val}')
                exifObject[ExifTags.TAGS[key]] = val
                # ExifVersion:b'0230'
                # ...
                # FocalLength:(2300, 100)
                # ColorSpace:1
                # ...
                # Model:'X-T2'
                # Make:'FUJIFILM'
                # LensSpecification:(18.0, 55.0, 2.8, 4.0)
                # ...
                # DateTime:'2019:12:01 21:30:07'
                # ...
        return(exifObject)

# for fast testing
if __name__ == "__main__":
    file="/home/rob/Documenten/GitHub/pyMediaNames/ProcessFolder/Gescand document.jpg"
    results = Extract_ExifData(file)
    print(f"Result for {file}")
    for result in results:
        value=results[f"{result}"]
        print(f"{result}: {value}")
    file="/home/rob/Documenten/GitHub/pyMediaNames/ProcessFolder/00-Diversen/2022-0507 073355 - Mooi koolzaadveld (tijdens hardlopen).jpg"
    results = Extract_ExifData(file)
    print(f"Result for {file}")
    for result in results:
        value=results[f"{result}"]
        print(f"{result}: {value}")

