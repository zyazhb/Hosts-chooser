import requests
import re
from fake_useragent import UserAgent
import argparse
import myutils


def init():
    ua = UserAgent()
    headers = {"User-Agent": ua.random, }
    return headers


def initArguments():
    parser = argparse.ArgumentParser(
        description="Prevent domains from dns polution.")
    parser.add_argument("-t", help="Your target domain", type=str)
    parser.add_argument("-r", help="Read a domain list", type=str)
    parser.add_argument(
        "--clean", help="Speed test and sort", action="store_true")
    parser.add_argument("--area", help="Choose area in china asia europe africa oceania north_america south_america",
                        choices=["china", "asia", "europe", "africa", "oceania", "north_america", "south_america", "debug"], type=str, default="north_america", nargs='?')
    args = parser.parse_args()
    return args


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


def main():
    headers = init()
    args = initArguments()
    if args.t:
        domain, iplist = run_core(args.t, headers, args.area)
    elif args.r:
        for domain in open(args.r):
            domain, iplist = run_core(domain, headers, args.area)
    else:
        iplist = ""

    if args.clean:
        myutils.output_dic(domain, myutils.clean(iplist))
    else:
        print(iplist)


if __name__ == "__main__":
    main()
