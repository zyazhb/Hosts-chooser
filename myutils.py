import subprocess
import time
import requests
import re
from ping3 import ping
import multi
from prettytable import PrettyTable
from threading import Thread, Lock

ipll = []
class DIG(Thread):
    def __init__(self, ip, domain):
        Thread.__init__(self)
        self.ip = ip
        self.domain = domain

    def run(self):
        response = subprocess.check_output("dig @{0} {1}".format(self.ip, self.domain), shell=True)
        if r";; connection timed out; no servers could be reached" not in str(response):
            ipll.append(self.ip)
            

def run_core(domain, area):
    # Encrypt!
    if area == "debug":
        iplist = ['220.181.38.148', '39.156.69.79', '210.23.129.34', '210.23.129.34', '220.181.38.148', '39.156.69.79', '202.108.22.220', '220.181.33.31', '112.80.248.64', '14.215.178.80', '180.76.76.92', '210.23.129.34', '210.23.129.34', '39.156.69.79', '220.181.38.148', '203.12.160.35', '203.12.160.35', '39.156.69.79', '220.181.38.148',
                  '202.108.22.220', '220.181.33.31', '112.80.248.64', '14.215.178.80', '180.76.76.92', '203.12.160.35', '203.12.160.35', '220.181.38.148', '39.156.69.79', '61.8.0.113', '61.8.0.113', '220.181.38.148', '39.156.69.79', '202.108.22.220', '220.181.33.31', '112.80.248.64', '14.215.178.80', '180.76.76.92', '61.8.0.113', '61.8.0.113']
    else:
        with open("dns.txt", "r") as f_dns:
            iplist_unsolve = [x.replace('\n', '') for x in f_dns.readlines() ]

        # 多线程dig
        T_thread = []
        for i in iplist_unsolve:
            T_thread.append(DIG(i, domain=domain))
        for i in range(len(T_thread)):
            T_thread[i].start()
        time.sleep(3)

        print("[+]Got domain! \n" + str(ipll))
    return domain, ipll


def clean(iplist):
    print("[+]Start Cleaning...")
    ip_dic = multi.multi_ping(iplist)
    ip_dic = sorted(ip_dic.items(), key=lambda kv: (kv[1], kv[0]))
    return(ip_dic)


def output_dic(domain, ip_dic):
    print("[+]Output:")

    table = PrettyTable(["Domain", "ip", "delay"])
    table.align["Domain"] = "l"
    for ip, delay in ip_dic:
        # print(str(domain) + "    " + str(ip) + "    " + str(delay))
        table.add_row([domain, ip, delay])

    print(table)
