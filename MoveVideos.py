import cv2 as cv
from pathlib import Path, WindowsPath
import os
import time
from datetime import date, datetime
# from ctypes import *
import win32api
import pywintypes
import win32file
import traceback
import random
import logging
import shutil

# INFO: Configure logging
logging.basicConfig(
	filename="D:\\_projects_github\\utilities\\move_videos.log",
	datefmt='%Y-%m-%d %H:%M:%S', 
	format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
	level=logging.INFO)

# INFO: Setup unique numbers
unique_n = list(range(5, 10000))
random.shuffle(unique_n)

# INFO: Constants
target_path = 'D:\TEMP_VIDEOS\\'
error_path = 'D:\TEMP_ERRORS\\'
all_videos = (Path('D:\\TEMP').rglob('*.*'))
numb_errors = 0

# INFO: Just print current date
now_pytime = pywintypes.Time (time.time())
print("TODAY: " + str(now_pytime))
print("\n")

def get_mov_timestamps(filename):
    ''' Get the creation and modification date-time from .mov metadata.

        Returns None if a value is not available.
    '''
    from datetime import datetime as DateTime
    import struct

    ATOM_HEADER_SIZE = 8
    # difference between Unix epoch and QuickTime epoch, in seconds
    EPOCH_ADJUSTER = 2082844800

    creation_time = modification_time = None

    # search for moov item
    with open(filename, "rb") as f:
        while True:
            atom_header = f.read(ATOM_HEADER_SIZE)
            #~ print('atom header:', atom_header)  # debug purposes
            if atom_header[4:8] == b'moov':
                break  # found
            else:
                atom_size = struct.unpack('>I', atom_header[0:4])[0]
                f.seek(atom_size - 8, 1)

        # found 'moov', look for 'mvhd' and timestamps
        atom_header = f.read(ATOM_HEADER_SIZE)
        if atom_header[4:8] == b'cmov':
            raise RuntimeError('moov atom is compressed')
        elif atom_header[4:8] != b'mvhd':
            raise RuntimeError('expected to find "mvhd" header.')
        else:
            f.seek(4, 1)
            creation_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
            creation_time = DateTime.fromtimestamp(creation_time)
            if creation_time.year < 1990:  # invalid or censored data
                creation_time = None

            modification_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
            modification_time = DateTime.fromtimestamp(modification_time)
            if modification_time.year < 1990:  # invalid or censored data
                modification_time = None

    return creation_time, modification_time

# INFO: Main routine
logging.info("Opening...")
for video_path in all_videos:
    try:
        modified_timestsamp = datetime.fromtimestamp(video_path.stat().st_mtime)
        create_date, modif_date = get_mov_timestamps(video_path)
        oldest_date = None
        if create_date == None and modif_date == None:
            oldest_date = modified_timestsamp
        elif create_date == None:
            if modified_timestsamp.year < 2000:
                oldest_date = modif_date
            else:
                oldest_date = modified_timestsamp if modified_timestsamp < modif_date else  modif_date
        elif modif_date == None:
            if modified_timestsamp.year < 2000:
                oldest_date = create_date
            else:
                oldest_date = modified_timestsamp if modified_timestsamp < create_date else create_date
        else:
            oldest_date = create_date if create_date < modif_date else modif_date

        oldest_date = oldest_date.strftime("%Y-%m")
        # INFO: Move to corresponding directory
        dir_path = Path(target_path + oldest_date)
        if not dir_path.exists():
            dir_path.mkdir()
        final_video_path = Path(str(dir_path) + "\\" + video_path.name)
        if final_video_path.exists():
            final_video_path = str(dir_path) + f"\\{video_path.stem}_duplicate_{unique_n[iUnique]}{video_path.suffix}"
            iUnique = iUnique + 1
        else:
            final_video_path = str(dir_path) + "\\" + video_path.name
        
        shutil.move(str(video_path), final_video_path)
    except Exception as ex:
        numb_errors += 1
        try:
            logging.error(traceback.format_exc())
            err_path = Path(error_path)
            if not err_path.exists():
                err_path.mkdir()
            str_video_path = str(video_path)
            full_path_in_err_path = str(err_path) + "\\" + video_path.name
            final_path = Path(full_path_in_err_path)
            if final_path.exists():
                final_path = str(err_path) + f"\\{video_path.stem}_duplicate_{unique_n[iUnique]}{video_path.suffix}"
                iUnique = iUnique + 1
            else:
                final_path = full_path_in_err_path
            shutil.move(str_video_path, final_path)
        except Exception as ex:
            logging.error(traceback.format_exc())
logging.info(f"Closing with {numb_errors} errors.")