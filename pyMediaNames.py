#!/usr/bin/python3

# Load the std Python library modules
import os
import sys
import argparse
from datetime import datetime
import time
import platform
import pathlib
# Load own modules (globally)
from mod_Write_Message import Write_Message
from mod_Read_Config import Read_Config
from mod_Process_Photo import Process_Photo
from mod_Process_Photo_Exif import Process_Photo_Exif
from mod_Process_Video import Process_Video
#
# Important functions, loaded in mainscript rather than from a custom/own library
# 

def CleanExit(sleepTime):
    # Gracefully Exit the script 
    Write_Message("INFO", f"Done! This window will close in {sleepTime} seconds")
    time.sleep(sleepTime)
    os._exit(0)
#
def get_arguments():
    # Get Commandline Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-SettingsFile')
    args=parser.parse_args()
    if not args.SettingsFile:
        return "settings.json" # default settings filename
    else:
        return args.SettingsFile
# Custom class to capture file info
class fileInfo():
    def __init__(self, filePath, fileName, fileExtension):
        self.filePath = filePath
        self.fileName = fileName
        self.fileExtension = fileExtension

# #############
# Main function. It starts here
# #############
def main():
    # ===============
    # CHECK PLATFORM: Is it linux? If yes, we're good to go
    # ===============
    currentPlatform = platform.system()
    if currentPlatform != 'Linux':
        Write_Message('ERROR', ':Platform is not supported. Stopping!!!')
        CleanExit(10)
    
    Write_Message("INFO", f"Script {os.path.basename(__file__)} is triggered, Starting its execution now...")
    settingsFileName = get_arguments()

    # Set some generally used variables
    scriptPath = os.path.dirname(__file__)
    settingsFileName = f"{scriptPath}/{settingsFileName}"

    # ===============
    # READ THE CONFIGuration file
    # ===============
    Write_Message("INFO", f"Will make an attempt to read and interpret settinsgfile {settingsFileName}")
    settingsObject = Read_Config(settingsFileName, scriptPath)
    if type(settingsObject) == str:
        Write_Message("ERROR",settingsObject)
        CleanExit(10)
    Write_Message("INFO", f"All values in settinsgfile {settingsFileName} are approved, continuing...")
    
    # Find and collect all files from ProcessFolder (recursivelly)
    allFiles = []
    for path,dirs,files in os.walk(settingsObject['ProcessFolder']):
        for file in files:
            fileName = pathlib.Path(file).name
            fileExtension = pathlib.Path(file).suffix
            allFiles.append(fileInfo(os.path.join(path,fileName),fileName, fileExtension))

    # Go thru all the files one by one to determine what type of file it is
    for file in allFiles:
        fileObject = None
        Write_Message("INFO", '------------------------------------------------------')
        # Did we process the file already?
        if "]." in file.filePath:
            Write_Message("WARNING", f"It looks like file {file.filePath} has been processed before; will take no action!")
            continue
        # See what type of file we have
        for object in settingsObject["Objects"]:
            if file.fileExtension.lower() in object["Identifiers"]:
                fileObject = object
                break

        # Is the file a video or photo?
        if fileObject:
            if fileObject["Type"] == "Photo":
               Write_Message("INFO", f"file {file.filePath} is a PHOTO file; will process it as such")
               Process_Photo(file, fileObject, settingsObject)
            else:
                Write_Message("INFO", f"file {file.filePath} is a VIDEO file; will process it as such")
                Process_Video(file, fileObject, settingsObject)
        else:
            Write_Message( "WARNING", f"File {file.filePath} is of an unknow file type ({file.fileExtension}); will skip the file")

if __name__ == '__main__':
    main()
