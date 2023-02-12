from bs4 import BeautifulSoup
import os
import re

all_files = []
for html_file in os.listdir():
    if html_file[-3:] != '.py':
        title = ''
        with open(html_file, encoding="utf8") as file:
            soup = BeautifulSoup(file)
            title = soup.title.string
            title = re.sub('\W', '_', title) + ".html"
        os.replace(html_file, title)