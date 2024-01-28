#!/usr/bin/env python
#coding:utf-8

import os
import time
import uuid
import json
import zipfile
import win32gui
import win32con
import win32api
import winreg as reg

def uuid16():
    raw = str(uuid.uuid4())
    uid = ''.join(raw.split('-'))
    return uid[0:3] + uid[8:10] + uid[12:14] + uid[16:18] + uid[:3]

def LoadJson(filepath):
    conf = None
    try:
        with open(filepath,'r', encoding='utf8') as fp:
            try:
                conf = json.load(fp)
            except:
                ToolTipWindow.Error('file parse failed', 'file=[ftp.json]')
                return None
    except:
        ToolTipWindow.Error('file open failed', 'file=[%s]' % filepath)
        return None
    return conf

def hide_console():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
        ctypes.windll.kernel32.CloseHandle(hwnd)

class Zip(object):
    def zip(path, out_path, ext):
        name = os.path.basename(path)
        file = out_path + name + ext
        zf = zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED)
        if os.path.isfile(path):
            zf.write(path, name)
        else:
            for dir_path, dir_names, file_names in os.walk(path):
                fpath = dir_path.replace(path, name)
                fpath = fpath and fpath + os.sep or ''
                for filename in file_names:
                    zf.write(os.path.join(dir_path, filename), os.path.join(fpath, filename))
        zf.close()
        return file

    def unzip(path, out_path):
        zf = zipfile.ZipFile(path, 'r', zipfile.ZIP_DEFLATED)
        for name in zf.namelist():
            target_path = os.path.join(out_path, name)
            if target_path.endswith('/'):
                target = target_path[:-1]
                if not os.path.exists(target):
                    os.makedirs(target)
            else:
                target,_ = os.path.split(target_path)
                if not os.path.exists(target):
                    os.makedirs(target)
                
                file = open(target_path,'wb')
                file.write(zf.read(name))
                file.close()
        #zf.extract(out_path)
        zf.close()


class ToolTipWindow(object):
    def __init__(self):
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "PythonToolTip"
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy, }
        classAtom = win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom, "Taskbar Demo", style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        nid = (self.hwnd, 0, win32gui.NIF_ICON, win32con.WM_USER + 20, hicon, "Demo")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
    
    def show(self, title, msg):
        nid = (self.hwnd,           # 句柄
               0,                   # 托盘图标ID
               win32gui.NIF_INFO,   # 标识
               0,                   # 回调消息ID
               0,                   # 托盘图标句柄
               "",                  # 图标字符串
               msg,                 # 气球提示字符串
               0,                   # 提示的显示时间
               title,               # 提示标题
               win32gui.NIIF_INFO   # 提示用到的图标
               )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
    
    def info(self, title, msg, sleep = 3):
        nid = (self.hwnd,           # 句柄
               0,                   # 托盘图标ID
               win32gui.NIF_INFO,   # 标识
               0,                   # 回调消息ID
               0,                   # 托盘图标句柄
               "",                  # 图标字符串
               msg,                 # 气球提示字符串
               0,                   # 提示的显示时间
               title,               # 提示标题
               win32gui.NIIF_INFO   # 提示用到的图标
               )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
        time.sleep(sleep)
        win32gui.DestroyWindow(self.hwnd)
        
    def error(self, title, msg, sleep = 4):
        nid = (self.hwnd,           # 句柄
               0,                   # 托盘图标ID
               win32gui.NIF_INFO   ,# 标识
               0,                   # 回调消息ID
               0,                   # 托盘图标句柄
               "",                  # 图标字符串
               msg,                 # 气球提示字符串
               0,                   # 提示的显示时间
               title,               # 提示标题
               win32gui.NIIF_ERROR  # 提示用到的图标
               )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
        time.sleep(sleep)
        win32gui.DestroyWindow(self.hwnd)
       
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    @staticmethod
    def Error(title, msg):
        tooltip = ToolTipWindow()
        tooltip.error(title, msg)
        
    @staticmethod
    def Info(title, msg):
        tooltip = ToolTipWindow()
        tooltip.info(title, msg)

def CreateReg(hkey, path, item, sub_item = '', sub_value = ''):
    key = reg.OpenKey(hkey, path)
    reg.SetValue(key, item, reg.REG_SZ, item)
    sub_key = reg.OpenKey(key, item)
    reg.SetValue(sub_key, sub_item, reg.REG_SZ, sub_value)
    reg.CloseKey(sub_key)
    reg.CloseKey(key)
    
def DeleteReg(hkey, path, item, sub_item = ''):
    try:
        key = reg.OpenKey(hkey, path)
        reg.SetValue(key, item, reg.REG_SZ, item)
        sub_key = reg.OpenKey(key, item)
        if sub_item == '':
            reg.DeleteKey(key, item)
        else:
            reg.DeleteKey(sub_key, sub_item)
        reg.CloseKey(sub_key)
        reg.CloseKey(key)
    except:
        return False
    return True

def RegisterSelectMenu(menu_name, menu_command):
    #empty menu
    #CreateReg(reg.HKEY_CLASSES_ROOT, 'Directory\\Background\\shell', menu_name, 'command', menu_command + ' "%V"')
    #director menu
    CreateReg(reg.HKEY_CLASSES_ROOT, 'Folder\\shell', menu_name, 'command', menu_command + ' 2 "%1"')
    #file menu
    CreateReg(reg.HKEY_CLASSES_ROOT, '*\\shell', menu_name, 'command', menu_command + ' 3 "%1"')

def RegisterMenu(menu_name, menu_command):
    #empty menu
    CreateReg(reg.HKEY_CLASSES_ROOT, 'Directory\\Background\\shell', menu_name, 'command', menu_command + ' 1 "%V"')
    #director menu
    CreateReg(reg.HKEY_CLASSES_ROOT, 'Folder\\shell', menu_name, 'command', menu_command + ' 2 "%1"')
    #file menu
    CreateReg(reg.HKEY_CLASSES_ROOT, '*\\shell', menu_name, 'command', menu_command + ' 3 "%1"')

def DeleteMenu(menu_name):
    DeleteReg(reg.HKEY_CLASSES_ROOT, 'Directory\\Background\\shell', menu_name, 'command')
    DeleteReg(reg.HKEY_CLASSES_ROOT, 'Directory\\Background\\shell', menu_name)
    DeleteReg(reg.HKEY_CLASSES_ROOT, 'Folder\\shell', menu_name, 'command')
    DeleteReg(reg.HKEY_CLASSES_ROOT, 'Folder\\shell', menu_name)
    DeleteReg(reg.HKEY_CLASSES_ROOT, '*\\shell', menu_name, 'command')
    DeleteReg(reg.HKEY_CLASSES_ROOT, '*\\shell', menu_name)