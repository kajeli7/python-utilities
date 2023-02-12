import winsound
import sched, time
import os, sys

def alert(FREQUENCY=1500):
    winsound.Beep(FREQUENCY, 500)
    winsound.Beep(FREQUENCY, 500)

while True:
    time.sleep(1800)
    alert(750)
    time.sleep(30)
    alert()
