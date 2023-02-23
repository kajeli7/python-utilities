import cv2 as cv
from pathlib import Path, WindowsPath
import os
import time
from datetime import date, datetime
# from ctypes import *
import win32api
import pywintypes
import win32file

def get_read_handle (filename):
    if os.path.isdir(filename):
        dwFlagsAndAttributes = win32file.FILE_FLAG_BACKUP_SEMANTICS
    else:
        dwFlagsAndAttributes = 0
    return win32file.CreateFile (
        filename,
        win32file.GENERIC_READ,
        win32file.FILE_SHARE_READ,
        None,
        win32file.OPEN_EXISTING,
        dwFlagsAndAttributes,
        None
    )


all_videos = (Path('D:\\TEMP').rglob('*.*'))

now_pytime = pywintypes.Time (time.time())
print("TODAY: " + str(now_pytime))

for video_path in all_videos:
    video_obj = cv.VideoCapture(str(video_path))
    # print(str(video_path) + " " + str(video_obj.isOpened()) + " " + video_obj.getBackendName())
    
    timestamp = video_path.stat().st_mtime
    handle = get_read_handle(str(video_path))
    time_of_file = win32file.GetFileTime(handle)
    print(time_of_file[0])
    # print(str(video_path) + " " +  str(datetime.fromtimestamp(timestamp)) + " " )
