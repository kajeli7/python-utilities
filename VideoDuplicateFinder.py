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
	filename="D:\\_projects_github\\utilities\\video_duplicate_finders.log",
	datefmt='%Y-%m-%d %H:%M:%S', 
	format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
	level=logging.INFO)

# Paths
all_images_path = Path('G:\\TEMP_VIDEOS_ALL')
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
        try:
            hash = md5(image_path)
            key = hash
            if key in duplicates:
                duplicates[key].append(str(image_path))
            else:
                duplicates[key] = [str(image_path)]
        except Exception as e:
            logging.error(traceback.format_exc())
    # INFO: Only get duplicated keys
    final_duplicates = {}
    for x, y in duplicates.items():
        if len(y) > 1:
            final_duplicates[x] = y
    json_object = json.dumps(final_duplicates, indent=4)

    with open("duplicate_videos.json", "w") as outfile:
        outfile.write(json_object)
    logging.info(f"Closing {all_images_path}, {len(files)} md5 computed.")

def read_duplicates():
    with open('duplicate_videos.json', 'r') as openfile:
    # Reading from json file
        json_object = json.load(openfile)
        for x, y in json_object.items():
            if len(y) > 1:
                print(x, y)
		
# dupli: Dictionnary
def remove_duplicates():
    with open('duplicate_videos.json', 'r') as openfile:
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
    with open('duplicate_videos.json', 'r') as openfile:
        json_object = json.load(openfile)
        count = 0
        for x, y in json_object.items():
            arr_deletes = y[1:]
            count = count + len(arr_deletes)
        return count

write_duplicates()
# read_duplicates()
# remove_duplicates()
# print(number_removed_files())

# for file_path in files:
#     print(md5(file_path))