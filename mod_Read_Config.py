import json
import re
from datetime import datetime
from dateutil.parser import parse
from os.path import isdir

def Read_Config(file, scriptpath):
    try:
        action = 'open settings file ' + file
        with open(file, mode ='r')as infile:
            action = 'interpret json settings file ' + file + '; the json syntax is invalid, please check!'
            settingsObject = json.load(infile)
    except:
        return 'Error occured while Attempting to ' + action

    # Check the contents
    try:
        # All optional parameters, plus the date:
        dummy = settingsObject["ExifDeviceMake"]
        dummy = settingsObject["ExifDeviceModel"]
        dummy = settingsObject["ImageDescription"]
        dummydate = settingsObject["NewDateTime"]
    except:
        return "One (or more) of the attributes ExifDeviceMake, ExifDeviceModel, NewDateTime or ImageDescription is missing"
    # Date must also have specific value: a valid date or "FromFileDetails"
    if dummydate != 'FromFileDetails':
        try:
            parse(dummydate)
        except:
            return f"The specified ExifDateTime ({dummy}) in the settingsfile ({file}) is not a valid date or 'FromFileDetails'"
    # ProcessFolder
    try:
        testValue = settingsObject["ProcessFolder"]
    except:
        return f"ProcessFolder is missing from {file}"
    if testValue[0] == ".":
        testValue = testValue.replace(".",scriptpath, 1)
    if not isdir(testValue):
        return f"Could not find folder pointed to by ProcessFolder ({testValue}) in settingsfile {file}"

    # NewFileName
    try:
        testValue = settingsObject["NewFileName"]
    except:
        return f"NewFileName parameter is missing from {file}"

    if not testValue:
        return f"NewFileName is missing from {file}"

    if dummydate != "FromFileDetails" and testValue != "PreserveCurrent":
        return "NewFileDate parameter is a fixed date and NewFileName is not PreserveCurrent; this will result in duplicate filenames!"

    try:
        testValue = datetime.now().strftime(settingsObject['DesiredOutputMask'])
    except:
        testValue = f"INVALIDMASK:{settingsObject['DesiredOutputMask']}"
    
    if not re.fullmatch("^[-:. 0-9]+$", testValue):
        # Still contains alpha characters?
        return f"The DesiredOutputMask in settingsfile {file} is invalid."


    # Object nodes
    if len(settingsObject["Objects"]) != 2:
        return f"The number of 'Objects' found in settingsfile {file} is {len(settingsObject['Objects'])}; this should be 2"
    photoCount = videoCount = 0
    for object in settingsObject["Objects"]:
        # Object type
        if object['Type'] == "Photo":
            photoCount = photoCount + 1
        elif object['Type'] == 'Video':
            videoCount = videoCount + 1
        else:
            return f"Invalid Object Type found ({object['Type']}) in settingsfile {file}"
        # Are all Inputxxxpos values numbers?
        try:
            testValue = f"{object['InputYearPos']}{object['InputMonthPos']}{object['InputDayPos']}{object['InputHourPos']}{object['InputMinutePos']}{object['InputSecondPos']}"
        except:
            testValue = "ERROR"
        if not testValue.isnumeric():
            return f"One of the DateTime positions of object {object['Type']} in settingsfile {file} is missing or not numeric; please check!"
        
    if photoCount != 1 or videoCount !=1:
        return f"Mismatch in number of Video ({videoCount}) and/or Photo ({photoCount}) objects in settingsfile {file}; these should both be 1" 

    return settingsObject