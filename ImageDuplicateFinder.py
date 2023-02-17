import hashlib
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import os
import time
from datetime import date, datetime
import traceback
import logging
# Configure Image
import json
Image.MAX_IMAGE_PIXELS = None

# Configure logging
logging.basicConfig(
	filename="D:\\_projects_github\\utilities\\image_duplicate_finders.log",
	datefmt='%Y-%m-%d %H:%M:%S', 
	format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
	level=logging.INFO)

# Paths
all_images_path = Path('G:\images_videos\pictures')
files = list(all_images_path.rglob('*.*'))

# Define functions
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def write_duplicates():    
    logging.info(f"Opening {all_images_path}, found {len(files)} files.")
    duplicates = {}

    for image_path in files:
        final_modif_date = None
        try:
            exifdata = None
            with Image.open(image_path) as image:
                exifdata = image.getexif()
            
            if exifdata.get(306) is not None:
                final_modif_date = datetime.strptime(exifdata.get(306), 
                '%Y:%m:%d %H:%M:%S').strftime("%Y-%m-%d_%H:%M")
            else:
                ti_m = os.path.getmtime(image_path)
                m_ti = time.ctime(ti_m)
                final_modif_date = date.fromtimestamp(ti_m).strftime("%Y-%m-%d_%H:%M")
        except PermissionError as perm:
            logging.error(traceback.format_exc())
            continue
        except Exception as e:
            # logging.error(traceback.format_exc())
            ti_m = os.path.getmtime(image_path)
            m_ti = time.ctime(ti_m)
            final_modif_date = date.fromtimestamp(ti_m).strftime("%Y-%m-%d_%H:%M")
        finally:
            try:
                hash = md5(image_path)
                key = hash
                if final_modif_date is not None:
                    key = hash + "_" + final_modif_date
                if key in duplicates:
                    duplicates[key].append(str(image_path))
                else:
                    duplicates[key] = [str(image_path)]
            except PermissionError as perm:
                logging.error(traceback.format_exc())
    # Only get duplicated keys
    final_duplicates = {}
    for x, y in duplicates.items():
        if len(y) > 1:
            final_duplicates[x] = y
    json_object = json.dumps(final_duplicates, indent=4)

    with open("duplicates.json", "w") as outfile:
        outfile.write(json_object)
    logging.info(f"Closing {all_images_path}, {len(files)} md5 computed.")

def read_duplicates():
    with open('duplicates.json', 'r') as openfile:
    # Reading from json file
        json_object = json.load(openfile)
        for x, y in json_object.items():
            if len(y) > 1:
                print(x, y)
		
# dupli: Dictionnary
def remove_duplicates():
    with open('duplicates.json', 'r') as openfile:
        logging.info("Begin deleting files")
        json_object = json.load(openfile)
        items = json_object.items()
        len_items = number_removed_files()
        logging.info(f'${len_items} files to delete')
        count = 0
        for x, y in items:
            arr_deletes = y[1:]
            count = count + len(arr_deletes)
            try:
                for elem in arr_deletes:
                    p = Path(elem)
                    if p.is_file():
                        os.remove(p)
            except Exception as e:
                logging.error(traceback.format_exc())
        logging.info(f'${count} files deleted.')
        logging.info("Finish deleting files")
                   

def number_removed_files():
    with open('duplicates.json', 'r') as openfile:
        json_object = json.load(openfile)
        count = 0
        for x, y in json_object.items():
            arr_deletes = y[1:]
            count = count + len(arr_deletes)
        return count

# remove_duplicates(duplicates)

# write_duplicates()
# read_duplicates()
# remove_duplicates()
# print(number_removed_files())