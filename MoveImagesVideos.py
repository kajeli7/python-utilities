# Recursively look for images in specific director
# only get image last modified date and move image to correct directory
# Process videos for later time
# Use software to find duplicate in images
from pathlib import Path, WindowsPath
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
import os
import time
from datetime import date, datetime
import traceback
import logging

Image.MAX_IMAGE_PIXELS = None
# Configure logging
logging.basicConfig(
	filename="D:\\_projects_github\\utilities\\move_images_videos_logs.log",
	datefmt='%Y-%m-%d %H:%M:%S', 
	format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
	level=logging.INFO)

# Paths
target_path = 'D:\TEMP_IMAGES\\'
error_path = 'D:\TEMP_ERRORS\\'
all_images_path = Path('D:\\TEMP')
files = list(all_images_path.rglob('*.*'))

logging.info(f"Opening {all_images_path}, found {len(files)} files.")
number_files_moved = 0

for image_path in files:
    try:
        exifdata = None
        with Image.open(image_path) as image:
            exifdata = image.getexif()
        
        final_modif_date = None
        if exifdata.get(306) is not None:
            final_modif_date = datetime.strptime(exifdata.get(306), 
            '%Y:%m:%d %H:%M:%S').strftime("%Y-%m")
        else:
            ti_m = os.path.getmtime(image_path)
            m_ti = time.ctime(ti_m)
            final_modif_date = date.fromtimestamp(ti_m).strftime("%Y-%m")

        dir_path = Path(target_path + final_modif_date)
        if not dir_path.exists():
            dir_path.mkdir()
        
        shutil.move(str(image_path), str(dir_path)) # TODO: Maybe add dir_path + image_path.name to Avoid file losses like what happened to you ???
        number_files_moved = number_files_moved + 1
    except Exception as e:
        logging.error(traceback.format_exc())
        err_path = Path(error_path)
        if not err_path.exists():
            err_path.mkdir()
        shutil.move(str(image_path), str(err_path))
	
logging.info(f"Closing {all_images_path}, {number_files_moved} files have been moved.")
