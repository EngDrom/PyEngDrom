
from org.pyengdrom.config.const import QT_REBOOT
from org.pyengdrom.config.reader import ProjectConfig
from org.pyengdrom.gui.enginit import EngDromInitializer
from org.pyengdrom.gui.index     import EngdromGUI

import sys

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", type=str, help="Project folder, if no folder given, switches to create project mode")
    args = parser.parse_args()
    
    if args.folder is None:
        err_code = EngDromInitializer(args).err_code
        if err_code != QT_REBOOT: exit(0)
    
    EngdromGUI(args)

if __name__ == "__main__": main()
