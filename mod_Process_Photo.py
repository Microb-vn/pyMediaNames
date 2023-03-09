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

def Process_Photo(file, fileObject, settingsObject):
    
    inputYearPos = int(fileObject["InputYearPos"])
    inputMonthPos = int(fileObject["InputMonthPos"])
    inputDayPos = int(fileObject["InputDayPos"])
    inputHourPos = int(fileObject["InputHourPos"])
    inputMinutePos = int(fileObject["InputMinutePos"])
    inputSecondPos = int(fileObject["InputSecondPos"])
    desiredOutputMask = settingsObject["DesiredOutputMask"]

    # Try to extract the exif data
    exifData = Extract_ExifData(file.filePath)
    if type(exifData) == str:
        exifDate = None
        Write_Message("WARNING", f"Cannot extract exif data from ({file.filePath}); {exifData} ")
        return

    # Try to pull current values from EXIF data
    Write_Message("INFO", f"Found EXIF data in photo file ({file.filePath}); capturing current values.")
    # ImageDescription
    try:
        imageDescription = exifData["ImageDescription"]
    except:
        imageDescription = None
    # Make
    try:
        exifMake = exifData["Make"]
    except:
        exifMake = None
    # Model
    try:
        exifModel = exifData["Model"]
    except:
        exifModel = None
    # DateTime
    try:
        # Try to compose a valid date
        exifDate=exifData["DateTime"]
        yyyy=int(exifDate[0:4])
        mm=int(exifDate[5:7])
        dd=int(exifDate[8:10])
        hour=int(exifDate[11:13])
        minute=int(exifDate[14:16])
        second=int(exifDate[17:19])
        fileNameDate = datetime(yyyy, mm, dd, hour, minute, second)
    except:
        exifDate=None

    if settingsObject["NewDateTime"] == "FromFileDetails":
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
        else:
            pass # we already have a valid fileNameDate pulled from the Exifdata

        if not fileNameDate:
            Write_Message("INFO", f"Could not compose a valid date from Photo Filename ({file.filePath}); will use the file creation date")
            fileNameDate = time.strptime(time.ctime(os.path.getctime(file.filePath)))
            # Convert time tuple into datetime object
            fileNameDate = datetime.fromtimestamp(time.mktime(fileNameDate))
    else:
        fileNameDate = parse(settingsObject["NewDateTime"])
    
    dateInDesiredFormat = fileNameDate.strftime(desiredOutputMask)

    # Do we need o change the filename?
    fileNameNoExt = file.fileName.replace(file.fileExtension,'')
    if settingsObject["NewFileName"] == "PreserveCurrent": 
        desiredNewFileName = f"[{fileNameNoExt}]"
    elif settingsObject["NewFileName"] == "FromParentFolder":
        desiredNewFileName = os.path.basename(os.path.dirname(file.filePath))
    else:
        desiredNewFileName = settingsObject["NewFileName"]
    
    if settingsObject["NewFileName"] == "PreserveCurrent" and file.fileName.startswith(dateInDesiredFormat):
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}) and NewFileName parameter set to preserve old filename; filename ({file.fileName}) already has proper format, no action required")
        exifFileName = file.filePath
    elif file.fileName.startswith(dateInDesiredFormat) and fileNameNoExt.replace(f'{dateInDesiredFormat} - ','') == desiredNewFileName:
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}) and possible new filename ({desiredNewFileName}); filename ({file.fileName}) already has this format, no action required")
        exifFileName = file.filePath
    else:
        fileFolder = file.filePath.replace(file.fileName,"")
        newName = f"{fileFolder}{dateInDesiredFormat} - {desiredNewFileName}{file.fileExtension}"
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}) and possible new filename ({desiredNewFileName}); will change filename of {file.fileName} to {newName}")
        exifFileName = newName
        os.rename(file.filePath, newName)
    #
    # Do we need to udate or add exifdate?
    Write_Message("INFO", "See if we need to make EXIF updates...")
    '''
        The EXIF fields that are not the date field get special treatment. When NO valid date was found AND
        when the field is blank, the script will fill the EXIF data with "dummy" data to indicate that
        the found EXIF data was blank
    '''
    exifObjects = []

    if settingsObject["ImageDescription"] != "":
        Write_Message("INFO", f'Will set Exif ImageDescription to value found in Settingsfile ({settingsObject["ImageDescription"]})')
        exifObjects.append(exifObject(270, settingsObject["ImageDescription"]))
    else:
        if not exifDate and not imageDescription:
            text = 'DESCRIPTION IS AUTO ADDED BY MEDIA ORGANIZER SCRIPT'
            Write_Message("INFO", f"Will set Exif ImageDescription to {text}")
            exifObjects.append(exifObject(270, text))

    if settingsObject["ExifDeviceMake"] != "":
        Write_Message("INFO", f'Will set Exif DeviceMake to value found in Settingsfile ({settingsObject["ExifDeviceMake"]})')
        exifObjects.append(exifObject(271, settingsObject["ExifDeviceMake"]))
    else:
        if not exifDate and not exifMake:
            text = 'SCRIPT'
            Write_Message("INFO", f"Will set Exif Make field to {text}")
            exifObjects.append(exifObject(271, text))

    if settingsObject["ExifDeviceModel"] != "":
        Write_Message("INFO", f'Will set Exif DeviceModel to value found in Settingsfile ({settingsObject["ExifDeviceModel"]})')
        exifObjects.append(exifObject(272, settingsObject["ExifDeviceModel"]))
    else:
        if not exifDate and not exifModel:
            text = 'pyMediaNames_V1.0'
            Write_Message("INFO", f"Will set Exif Model field to {text}")
            exifObjects.append(exifObject(272, text))

    newExifDate = fileNameDate.strftime("%Y:%m:%d %H:%M:%S")
    if exifDate != newExifDate:
        Write_Message("INFO", f'Will set Exif Date to {newExifDate}')
        exifObjects.append(exifObject(306, newExifDate))
        exifObjects.append(exifObject(36868, newExifDate))

    if len(exifObjects) != 0:
        result = Update_ExifData(exifFileName, exifObjects)
        if result != "Ok":
            Write_Message("WARNING", result)
        Write_Message("INFO", f'Exif Updates Done')
    else:
        Write_Message("INFO", f'No Exif Updates to be done')

    return