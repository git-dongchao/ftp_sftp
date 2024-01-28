#!/usr/bin/python
#coding:utf-8

import sys
import os
from utils_helper import *
from utils_ftp import *
from utils_sftp import *

def main(argv):
    
    if len(argv) != 4:
        ToolTipWindow.Error('parameter count error', 'count=[%d]' % len(argv))
        return
        
    outer_inner = int(argv[1])
    type = int(argv[2])
    upload = argv[3]

    path = os.path.dirname(os.path.realpath(sys.executable))
    filepath = os.path.join(path, 'ftp.json')
    conf = LoadJson(filepath)
    if conf is None:
        return    
    host = host = conf['outer_host'] if outer_inner == 1 else conf['inner_host']
    port = conf['port']
    username = conf['username']
    password = conf['password']
    remote_path = conf['outer_path'] if outer_inner == 1 else conf['inner_path']

    ftp = FTPConnection(host, port, username, password)
    if port == 22:
        ftp = SFTPConnection(host, port, username, password)
    if ftp.connect() == False:
        ToolTipWindow.Error('connect host fail', 'host=[%s:%d]' % (host, port))
        return
    if ftp.is_dir_exist(remote_path) == False:
        ftp.mkdir(remote_path)
    
    is_file = os.path.isfile(upload)
    
    tooltip = ToolTipWindow()
    uid = uuid16()
    if is_file and (upload.endswith('.zip') or upload.endswith('.7z') or upload.endswith('.tar')  or upload.endswith('.tar.gz')):
        if os.stat(upload).st_size > 1024 * 1024 * 5:
            tooltip.show('upload start', '%s=[%s]' % ('file' if is_file else 'directory', os.path.basename(upload)))
        ftp.upload(os.path.join(remote_path, os.path.basename(upload) + '.raw_file_' + uid), upload)
    else:
        ext = '.zip' + '_dir_' + uid
        if is_file:
            ext = '.zip' + '_file_' + uid
        file = Zip.zip(upload, './', ext)
        if os.stat(file).st_size > 1024 * 1024 * 5:
            tooltip.show('upload start', '%s=[%s]' % ('file' if is_file else 'directory', os.path.basename(upload)))
        ftp.upload(os.path.join(remote_path, os.path.basename(file)), file)
        os.remove(file)
    
    tooltip.info('upload success', '%s=[%s]' % ('file' if is_file else 'directory', os.path.basename(upload)))

if (__name__ == '__main__'):
    main(sys.argv)
