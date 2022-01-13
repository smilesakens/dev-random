import os
import shutil
import subprocess
import sys
import time

def bgrnd_cmd(cmdline):
    try:
        proc = subprocess.Popen(cmdline)
    except:
        proc = None
        print('CMD FAILED: {}'.format(cmdline))

    return proc

def exec_cmd(cmdline):
    try:
        result = subprocess.check_output(cmdline)
    except:
        result = 'FAIL'
        print('CMD FAILED: {}'.format(cmdline))

    return result

def change_ip(interface, ipaddr):
    result = exec_cmd('netsh interface ip set address name="{}" static {} 255.255.255.0'.format(interface, ipaddr))

def get_interface():
    result = exec_cmd('netsh interface show interface')
    int_list = result.splitlines()
    int_list = int_list[int_list.index('-'*73) + 1:len(int_list) - 1]
    int_list = int_list.pop(0)
    target_interface = int_list.split('   ').pop()

    return target_interface

if __name__ == '__main__':

    proc_list = []

    target_interface = get_interface()
    change_ip(target_interface, '192.168.1.200')
    time.sleep(600)
    proc_list.append(bgrnd_cmd(['taskmgr']))
    time.sleep(30)
    proc_list.append(bgrnd_cmd(['C:\Program Files (x86)\Notepad++\cmd.exe']))
    time.sleep(120)
    proc_list.append(bgrnd_cmd(['C:\Program Files (x86)\Notepad++\cmd2.exe']))
    change_ip(target_interface, '3.101.55.201')
    time.sleep(60)
    #print(exec_cmd('ipconfig'))
    for proc in proc_list:
        if type(proc) != tuple and proc:
            proc.terminate()
    sys.exit(0)
