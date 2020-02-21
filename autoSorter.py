#!/usr/bin/env python3
import os, time
from os import path
from signal import signal, SIGINT
from sys import exit

## Directories
ROOT    = '/root'
TARGET  = '/Downloads' 
DIRS    = {
    'PICTURES'  :'/Pictures',
    'DOCUMENTS' :'/Documents',
    'VIDEOS'    :'/Videos'
}
## Extensions || Things to do, allow extension to be load via text file
# EXT = open('extDict.txt','r')
IMAGES = ['JPEG']

## Set the time it takes to poll
TIME = 0.5 

def initialize():
    print('\nInitializing, Checking if directories exist.')
    for DIR in DIRS:
        EXIST = path.exists(ROOT+DIRS[DIR])
        print(ROOT+DIRS[DIR] + '\t:\t' + str(EXIST))
        if not EXIST:
            print('\nError\t:\tPlease ensure that specified directories exists.')
            exit(-1)

def checkExist():
    before = dict ([(f, None) for f in os.listdir (ROOT+TARGET)])
    while True:
        time.sleep(TIME)
        after = dict ([(f, None) for f in os.listdir (ROOT+TARGET)])
        added = [f for f in after if not f in before]
        #removed = [f for f in before if not f in after]
        if added:
            print(f'\nNew file(s) detected : {added}')
        before = after        

def moveFile(added):
    

def signal_handler(sig, frame):
    print('\nAuto Sorter script terminated. Farewell!')
    exit(0)

def main():
    signal(SIGINT, signal_handler)
    initialize()
    checkExist()

if __name__ == '__main__':
    main()
