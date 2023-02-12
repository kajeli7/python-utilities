#!/usr/bin/env python

import os

#tunes for beeporama: (frequence,duration)
tune1=[(1000,320),(900,10),(500,410),(400,10),(340,410),(300,10)]
tune2=[(1000,10),(500,10),(440,20),(340,2),(720,4),(880,40)]

tune=tune2

cmd='beep -f100 -l1 '

for i,j in tune: 
	cmd=cmd + ' -n -f '+ str(i) + ' -l'+str(j)

os.system(cmd)
