#! /usr/bin/env python3
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
    headers = init()
    parser, args = initArguments()
    if args.target:
        domain, iplist = myutils.run_core(args.target, headers, args.area)
    elif args.r:
        for domain in open(args.r):
            domain, iplist = myutils.run_core(domain, headers, args.area)
    else:
        parser.print_help()

    if args.clean:
        #myutils.thread_work(args.thread, myutils.clean, iplist)
        myutils.output_dic(domain, myutils.clean(iplist))


if __name__ == "__main__":
    main()
