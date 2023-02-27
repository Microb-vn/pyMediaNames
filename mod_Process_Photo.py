from datetime import datetime
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

def Process_Photo(file, fileObject):
    
    inputYearPos = int(fileObject["InputYearPos"])
    inputMonthPos = int(fileObject["InputMonthPos"])
    inputDayPos = int(fileObject["InputDayPos"])
    inputHourPos = int(fileObject["InputHourPos"])
    inputMinutePos = int(fileObject["InputMinutePos"])
    inputSecondPos = int(fileObject["InputSecondPos"])
    desiredOutputMask = fileObject["DesiredOutputMask"]
    # Try to extract the exif data
    exifData = Extract_ExifData(file.filePath)
    if type(exifData) == str:
        exifDate=False
        Write_Message("WARNING", f"Found NO EXIF data in photo file ({file.filePath}); will skip further processing for this file ")
        return
    else:
        Write_Message("INFO", f"Found EXIF data in photo file ({file.filePath}).")
        try:
            # Try to compose a valid date
            yyyy=int(exifData["DateTime"][0:4])
            mm=int(exifData["DateTime"][5:7])
            dd=int(exifData["DateTime"][8:10])
            hour=int(exifData["DateTime"][11:13])
            minute=int(exifData["DateTime"][14:16])
            second=int(exifData["DateTime"][17:19])
            fileNameDate = datetime(yyyy, mm, dd, hour, minute, second)
            exifDate=True
        except:
            exifDate=False

    if not exifDate:
        Write_Message("INFO", f"Photo file ({file.fileName}) does not contain valid or complete EXIF data; will use the filename to compose date.")
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
    
    dateInDesiredFormat = fileNameDate.strftime(fileObject["DesiredOutputMask"])

    # Do we need o change the filename?
    if file.fileName.startswith(dateInDesiredFormat):
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}); filename ({file.fileName}) already has this format, no action required")
        exifFileName = file.filePath
    else:
        fileFolder = file.filePath.replace(file.fileName,"")
        fileNameNoExt = file.fileName.replace(file.fileExtension,'')
        newName = f"{fileFolder}{dateInDesiredFormat} - [{fileNameNoExt}]{file.fileExtension}"
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}); will change filename of {file.fileName} to {newName}")
        exifFileName = newName
        os.rename(file.filePath, newName)
    #
    # Do we need to udate or add exifdate?
    if not exifDate:
        # There is no ExifData yet, create the basic info
        Write_Message("INFO", "As no valid Exif date is found, will update that with what was found during this scan"      )

        exifObjects = []
        
        exifObjects.append(exifObject(271, "ADDED BY SCRIPT"))
        exifObjects.append(exifObject(272, "UNKNOWN"))
        newExifDate = fileNameDate.strftime("%Y:%m:%d %H:%M:%S")
        exifObjects.append(exifObject(36868, newExifDate))

        result = Update_ExifData(exifFileName, exifObjects)
        if result != "Ok":
            Write_Message("WARNING", result)

    return