'''
防止dns污染自动匹配被DNS污染但是ip没有被屏蔽的网站
'''
import requests
import re
from fake_useragent import UserAgent
import argparse
from ping3 import ping


def init():
    ua = UserAgent()
    headers = {"User-Agent": ua.random, }
    return headers


def initArguments():
    parser = argparse.ArgumentParser(
        description="Prevent domains from dns polution.")
    parser.add_argument("-t", help="Your target domain", type=str)
    parser.add_argument("-r", help="Read a domain list", type=str)
    parser.add_argument("--clean", help="Speed test", action="store_true")
    parser.add_argument("--area", help="Choose area in china asia europe africa oceania north_america south_america",
                        choices=["china", "asia", "europe", "africa", "oceania", "north_america", "south_america"])
    args = parser.parse_args()
    return args


def run(domain, headers, area):
    # Encrypt!
    '''
    r = requests.get("https://en.ipip.net/dns.php?a=dig&host=" +
                     domain+"&area%5B%5D="+area, headers=headers)
    iplist = re.findall("\\d+\\.\\d+\\.\\d+\\.\\d+", r.text)
    '''
    iplist = ['220.181.38.148', '39.156.69.79', '210.23.129.34', '210.23.129.34', '220.181.38.148', '39.156.69.79', '202.108.22.220', '220.181.33.31', '112.80.248.64', '14.215.178.80', '180.76.76.92', '210.23.129.34', '210.23.129.34', '39.156.69.79', '220.181.38.148', '203.12.160.35', '203.12.160.35', '39.156.69.79', '220.181.38.148',
              '202.108.22.220', '220.181.33.31', '112.80.248.64', '14.215.178.80', '180.76.76.92', '203.12.160.35', '203.12.160.35', '220.181.38.148', '39.156.69.79', '61.8.0.113', '61.8.0.113', '220.181.38.148', '39.156.69.79', '202.108.22.220', '220.181.33.31', '112.80.248.64', '14.215.178.80', '180.76.76.92', '61.8.0.113', '61.8.0.113']
    return domain, iplist


def ping_host(ip):
    response = ping(ip)
    if response is not None:
        delay = int(response * 1000)
        return delay


def clean(iplist):
    # TODO
    ip_dic = dict()
    for ip in iplist:
        ip_dic[ip] = ping_host(ip)
    ip_dic = sorted(ip_dic.items(), key=lambda kv: (kv[1], kv[0]))
    return(ip_dic)


def output_dic(domain, ip_dic):
    for ip, delay in ip_dic:
        print(str(domain) + "    " + str(ip) + "    " + str(delay))


def main():
    headers = init()
    args = initArguments()
    if args.t:
        domain, iplist = run(args.t, headers, args.area)
    elif args.r:
        for domain in open(args.r):
            domain, iplist = run(domain, headers, args.area)
    else:
        iplist = ""

    if args.clean:
        output_dic(domain, clean(iplist))
    else:
        print(iplist)


if __name__ == "__main__":
    main()
