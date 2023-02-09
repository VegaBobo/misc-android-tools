#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join
import sys
import pathlib

pit_path=sys.argv[1]
extracted_firmware_path=""

class Partition(object):
    name = "" # eg: BOOT
    filename = "" # eg: boot.img

    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

try:
    extracted_firmware_path=sys.argv[2]
except:
    extracted_firmware_path=pathlib.Path(__file__).parent.resolve()
    # firmware directory not specified, using current folder as firmware path

with open(pit_path) as pitFile:
    lines = [line.rstrip() for line in pitFile]

partitions = []
lastLine=""

for i in lines:
    if(("Flash Filename" in i) and ("-" not in i) and ("Flash Filename:" != i)):
        i=i.replace("Flash Filename: ","")
        lastLine=lastLine.replace("Partition Name: ","")
        p=Partition(lastLine,i)
        partitions.append(p)
    lastLine=i

filesInDirectory = [f for f in listdir(extracted_firmware_path) if isfile(join(extracted_firmware_path, f))]
partitions2Flash = []
for i in partitions:
    has=False
    for v in filesInDirectory:
        if(v==i.filename):
            has=True
    if(has):
        partitions2Flash.append(i)

fullString=""

for i in partitions2Flash:
    fullString=fullString+"--"+i.name+" "+i.filename+" "

print("You should run this command to flash on your Samsung device: ")
print("heimdall flash " + fullString)
