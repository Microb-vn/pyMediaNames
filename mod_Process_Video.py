from datetime import datetime
from dateutil.parser import parse
import os
import time
# import own modules
from mod_Write_Message import Write_Message

def Process_Video(file, fileObject, settingsObject):
    
    inputYearPos = int(fileObject["InputYearPos"])
    inputMonthPos = int(fileObject["InputMonthPos"])
    inputDayPos = int(fileObject["InputDayPos"])
    inputHourPos = int(fileObject["InputHourPos"])
    inputMinutePos = int(fileObject["InputMinutePos"])
    inputSecondPos = int(fileObject["InputSecondPos"])
    desiredOutputMask = fileObject["DesiredOutputMask"]

    if settingsObject["NewDateTime"] != "FromFileDetails":
        fileNameDate = parse(settingsObject["NewDateTime"])
    else:
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
            Write_Message("INFO", f"Could not compose a valid date from Video Filename ({file.filePath}); will use the file creation date")
            fileNameDate = time.strptime(time.ctime(os.path.getctime(file.filePath)))
            # Convert time tuple into datetime object
            fileNameDate = datetime.fromtimestamp(time.mktime(fileNameDate))
    
    dateInDesiredFormat = fileNameDate.strftime(desiredOutputMask)

    # Do we need o change the filename?
    fileNameNoExt = file.fileName.replace(file.fileExtension,'')
    if settingsObject["NewFileName"] == "PreserveCurrent":
        desiredFileName = f"[{fileNameNoExt}]"
    elif settingsObject["NewFileName"] == "FromParentFolder":
        desiredFileName = os.path.basename(os.path.dirname(file.filePath))
    else:
        desiredFileName = settingsObject["NewFileName"]

    if settingsObject["NewFileName"] == "PreserveCurrent" and file.fileName.startswith(dateInDesiredFormat):
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}) and NewFileName parameter set to preserve old filename; filename ({file.fileName}) already has proper format, no action required")
        exifFileName = file.filePath
    elif file.fileName.startswith(dateInDesiredFormat) and fileNameNoExt.replace(f'{dateInDesiredFormat} - ','') == desiredNewFileName:
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}) and possible new filename ({desiredNewFileName}); filename ({file.fileName}) already has this format, no action required")
        exifFileName = file.filePath
    else:
        fileFolder = file.filePath.replace(file.fileName,"")
        newName = f"{fileFolder}{dateInDesiredFormat} - {desiredFileName}{file.fileExtension}"
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}) and possible new filename ({desiredFileName}); will change filename of {file.fileName} to {newName}")
        exifFileName = newName
        os.rename(file.filePath, newName)
    #
    return