import json
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
    # Mode
    try:
        testValue = settingsObject["Mode"]
    except:
        testValue = ""
    if not testValue in ["Standard", "ExifFullUdate"]:
        return 'Mode in the settingsfile is missing or invalid'
    if testValue == "ExifFullUpdate":
        try:
            # When we have a Mode of ExifFullUpdate, following fields need to be there too
            dummy = settingsObject["ExifDeviceMake"]
            dummy = settingsObject["ExifDeviceModel"]
            dummy = settingsObject["FileTitle"]
            dummy = settingsObject["ExifDateTime"]
        except:
            return "When mode is ExifFullUpdate, attributes ExifDeviceMake, ExifDeviceModel, ExifDateTime, and FileTitle must also be defined"
        # Date must also have specific value
        if dummy != 'ExifFullUpdate':
            try:
                parse(dummy)
            except:
                return f"The specified ExifDateTime ({dummy}) in the settingsfile ({file}) is not a valid date; use your localized data format, or specify the value 'ExifFullUpdate'"
    # ProcessFolder
    try:
        testValue = settingsObject["ProcessFolder"]
    except:
        return "ProcessFolder is missing from {file}"
    if testValue[0] == ".":
        testValue = testValue.replace(".",scriptpath, 1)
    if not isdir(testValue):
        return f"Could not find folder pointed to by ProcessFolder ({testValue}) in settingsfile {file}"


    return settingsObject