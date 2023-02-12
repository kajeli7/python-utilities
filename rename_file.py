import os
import re

for file in os.listdir():
    if ".hahaha" in file:
        file_name = file.split("_")
        newfile_name = "mvt_" + file_name[1]
        os.replace(file, newfile_name)