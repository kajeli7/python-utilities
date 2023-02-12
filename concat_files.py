import os
import re

all_files = []
for html_file in os.listdir():
    if html_file[-3:] != '.py':
        all_files.append(html_file)

with open('E:\en_cours\stage\datawarehouse\\remove_me_all.csv', 'w') as outfile:
    for fname in all_files:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
