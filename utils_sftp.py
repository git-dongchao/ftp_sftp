#coding:utf-8

import time
import stat
import shutil
import paramiko

class SFTPConnection(object):

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self, timeout = 5):
        try:
            self.conn = paramiko.Transport((self.host, self.port))
            self.conn.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.conn, 1073741824, 1073741824)
            return True
        except:
            pass
        return False

    def close(self):
        self.transport.close()
        
    def upload(self, remote_path, local_path):
        return self.sftp.put(local_path, remote_path)
        
    def download(self, remote_path, local_path):
        with self.sftp.open(remote_path, 'rb') as fp:
            shutil.copyfileobj(fp, open(local_path, 'wb'))

    def mkdir(self, remote_path):
        return self.sftp.mkdir(remote_path)
        
    def rmdir(self, remote_path):
        return self.sftp.rmdir(remote_path) 
        
    def listdir(self, path):
        files = []
        dir_attrs = self.sftp.listdir_attr(path)
        for dir_attr in dir_attrs:
            if stat.S_ISDIR(dir_attr.st_mode) == False:
                files.append({'filename': dir_attr.filename, 'modify': dir_attr.st_mtime, 'size': dir_attr.st_size})
        return files
        
    def is_dir_exist(self, remote_path):
        try:
            self.sftp.chdir(remote_path)
            return True
        except:
            pass
        return False
