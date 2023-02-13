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
import random

Image.MAX_IMAGE_PIXELS = None
# Configure logging
logging.basicConfig(
	filename="D:\\_projects_github\\utilities\\move_images_videos_logs.log",
	datefmt='%Y-%m-%d %H:%M:%S', 
	format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
	level=logging.INFO)

# Setup unique numbers
unique_n = list(range(5, 10000))
random.shuffle(unique_n)

# Paths
target_path = 'D:\TEMP_IMAGES\\'
error_path = 'D:\TEMP_ERRORS\\'
all_images_path = Path('D:\\TEMP')
files = list(all_images_path.rglob('*.*'))

logging.info(f"Opening {all_images_path}, found {len(files)} files.")
number_files_moved = 0
iUnique = 0
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
        final_path_image = Path(str(dir_path) + "\\" + image_path.name)
        if final_path_image.exists():
            final_path_image = str(dir_path) + f"\\{image_path.stem}_duplicate_{unique_n[iUnique]}{image_path.suffix}"
            iUnique = iUnique + 1
        else:
            final_path_image = str(dir_path) + "\\" + image_path.name
        
        shutil.move(str(image_path), final_path_image)
        number_files_moved = number_files_moved + 1
    except Exception as e:
        logging.error(traceback.format_exc())
        err_path = Path(error_path)
        if not err_path.exists():
            err_path.mkdir()
        str_image_path = str(image_path)
        full_path_in_err_path = str(err_path) + "\\" + image_path.name
        final_path = Path(full_path_in_err_path)
        if final_path.exists():
            final_path = str(err_path) + f"\\{image_path.stem}_duplicate_{unique_n[iUnique]}{image_path.suffix}"
            iUnique = iUnique + 1
        else:
            final_path = full_path_in_err_path
        shutil.move(str_image_path, final_path)
	
logging.info(f"Closing {all_images_path}, {number_files_moved} files have been moved.")
