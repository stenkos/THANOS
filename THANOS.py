# THANOS source code
# by stenkos (github.com/stenkos)
# version: 1
# start date: 2023-01-27
# wyd: coding a script that deletes half the files in your specified directory,
# this is a command line app that parses your inputted directory and does stuff
# with it
# ------------------------------------------------------------------------------

import sys
import os
from pathlib import Path
from time import sleep as wait
from random import randint
import shutil

#this section defines a bunch of text coolness i use later
#---------------------------------------------------------

thanosANSI = """
    ███        ▄█    █▄       ▄████████ ███▄▄▄▄    ▄██████▄     ▄████████ 
▀█████████▄   ███    ███     ███    ███ ███▀▀▀██▄ ███    ███   ███    ███ 
   ▀███▀▀██   ███    ███     ███    ███ ███   ███ ███    ███   ███    █▀  
    ███   ▀  ▄███▄▄▄▄███▄▄   ███    ███ ███   ███ ███    ███   ███        
    ███     ▀▀███▀▀▀▀███▀  ▀███████████ ███   ███ ███    ███ ▀███████████ 
    ███       ███    ███     ███    ███ ███   ███ ███    ███          ███ 
    ███       ███    ███     ███    ███ ███   ███ ███    ███    ▄█    ███ 
   ▄████▀     ███    █▀      ███    █▀   ▀█   █▀   ▀██████▀   ▄████████▀  
                                                                          """

inevitableANSI = """

▪       ▄▄▄· • ▌ ▄ ·.     ▪    ▐ ▄ ▄▄▄ . ▌ ▐·▪  ▄▄▄▄▄ ▄▄▄· ▄▄▄▄· ▄▄▌  ▄▄▄ .
██     ▐█ ▀█ ·██ ▐███▪    ██  •█▌▐█▀▄.▀·▪█·█▌██ •██  ▐█ ▀█ ▐█ ▀█▪██•  ▀▄.▀·
▐█·    ▄█▀▀█ ▐█ ▌▐▌▐█·    ▐█ ·▐█▐▐▌▐▀▀▪▄▐█▐█•▐█· ▐█.▪▄█▀▀█ ▐█▀▀█▄██▪  ▐▀▀▪▄
▐█▌    ▐█ ▪▐▌██ ██▌▐█▌    ▐█ ▌██▐█▌▐█▄▄▌ ███ ▐█▌ ▐█▌·▐█ ▪▐▌██▄▪▐█▐█▌▐▌▐█▄▄▌
▀▀▀     ▀  ▀ ▀▀  █▪▀▀▀    ▀▀ ▀▀▀ █▪ ▀▀▀ . ▀  ▀▀▀ ▀▀▀  ▀  ▀ ·▀▀▀▀ .▀▀▀  ▀▀▀ ▀  ▀  ▀ 

"""

fool = """
 ▄· ▄▌      ▄• ▄▌     ▄▄·        ▐ ▄ .▄▄ · ▪   ·▄▄▄▄  ▄▄▄ .▄▄▄  
▐█▪██▌▪     █▪██▌    ▐█ ▌▪▪     •█▌▐█▐█ ▀. ██  ██▪ ██ ▀▄.▀·▀▄ █·
▐█▌▐█▪ ▄█▀▄ █▌▐█▌    ██ ▄▄ ▄█▀▄ ▐█▐▐▌▄▀▀▀█▄▐█· ▐█· ▐█▌▐▀▀▪▄▐▀▀▄ 
 ▐█▀·.▐█▌.▐▌▐█▄█▌    ▐███▌▐█▌.▐▌██▐█▌▐█▄▪▐█▐█▌ ██. ██ ▐█▄▄▌▐█•█▌
  ▀ •  ▀█▄▀▪ ▀▀▀     ·▀▀▀  ▀█▄▀▪▀▀ █▪ ▀▀▀▀ ▀▀▀ ▀▀▀▀▀•  ▀▀▀ .▀  ▀
• ▌ ▄ ·. ▄▄▄ .     ▄▄▄·     ·▄▄▄            ▄▄▌      ▄▄      ▄▄ 
·██ ▐███▪▀▄.▀·    ▐█ ▀█     ▐▄▄·▪     ▪     ██•      ██▌     ██▌
▐█ ▌▐▌▐█·▐▀▀▪▄    ▄█▀▀█     ██▪  ▄█▀▄  ▄█▀▄ ██▪      ▐█·     ▐█·
██ ██▌▐█▌▐█▄▄▌    ▐█ ▪▐▌    ██▌.▐█▌.▐▌▐█▌.▐▌▐█▌▐▌    .▀      .▀ 
▀▀  █▪▀▀▀ ▀▀▀      ▀  ▀     ▀▀▀  ▀█▄▀▪ ▀█▄▀▪.▀▀▀      ▀       ▀ 
"""

info = """
You have just granted this script the power of Thanos. In one snap he will
eradicate half of the folder you specified, all he needs now is a confirmation.
[y/n]. Do you got the balls? """


def printSlow(str, x):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        wait(x)

#this section of code is meant to make sure there is only one arg
#arg_status is True if there is only one arg and False in any other situation
#----------------------------------------------------------------------------

# Take the first argument as the path
try:
    thePath = sys.argv[1]
except:
    arg_status = False
    
# Use the path object as needed
try:
    formatPath = thePath.replace("\\", "/")
    formatPath = formatPath.replace("\n", "")
except:
    arg_status = False

try:
    if sys.argv[1]:
        try:
            if sys.argv[2]:
                arg_status = False
        except:
            arg_status = True
except:
    arg_status = False

if not arg_status:
    print("""you did it wrong, here's how you use it correctly:
if you are running the python script use `python THANOS.py <path>`
where <path> is a directory
if you are running the binary use `THANOS <path>`""")


#this is where fun starts
#this part of the script is now what people see when they run it properly
#------------------------------------------------------------------------

def deletion():
    count = 0
    non_existent = False
    try:
        the_universe = os.listdir(formatPath)
    except:
        non_existent = True
    if not non_existent:
        half_of_the_universe = (the_universe[::2])
        for x in half_of_the_universe:
            try:
                shutil.rmtree(formatPath + "/" + x)
            except:
                try:
                    os.remove(formatPath + "/" + x)
                except:
                    count = count + 1
        if count > 0:
            print("Skipped", count, "files/folders")
        printSlow("""

▪  ▄▄▄▄▄    ▪  .▄▄ ·     ·▄▄▄▄         ▐ ▄ ▄▄▄ .
██ •██      ██ ▐█ ▀.     ██▪ ██ ▪     •█▌▐█▀▄.▀·
▐█· ▐█.▪    ▐█·▄▀▀▀█▄    ▐█· ▐█▌ ▄█▀▄ ▐█▐▐▌▐▀▀▪▄
▐█▌ ▐█▌·    ▐█▌▐█▄▪▐█    ██. ██ ▐█▌.▐▌██▐█▌▐█▄▄▌
▀▀▀ ▀▀▀     ▀▀▀ ▀▀▀▀     ▀▀▀▀▀•  ▀█▄▀▪▀▀ █▪ ▀▀▀ 
""", 0.0001)
        wait(0.7)
    
    else:
        printSlow(fool, 0.0001)
        wait(0.75)
        print("""
THAT DIRECTORY DOESN'T EXIST""")
    

def main():
    wait(0.5)
    printSlow(thanosANSI, 0.0001)
    wait(0.5)
    confirmation = input(info)
    if confirmation.lower() == "y":
        deletion()
    else:
        input("""
y was not specified and for safety the script will not execute.
Please press ENTER to exit the script.""")




if arg_status:
    main()




