# hrv_file_transfer

## Overview
This repo contains python scripts used to transfer files containg scripted commands related to automated deployment of an MS-SID instrument. See hrv-scriptgen repo for generating the files.

## Starting point
http://firmlyembedded.co.za/useful-python-script-to-send-and-receive-serial-data/

## Building standalone program
python -m auto_py_to_exe
This will open a localhost in web browser
Point to cfgGen.py in Script Location
Point to either .ico image in the img folder for Icon
Run Convert .py to .exe

## Using the script
The program relies having a serial device to transfer across to the MS-SID system control board (SCB).
USB-to-serial devices plugged into the computer running the program works well.
The SCB must have an SD card installed and mounted.

## Future Improvements
- load multiple files and concatenate to write all to msoperat.cfg
- fix transfer removing line feeds and adding more carriage returns
- correct checksum