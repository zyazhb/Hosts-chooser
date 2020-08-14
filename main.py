#! /usr/bin/env python3
import argparse
import myutils

import sys


def initArguments():
    parser = argparse.ArgumentParser(
        description="Prevent domains from dns polution.")
    parser.add_argument("-t", "--target", help="Your target domain", type=str)
    parser.add_argument("-r", help="Read a domain list", type=str)
    parser.add_argument(
        "--clean", help="Speed test and sort", action="store_true")
    parser.add_argument("--area", help="Choose area in china asia europe africa oceania north_america south_america",
                        choices=["china", "asia", "europe", "africa", "oceania", "north_america", "south_america", "debug"], type=str, nargs='?')
    parser.add_argument(
        "--update", help="Auto update hosts", action="store_true")
    args = parser.parse_args()
    return parser, args


def main():
    parser, args = initArguments()
    if args.target:
        if args.area:
            domain, ipdict = myutils.run_remote_core(args.target, args.area)
        else:
            domain, ipdict = myutils.run_core(args.target)
    elif args.r:
        for domain in open(args.r):
            domain, ipdict = myutils.run_core(domain, args.area)
    else:
        domain = None
        parser.print_help()

    if args.clean and domain:
        myutils.output_dic(domain, ipdict[1])

    if args.update and domain and ('win' not in sys.platform):
        myutils.update_hosts(domain, tuple(ipdict[1].keys()))
        myutils.update_crontab(domain)


if __name__ == "__main__":
    main()
