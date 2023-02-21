from datetime import datetime

def Write_Message(severity, message):
    # Write a message to console
    now = datetime.now()
    nowFormatted = now.strftime('%Y-%m%d %H%M%S')

    if severity == "INFO":
        print(f"{nowFormatted} - \033[0;32;40mINFO: {message}\033[0;0m") # green on black
    elif severity == "WARNING":
        print(f"{nowFormatted} - \033[0;36;40mWARNING: {message}\033[0;0m") # cyan on black
    elif severity == "ERROR":
        print(f"{nowFormatted} - \033[0;31;40mERROR: {message}\033[0;0m") # red on black
    else:
        print(f"{nowFormatted} - \033[0;31;44mFATAL: {message}\033[0;0m") # Red on blue
#