#!/usr/bin/env python
#coding:utf-8

import sys
import os
from utils_helper import *

def main(argv):
    cwd = os.getcwd()
    DeleteMenu('FTP upload')
    RegisterSelectMenu('FTP upload', os.path.join(cwd, 'ftp_upload.exe 1'))
    DeleteMenu('FTP download')
    RegisterMenu('FTP download', os.path.join(cwd, 'ftp_download.exe 1'))
    print('register success')
    os.system("pause")

if (__name__ == '__main__'):
    main(sys.argv)
