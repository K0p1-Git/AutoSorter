#!/usr/bin/env python3
import os, shutil, time
from os import path
from pathlib import Path
from signal import signal, SIGINT
from sys import exit

## Directories are delclared here
USER = Path.home()
TARGET  = path.join(USER, 'Downloads')
DIRS    = {
    'PICTURES'  : path.join(USER, 'Pictures'),
    'DOCUMENTS' : path.join(USER, 'Documents'),
    'VIDEOS'    : path.join(USER, 'Videos')
}
## Extensions are declared here or be loaded via text file. 
EXT = {
    'jpeg':'PICTURES',
    'png':'PICTURES'
}

with open("extensions.txt") as f:
    for line in f:
       (key, val) = line.split('\t')
       EXT[key] = val.strip()

## Set polling rate in seconds
TIME = 0.5 

## The initialize() function is used to check whether declared directories
## and its path exist within the system else terminate the program.

def initialize():
    print('\nInitializing, Checking if directories exist.')
    for DIR in DIRS:
        EXIST = path.exists(DIRS[DIR])
        print(DIRS[DIR] + '\t:\t' + str(EXIST))
        if not EXIST:
            print('\nError\t:\tPlease ensure that specified directories exists.')
            exit(-1)
    print('\nDirectories loaded ...')

## The checkExist() function is used to poll the target directory for new files being added.
## Once a file has been detected, it will move it to the pre-defined directories.

def checkExist():
    before = []
    print(f'\n¯\(◉‿◉)/¯ Watching {TARGET} for change ¯\(◉‿◉)/¯')
    while True:
        time.sleep(TIME)
        after = dict ([(f, None) for f in os.listdir (TARGET)])
        added = [f for f in after if not f in before]
        #removed = [f for f in before if not f in after]
        if added:
            print(f'\nNew file(s) detected : {added}')
            moveFile(added, EXT)
        before = after        

## The moveFile() function takes in a list containing newly added files

def moveFile(files, extensions):
    for f in files:
        for e in extensions:
            if(f.lower().endswith(e)):
                target_file = path.join(TARGET, f)
                dest = DIRS[EXT[e]]
                ## Check to see whether file exist in the destination directory
                if (path.exists(path.join(dest, f))):
                    print(f'\nFile {target_file} already exist in {dest}, appending datetime.') 
                    timestr = time.strftime("%Y%m%d-%H%M%S-",time.localtime())
                    os.rename(target_file,path.join(TARGET, timestr+f))
                else: 
                    print(f'\nFile: {target_file} ends with {e} and should be stored in {dest}')
                    shutil.move(target_file, dest)
                    print('File moved')

## The signalHandler function is used to terminate the script when ctrl + C is detected

def signalHandler(sig, frame):
    print('\nAuto Sorter script terminated. Farewell!')
    exit(0)

def welcome():
    print('''
                _           _____            _            
     /\        | |         / ____|          | |           
    /  \  _   _| |_ ___   | (___   ___  _ __| |_ ___ _ __ 
   / /\ \| | | | __/ _ \   \___ \ / _ \| '__| __/ _ \ '__|
  / ____ \ |_| | || (_) |  ____) | (_) | |  | ||  __/ |   
 /_/    \_\__,_|\__\___/  |_____/ \___/|_|   \__\___|_|   
                                                          
    Version 1.2.1 -  Twitter @ K0p1_

            ''')

## Main function starts here

def main():
    signal(SIGINT, signalHandler)
    welcome()
    initialize()
    checkExist()

if __name__ == '__main__':
    main()
