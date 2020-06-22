import requests
import re
from ping3 import ping
import multi


def run_core(domain, headers, area):
    # Encrypt!
    if area == "debug":
        iplist = ['220.181.38.148', '39.156.69.79', '210.23.129.34', '210.23.129.34', '220.181.38.148', '39.156.69.79', '202.108.22.220', '220.181.33.31', '112.80.248.64', '14.215.178.80', '180.76.76.92', '210.23.129.34', '210.23.129.34', '39.156.69.79', '220.181.38.148', '203.12.160.35', '203.12.160.35', '39.156.69.79', '220.181.38.148',
                  '202.108.22.220', '220.181.33.31', '112.80.248.64', '14.215.178.80', '180.76.76.92', '203.12.160.35', '203.12.160.35', '220.181.38.148', '39.156.69.79', '61.8.0.113', '61.8.0.113', '220.181.38.148', '39.156.69.79', '202.108.22.220', '220.181.33.31', '112.80.248.64', '14.215.178.80', '180.76.76.92', '61.8.0.113', '61.8.0.113']
    else:
        r = requests.get("https://en.ipip.net/dns.php?a=dig&host=" +
                         domain+"&area%5B%5D="+area, headers=headers)
        iplist = re.findall("\\d+\\.\\d+\\.\\d+\\.\\d+", r.text)
        print("[+]Got domain! \n" + str(iplist))
    return domain, iplist


def ping_host(ip):
    response = ping(ip)
    if response is not None:
        delay = int(response * 1000)
        #print("[+]ping "+str(ip))
        return delay


def clean(iplist):
    # TODO
    ip_dic = multi.multi_ping(iplist)
    print("[+]Start Cleaning...")
    # print(ip_dic)
    ip_dic = sorted(ip_dic.items(), key=lambda kv: (kv[1], kv[0]))
    return(ip_dic)


def output_dic(domain, ip_dic):
    for ip, delay in ip_dic:
        print(str(domain) + "    " + str(ip) + "    " + str(delay))


def test(wtf):
    print(wtf)
