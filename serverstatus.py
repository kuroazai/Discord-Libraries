# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 18:44:49 2020

@author: Odin
"""
import subprocess
import os
import psutil


def server_status():
    # yes mate
    if "FXServer.exe" in (p.name() for p in psutil.process_iter()):
        return True
    else:
        return False


def server_start():
    # yes mate
    if "FXServer.exe" in (p.name() for p in psutil.process_iter()):
        return 'Server is already running... '
    else:
        os.chdir('C:\FXServer\server-data')
        os.system('start cmd.exe @cmd /c "C:\FXServer\server\start_server.bat"')
        return 'Server Start... '


def server_restart():
    # close server
    os.system("taskkill /f /im FXServer.exe /T")
    os.chdir('C:\FXServer\server-data')
    os.system('start cmd.exe @cmd /c "C:\FXServer\server\start_server.bat"')
    return 'Server Restarting... '


def server_stop():
    os.system("taskkill /f /im FXServer.exe /T")
    return 'Server stopping... '
