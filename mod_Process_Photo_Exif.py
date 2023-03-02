from datetime import datetime
from dateutil.parser import parse
import os
import time
# import own modules
from mod_Extract_ExifData import Extract_ExifData
from mod_Update_ExifData import Update_ExifData
from mod_Write_Message import Write_Message

# Custom class to store updates for exifData
class exifObject():
    def __init__(self, propertyNr, propertyValue):
        self.propertyNr = propertyNr
        self.propertyValue = propertyValue

def Process_Photo_Exif(file, fileObject, settingsObject):
    
    inputYearPos = int(fileObject["InputYearPos"])
    inputMonthPos = int(fileObject["InputMonthPos"])
    inputDayPos = int(fileObject["InputDayPos"])
    inputHourPos = int(fileObject["InputHourPos"])
    inputMinutePos = int(fileObject["InputMinutePos"])
    inputSecondPos = int(fileObject["InputSecondPos"])
    desiredOutputMask = fileObject["DesiredOutputMask"]
    # Try to extract the exif data

    if settingsObject["ExifDateTime"] == "FromFileDetails":
        Write_Message("INFO", f"Photo file ({file.filePath}), will use the filename to compose date.")
        yyyy = mm = dd = hour = minute = second = None
        if len(file.fileName) >= inputDayPos+2:
            dd = file.fileName[inputDayPos:inputDayPos+2]
        if len(file.fileName) >= inputMonthPos+2:
            mm = file.fileName[inputMonthPos:inputMonthPos+2]
        if len(file.fileName) >= inputYearPos+2:
            yyyy = file.fileName[inputYearPos:inputYearPos+4]
        if len(file.fileName) >= inputHourPos+2:
            hour = file.fileName[inputHourPos:inputHourPos+2]
        if len(file.fileName) >= inputMinutePos+2:
            minute = file.fileName[inputMinutePos:inputMinutePos+2]
        if len(file.fileName) >= inputSecondPos+2:
            second = file.fileName[inputSecondPos:inputSecondPos+2]
        try:
            fileNameDate = datetime(int(yyyy), int(mm), int(dd), int(hour), int(minute), int(second))
        except:
            fileNameDate = None

        if not fileNameDate:
            Write_Message("INFO", f"Could not compose a valid date from Photo Filename ({file.filePath}); will use the file creation date")
            fileNameDate = time.strptime(time.ctime(os.path.getctime(file.filePath)))
            # Convert time tuple into datetime object
            fileNameDate = datetime.fromtimestamp(time.mktime(fileNameDate))
        
    else:
        # Date is hardcoded in settingsfile
        fileNameDate = datetime.date(parse(settingsObject["ExifDateTime"]))

    dateInDesiredFormat = fileNameDate.strftime(desiredOutputMask)

    # Do we need o change the filename?
    fileNameNoExt = file.fileName.replace(file.fileExtension,'')
    if settingsObject["NewFileName"] == "KeepCurrent": 
        desiredNewFileName = f"[{fileNameNoExt}]"
    elif settingsObject["NewFileName"] == "FromParentFolder":
        desiredNewFileName = os.path.basename(os.path.dirname(file.filePath))
    else:
        desiredNewFileName = settingsObject["NewFileName"]
    
    if file.fileName.startswith(dateInDesiredFormat) and fileNameNoExt == desiredNewFileName:
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}) and suggested new filename ({desiredNewFileName}); filename ({file.fileName}) already has this format, no action required")
        exifFileName = file.filePath
    else:
        fileFolder = file.filePath.replace(file.fileName,"")
        newName = f"{fileFolder}{dateInDesiredFormat} - {desiredNewFileName}{file.fileExtension}"
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}); will change filename of {file.fileName} to {newName}")
        exifFileName = newName
        os.rename(file.filePath, newName)
    #
    # Do we need to udate or add exifdate?
    # There is no ExifData yet, create the basic info
    Write_Message("INFO", "Update Exif Data in the photo file")

    exifObjects = []
    
    if settingsObject["FileTitle"]:
        exifObjects.append(exifObject(270, settingsObject["FileTitle"]))     
    
    if settingsObject["ExifDeviceMake"]:
        exifObjects.append(exifObject(271, settingsObject["ExifDeviceMake"]))

    if settingsObject["ExifDeviceModel"]:
        exifObjects.append(exifObject(272, settingsObject["ExifDeviceModel"]))
    
    newExifDate = fileNameDate.strftime("%Y:%m:%d %H:%M:%S")
    exifObjects.append(exifObject(306, newExifDate))
    exifObjects.append(exifObject(36868, newExifDate))

    result = Update_ExifData(exifFileName, exifObjects)
    if result != "Ok":
        Write_Message("WARNING", result)

    return