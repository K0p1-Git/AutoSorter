#!/usr/bin/env python3
import os, time
from os import path
from signal import signal, SIGINT
from sys import exit

## Directories are delclared here
TARGET  = '/root/Downloads/' 
DIRS    = {
    'PICTURES'  :'/root/Pictures',
    'DOCUMENTS' :'/root/Documents',
    'VIDEOS'    :'/root/Videos'
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

## The checkExist() function is used to poll the target directory for new files being added.
## Once a file has been detected, it will move it to the pre-defined directories.

def checkExist():
    before = []
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
                print(f'\nFile: {TARGET+f} end with {e} and should be stored in {DIRS[EXT[e]]}')
                os.system(f'mv {TARGET+f} {DIRS[EXT[e]]}')
                print('File moved')

## The signalHandler function is used to terminate the script when ctrl + C is detected

def signalHandler(sig, frame):
    print('\nAuto Sorter script terminated. Farewell!')
    exit(0)

## Main function starts here

def main():
    signal(SIGINT, signalHandler)
    print(EXT)
    initialize()
    checkExist()

if __name__ == '__main__':
    main()
