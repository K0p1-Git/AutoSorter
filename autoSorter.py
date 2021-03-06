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
VERSION = '1.4.1'

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

## Import (extension, Category, location) from text file
def userImport(index):
    if (sys.argv[index] == '--import'):
        try:
            FILE = str(sys.argv[index+1])
            if FILE:
                with open(FILE) as f:
                    for line in f:
                        (ext, cat, loc) = line.split('\t',2)
                        EXT[ext] = cat.strip()
                        DIRS[cat] = path.join(USER, loc.strip())
            elif not FILE:
                with open("extensions.txt") as f:
                    for line in f:
                        (ext, cat, loc) = line.split('\t',2)
                        EXT[ext] = cat.strip()
                        DIRS[cat] = path.join(USER, loc.strip())
        except FileNotFoundError:
            print(COLOR_RED + f'Unkown file {sys.argv[index+1]} not found.') 
            print(COLOR_RED + f'Usage\t: {sys.argv[0]} [FILE]\n')
            exit(-1)
        except Exception as ex:
            print(COLOR_RED + f'Error\t: {sys.argv[0]} [FILE]\n')
            exit(-1)
            
## Set polling rate in seconds
TIME = 0.5
def setPoll(index):
    global TIME
    if (sys.argv[index] == '--poll'):
        try:
            TIME = float(sys.argv[index+1])
        except ValueError as verr:
            print(COLOR_RED + f'Usage\t: {sys.argv[0]} (Float in second i.e 0.5)\n')
            exit(-1)
        except Exception as ex:
            print(COLOR_RED + f'Error\t: {sys.argv[0]} (Float in second i.e 0.5)\n')
            exit(-1)

## SwitchHandler() function is used to seek arguments entered by the user and return
## the appropriate values i.e. displaying help messages ... etc 
## WIP: leaving this here for future developments/implementation  

def switchHandler():
    skip = False
    flag = {
        '--help'    : 'This is a sample test help message. AutoSorter does not require any arugments to run.\n',
        '-h'        : 'This is a sample test help message. AutoSorter does not require any arugments to run.\n',
        '--poll'    : 'Set polling time. Default set at 0.5 poll per second.\n',
        '--import'  : 'User self defined file for extensions and directories. Default set: extensions.txt\n',
        '--version' : f'AutoSorter version {VERSION}. Fine me at:\n\nGithub: @K0p1-Git\nTwitter: @K0p1_\n'
    }
    if (len(sys.argv) > 1):
        for argc, arg in enumerate(sys.argv[1:], start=1):
            try:
                if skip:
                    skip = False
                    continue
                elif ((arg == '--help') or (arg == '-h') or (arg == '--version')):
                    print(COLOR_CYAN + flag[arg])
                    for key, value in flag.items():
                        print(f'{key:<13} {value}')
                    exit(0)
                elif (arg == '--poll'):
                    setPoll(argc)
                    skip = True
                elif (arg == '--import'):
                    userImport(argc)
                    skip = True
                else:
                    print(COLOR_RED + f'Unknow {arg} argument found...')
                    print(COLOR_RED + f'Usage: {sys.argv[0]} --help to display help message\n') 
                    exit(-1)
            except KeyError:
                print(COLOR_RED + f'Unknow {arg} argument found...')
                print(COLOR_RED + f'Usage: {sys.argv[0]} --help to display help message\n') 
                exit(-1)
            except Exception as ex:
                print(COLOR_RED + f'\nError\t: parsing of arugments failed)')
                exit(-1)

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
    print(COLOR_GREEN + '\n\nAuto Sorter script terminated. Farewell!')
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

## Main function starts here

def main():
    signal(SIGINT, signalHandler)
    switchHandler()
    welcome()
    print(COLOR_YELLOW + f'\nINFO: Polling time set at poll per {TIME} second(s).\n') ## Debug
    initialize()
    checkExist()

if __name__ == '__main__':
    main()
