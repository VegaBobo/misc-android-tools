#!/usr/bin/python3
import xml.etree.ElementTree as etree
import hashlib
import os

inputfile = 'flashfile.xml'
outputfile = 'flashfile.txt'

print("Opening %s" % inputfile)
xmltree = etree.parse(inputfile)

step_elements = xmltree.findall('.//step')
phone_model = xmltree.find('.//phone_model').attrib['model']
if "_" in phone_model:
    phone_model = phone_model.split("_")[0]

flashfile = open(outputfile, "w+")
flashfile.write("#!/bin/sh" + "\n")

sanity_check = """
## ALWAYS CHECK SCRIPT BEFORE RUNNING !!!
## SEMPRE CHEQUE O SCRIPT ANTES DE RODAR !!!

FIRMWARE_DEVICE=%s
CONNECTED_DEVICE=$(fastboot getvar product 2>&1 | awk 'NR==1{print $2}')
if [ "$FIRMWARE_DEVICE" != "$CONNECTED_DEVICE" ]; then
    echo "This package is for $FIRMWARE_DEVICE, connected device is $CONNECTED_DEVICE."
    exit 1
fi

ACTIVE_SLOT=$(fastboot getvar current-slot 2>&1 | awk 'NR==1{print $2}')
if [ "$ACTIVE_SLOT" = "b" ]; then
    echo "\\"b/_b\\" slot is active, switching back to \\"a/_a\\""
    fastboot --set-active=a
fi
""" % phone_model

flashfile.write(sanity_check + "\n")

for e in step_elements:
    print('Processing \"%s\"' % etree.tostring(e, encoding='unicode').strip())
    cmd = "fastboot "
    operation = e.attrib['operation']
    match operation:
        case "flash":
            partition = e.attrib['partition']
            filename = e.attrib['filename']
            md5 = e.attrib['MD5']
            target_file = None
            try:
                target_file = open(filename, "rb")
            except:
                flashfile.close()
                os.remove(outputfile)
                raise Exception('Cannot proceed, %s file does not exist.' % filename)
            file_hash = hashlib.md5()
            while chunk := target_file.read(8192):
                file_hash.update(chunk)
            if md5 != file_hash.hexdigest():
                flashfile.close()
                os.remove(outputfile)
                raise Exception('Cannot proceed, %s checksum does not match, corrupted firmware?' % filename)
            cmd += "flash {} {}".format(partition, filename)
        case "oem" | "getvar":
            var = e.attrib['var']
            cmd += "{} {}".format(operation, var)
        case "erase":
            partition = e.attrib['partition']
            cmd += "erase {}".format(partition)
        case _: 
            flashfile.close()
            os.remove(outputfile)
            raise Exception('%s contains not supported operation, exiting..' % inputfile)
    flashfile.write(cmd + "\n")

flashfile.write("\necho \"Flash finished.\"\n")
flashfile.close()
print("Generated %s" % outputfile)
