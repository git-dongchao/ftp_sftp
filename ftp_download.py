#!/usr/bin/python
#coding:utf-8

import sys
import win32api
import win32con
from utils_helper import *
from utils_ftp import *
from utils_sftp import *

def main(argv):

    if len(argv) != 4:
        ToolTipWindow.Error('parameter count error', 'count=[%d]' % len(argv))
        return

    outer_inner = int(argv[1])
    type = int(argv[2])
    download = None
    unzip_path = None
    if type == 1:   # select empty
        download = argv[3]
        unzip_path = argv[3]
    elif type == 2: # select directory
        download = os.path.dirname(argv[3])
        unzip_path = argv[3]
    elif type == 3: # select file
        download = os.path.dirname(argv[3])
        unzip_path = os.path.dirname(argv[3])
        
    path = os.path.dirname(os.path.realpath(sys.executable))
    filepath = os.path.join(path, 'ftp.json')
    conf = LoadJson(filepath)
    if conf is None:
        return
    host = conf['outer_host'] if outer_inner == 1 else conf['inner_host']
    port = conf['port']
    username = conf['username']
    password = conf['password']
    remote_path = conf['inner_path'] if outer_inner == 1 else conf['outer_path']
        
    ftp = FTPConnection(host, port, username, password)
    if port == 22:
        ftp = SFTPConnection(host, port, username, password)
    if ftp.connect() == False:
        ToolTipWindow.Error('connect host fail', 'host=[%s:%d]' % (host, port))
        return
    if ftp.is_dir_exist(remote_path) == False:
        ToolTipWindow.Error('not found directory', "directory=[%s]" % remote_path)
        return
    
    files = ftp.listdir(remote_path)
    if len(files) == 0:
        ToolTipWindow.Error('not found file', 'directory=[%s]' % remote_path)
        return
        
    files.sort(key = lambda f : f['modify'])
    file = files[-1]
    filename = files[-1]['filename']
    ext_name = os.path.splitext(filename)[-1]

    compress_type = ext_name.split('_', 3)[0]
    file_type = ext_name.split('_', 3)[1]    
    
    tooltip = ToolTipWindow()
    if file_type == 'file':
        download_filename = os.path.splitext(filename)[0]
        if os.path.exists(os.path.join(download, download_filename)):
            rv = win32api.MessageBox(0, "是否覆盖已有文件 : %s" % download_filename, "文件已存在", win32con.MB_OKCANCEL | win32con.MB_ICONQUESTION)
            if rv == win32con.IDCANCEL:
                return
        if int(file['size']) > 1024 * 1024 * 5:
            tooltip.show('download start', 'file=[%s]' % download_filename)

        if compress_type == '.zip':
            ftp.download(os.path.join(remote_path, filename), os.path.join(download, filename))
            Zip.unzip(filename, unzip_path)
            os.remove(filename)
        else:
            ftp.download(os.path.join(remote_path, filename), os.path.join(download, download_filename))
        tooltip.info('download success', 'file=[%s]' % download_filename, 100)
    elif file_type == 'dir':
        download_filename = os.path.splitext(filename)[0]
        if os.path.exists(os.path.join(download, download_filename)):
            rv = win32api.MessageBox(0, "是否覆盖已有目录 : %s" % download_filename, "目录已存在", win32con.MB_OKCANCEL | win32con.MB_ICONQUESTION)
            if rv == win32con.IDCANCEL:
                return
        if int(file['size']) > 1024 * 1024 * 5:
            tooltip.show('download start', 'directory=[%s]' % download_filename)
        
        ftp.download(os.path.join(remote_path, filename), os.path.join(download, filename))
        Zip.unzip(filename, unzip_path)
        os.remove(filename)
        tooltip.info('download success', 'directory=[%s]' % download_filename)
    else:
        ToolTipWindow.Error('unknown file type', 'filename=[%s]' % filename)
    

if (__name__ == '__main__'):
    main(sys.argv)
