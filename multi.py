#!/usr/bin/python
# _*_coding:utf-8_*_
#
from threading import Thread
import subprocess
from ping3 import ping
import time
import re
import sys

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
    time.sleep(5)
    return ip_dic


iplist = []

class DIG(Thread):
    def __init__(self, ip, domain):
        Thread.__init__(self)
        self.ip = ip
        self.domain = domain

    def run(self):
        runtimePlatform = sys.platform

        # response = subprocess.check_output(
        #     "dig @{0} {1} +short".format(self.ip, self.domain), shell=True)
        if runtimePlatform == "linux":
            proc = subprocess.Popen(
                "dig @{0} {1} +short".format(self.ip, self.domain), shell=True, close_fds=True, stdout=subprocess.PIPE)
        else:
            proc = subprocess.Popen(
                "nslookup {0} {1}".format(self.domain, self.ip), shell=True, stdout=subprocess.PIPE)

        # time.sleep(1.5)
        response = proc.stdout.read()
        proc.kill()

        if runtimePlatform == "linux":
            if ";; connection timed out; no servers could be reached" not in response.decode():
                ans = re.findall("\\d+\\.\\d+\\.\\d+\\.\\d+", str(response.decode()))
                if ans != []:
                    iplist.extend(ans)
        else:
            # TODO 完善输出机制
            ans = re.findall("\\d+\\.\\d+\\.\\d+\\.\\d+", str(response))
            if ans != []:
                iplist.extend(ans[1:])

def multi_local_dns(domain):
    with open("dns.txt", "r") as f_dns:
        iplist_unsolve = [x.replace('\n', '') for x in f_dns.readlines()]

        # 多线程dig
        T_thread = []
        for i in iplist_unsolve:
            T_thread.append(DIG(i, domain=domain))
        for i in range(len(T_thread)):
            T_thread[i].start()
        time.sleep(15)

        # 去重
        iplist_change = list(set(iplist))
        print("[+]Got domain! \n" + str(iplist_change))
    return domain, iplist_change
