#!/usr/bin/python
# _*_coding:utf-8_*_
#
from threading import Thread
from ping3 import ping
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
# 多线程同时执行


def multi_ping(iplist):
    T_thread = []
    for i in iplist:
        t = PING(i)
        T_thread.append(t)
    for i in range(len(T_thread)):
        T_thread[i].start()
    return ip_dic
