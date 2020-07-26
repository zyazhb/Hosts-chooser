#! /usr/bin/env python3
import argparse
import myutils

def initArguments():
    parser = argparse.ArgumentParser(
        description="Prevent domains from dns polution.")
    parser.add_argument("-t", "--target", help="Your target domain", type=str)
    parser.add_argument("-l", "--local", help="Use local api to find ip", action="store_true")
    parser.add_argument("-r", help="Read a domain list", type=str)
    parser.add_argument(
        "--clean", help="Speed test and sort", action="store_true")
    parser.add_argument("--area", help="Choose area in china asia europe africa oceania north_america south_america",
                        choices=["china", "asia", "europe", "africa", "oceania", "north_america", "south_america", "debug"], type=str, default="north_america", nargs='?')
    args = parser.parse_args()
    return parser, args


def main():
    parser, args = initArguments()
    try:
        if args.target:
            if args.local:
                domain, iplist = myutils.run_core(args.target, args.area)
            else:
                domain, iplist = myutils.run_remote_core(args.target, args.area)
        elif args.r:
            if args.local:
                for domain in open(args.r):
                    domain, iplist = myutils.run_core(domain, args.area)
            else:
                for domain in open(args.r):
                    domain, iplist = myutils.run_remote_core(domain, args.area)
        else:
            parser.print_help()
        if args.clean:
            myutils.output_dic(domain, myutils.clean(iplist))
    except myutils.domainError:
        print('''The domain you entered is invalid,
The right example: python main.py -t github.com
        ''')
    if args.clean:
        myutils.output_dic(domain, ipdict[1])

if __name__ == "__main__":
    main()
