#! /usr/bin/env python3
from fake_useragent import UserAgent
import argparse
import myutils
import requests


def init():
    ua = UserAgent()
    headers = {"User-Agent": ua.random, }
    return headers


def initArguments():
    parser = argparse.ArgumentParser(
        description="Prevent domains from dns polution.")
    parser.add_argument("-t", "--target", help="Your target domain", type=str)
    parser.add_argument("-r", help="Read a domain list", type=str)
    parser.add_argument(
        "--clean", help="Speed test and sort", action="store_true")
    parser.add_argument("--area", help="Choose area in china asia europe africa oceania north_america south_america",
                        choices=["china", "asia", "europe", "africa", "oceania", "north_america", "south_america", "debug"], type=str, default="north_america", nargs='?')
    parser.add_argument(
        "--thread", help="Run num of threads,default is 3", type=int, default=3)
    args = parser.parse_args()
    return parser, args

def main():
    headers = init()#随机生成useragent
    parser, args = initArguments()#生成提示信息

    try:
        if args.target:
            domain,iplist = myutils.run_core(args.target, headers, args.area)
            checkdomain(domain)
        elif args.r:
            for domain in open(args.r):
                domain, iplist = myutils.run_core(domain, headers, args.area)
        else:
            raise ValueError

        if args.clean:
            #myutils.thread_work(args.thread, myutils.clean, iplist)
            myutils.output_dic(domain, myutils.clean(iplist))
    except requests.exceptions.MissingSchema:
        print("The domain was not found")
    except ValueError:
        print("pleas enter vaild paras or add -h/--help to view help information")

def checkdomain(domain):
    url=domain
    res=requests.get(url)
    if res.status_code!=200:
        raise requests.exceptions.MissingSchema

if __name__ == "__main__":
    main()
