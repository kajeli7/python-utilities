import cv2 as cv
from pathlib import Path, WindowsPath

all_videos = (Path('D:\\TEMP').rglob('*.*'))

for video_path in all_videos:
    video_obj = cv.VideoCapture(str(video_path))
    
    print(str(video_path) + " " + str(video_obj.isOpened()) + " " + video_obj.getBackendName())
