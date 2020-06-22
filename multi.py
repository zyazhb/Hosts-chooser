#!/usr/bin/python
# _*_coding:utf-8_*_
#
from threading import Thread, Lock
from ping3 import ping
import time
ip_dic = dict()

class PING(Thread):
    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip

    def run(self):
        response = ping(self.ip)
        if response is not None:
            delay = int(response * 1000)
            #print("[+]ping "+str(self.ip))
            ip_dic[self.ip] = delay


def multi_ping(iplist):
    T_thread = []
    for i in iplist:
        T_thread.append(PING(i))
    for i in range(len(T_thread)):
        T_thread[i].start()
    time.sleep(3)
    return ip_dic
