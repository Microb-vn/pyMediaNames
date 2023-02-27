from datetime import datetime
import os
import time
# import own modules
from mod_Write_Message import Write_Message

def Process_Video(file, fileObject):
    
    inputYearPos = int(fileObject["InputYearPos"])
    inputMonthPos = int(fileObject["InputMonthPos"])
    inputDayPos = int(fileObject["InputDayPos"])
    inputHourPos = int(fileObject["InputHourPos"])
    inputMinutePos = int(fileObject["InputMinutePos"])
    inputSecondPos = int(fileObject["InputSecondPos"])
    desiredOutputMask = fileObject["DesiredOutputMask"]

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
    
    dateInDesiredFormat = fileNameDate.strftime(fileObject["DesiredOutputMask"])

    # Do we need o change the filename?
    if file.fileName.startswith(dateInDesiredFormat):
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}); filename ({file.fileName}) already has this format, no action required")
    else:
        fileFolder = file.filePath.replace(file.fileName,"")
        fileNameNoExt = file.fileName.replace(file.fileExtension,'')
        newName = f"{fileFolder}{dateInDesiredFormat} - [{fileNameNoExt}]{file.fileExtension}"
        Write_Message("INFO", f"Found desired date ({dateInDesiredFormat}); will change filename of {file.fileName} to {newName}")
        exifFileName = newName
        os.rename(file.filePath, newName)
    #
    return