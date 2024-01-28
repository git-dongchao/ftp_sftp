#!/usr/bin/python
#coding:utf-8

import os
import time
import ctypes
from ftplib import FTP

class FTPConnection(object):
    
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ftp = FTP()
        self.ftp.encoding = "utf-8"
        self.ftp.set_pasv(0)
        
    def connect(self, timeout = 5):
        try:
            self.ftp.connect(self.host, self.port, timeout)
            self.ftp.login(self.username, self.password)
            return True
        except:
            pass
        return False
        
    def close(self):
        self.ftp.close()
        
    def upload(self, remote_path, local_path):
        file = open(local_path, "rb")
        return self.ftp.storbinary("STOR " + remote_path, file)
        
    def download(self, remote_path, local_path):
        file = open(local_path, "wb").write
        return self.ftp.retrbinary("RETR " + remote_path, file)
        
    def mkdir(self, remote_path):
        return self.ftp.mkd(remote_path)
        
    def rmdir(self, remote_path):
        return self.ftp.rmd(remote_path) 
        
    def listdir(self, path):
        files = []
        mlsd = self.ftp.mlsd(path)
        for file in mlsd:
            if file[1]['type'] == 'file':
                files.append({'filename': file[0], 'type': file[1]['type'], 'modify': file[1]['modify'], 'size':file[1]['size']})
        return files
        
    def is_dir_exist(self, remote_path):
        try:
            self.ftp.cwd(remote_path)
            return True
        except:
            pass
        return False
