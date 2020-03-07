#!/usr/bin/env python3
import os, shutil, time, sys
from os import path
from pathlib import Path
from signal import signal, SIGINT
from sys import exit
from colorama import init, Fore, Back, Style
init(autoreset=True) ## Autorest color back to default after each print used with colorama

## Preset Colors
COLOR_END       = Style.RESET_ALL               ## RESET/END
COLOR_GREEN     = Fore.GREEN + Style.BRIGHT     ## SUCCESS
COLOR_RED       = Fore.RED + Style.BRIGHT       ## ERROR
COLOR_YELLOW    = Fore.YELLOW + Style.BRIGHT    ## INFO
COLOR_CYAN      = Fore.CYAN + Style.BRIGHT

## Version number
VERSION = '1.4.0'

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
        if EXIST:
            print(DIRS[DIR] + '\t:\t' + COLOR_GREEN + str(EXIST))
        if not EXIST:
            print(COLOR_YELLOW + DIRS[DIR] + '\t: ' + COLOR_RED + str(EXIST))
            print(COLOR_RED + '\nError\t: ' + COLOR_END + 'Please ensure that specified directories exists.')
            exit(-1)
    print(COLOR_YELLOW + '\nINFO\t: ' + COLOR_END + 'Directories loaded ...')

## The checkExist() function is used to poll the target directory for new files being added.
## Once a file has been detected, it will move it to the pre-defined directories.

def checkExist():
    before = []
    print('\n' + COLOR_YELLOW + f'¯\(◉‿◉)/¯ Watching {TARGET} for change ¯\(◉‿◉)/¯')
    while True:
        time.sleep(TIME)
        after = dict ([(f, None) for f in os.listdir (TARGET)])
        added = [f for f in after if not f in before]
        if added:
            print(COLOR_YELLOW + '\nNew file(s) detected :' + COLOR_CYAN + f'{added}')
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
                    print(COLOR_YELLOW + '\nINFO : ' + COLOR_END + f'{target_file} already exist in {dest}, appending datetime.') 
                    timestr = time.strftime("%Y%m%d-%H%M%S-",time.localtime())
                    os.rename(target_file,path.join(TARGET, timestr+f))
                else: 
                    print(COLOR_YELLOW + '\nINFO : ' + COLOR_END +f'{target_file} ends with {e} and should be stored in {dest}')
                    shutil.move(target_file, dest)
                    print(COLOR_YELLOW + 'INFO : ' + COLOR_END + COLOR_GREEN + 'File moved Successfully!')

## The signalHandler function is used to terminate the script when ctrl + C is detected

def signalHandler(sig, frame):
    print(COLOR_GREEN + '\nAuto Sorter script terminated. Farewell!')
    exit(0)

def welcome():
    print(COLOR_CYAN + '''
                _           _____            _            
     /\        | |         / ____|          | |           
    /  \  _   _| |_ ___   | (___   ___  _ __| |_ ___ _ __ 
   / /\ \| | | | __/ _ \   \___ \ / _ \| '__| __/ _ \ '__|
  / ____ \ |_| | || (_) |  ____) | (_) | |  | ||  __/ |   
 /_/    \_\__,_|\__\___/  |_____/ \___/|_|   \__\___|_|   
                                                          
''' + COLOR_RED + ' Version ' + COLOR_YELLOW + VERSION + COLOR_RED + '  Twitter ' + COLOR_YELLOW + '@ K0p1_')

## SwitchHandler() function is used to seek arguments entered by the user and return
## the appropriate values i.e. displaying help messages ... etc 
## WIP: leaving this here for future developments/implementation  

def switchHandler():
    flag = {
        '--version' : f'AutoSorter version {VERSION}. Fine me at:\n\nGithub: @K0p1-Git\nTwitter: @K0p1_\n',
        '--help'    : '''This is a sample test help message.
AutoSorter does not require any arugments to run.\n''',
        '-h'        : '''This is a sample test help message.
AutoSorter does not require any arugments to run.\n'''
    }
    if (len(sys.argv) > 1):
        for arg in sys.argv[1:]:
            try:
                if ((arg == '--help') or (arg == '-h') or (arg == '--version')):
                    print(COLOR_CYAN + flag[arg])
                    exit(0)
                print(flag[arg])
            except KeyError:
                print(COLOR_RED + f'Unknow {arg} argument found...')
                print(COLOR_RED + f'Usage: {sys.argv[0]} --help to display help message\n') 
                exit(-1)

## Main function starts here

def main():
    signal(SIGINT, signalHandler)
    switchHandler()
    welcome()
    initialize()
    checkExist()

if __name__ == '__main__':
    main()
