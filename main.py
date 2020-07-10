#! /usr/bin/env python3
import argparse
import myutils
from threading import Thread, Lock
import time

def initArguments():
    parser = argparse.ArgumentParser(
        description="Prevent domains from dns polution.")
    parser.add_argument("-t", "--target", help="Your target domain", type=str)
    parser.add_argument("-r", "--read", help="Read a domain list,take each domain in each lines(use your Enter)", type=str)
    parser.add_argument(
        "--clean", help="Speed test and sort", action="store_true")
    parser.add_argument("--area", help="Choose area in china asia europe africa oceania north_america south_america",
                        choices=["china", "asia", "europe", "africa", "oceania", "north_america", "south_america", "debug"], type=str, default="north_america", nargs='?')
    parser.add_argument(
        "--thread", help="Run num of threads,default is 3", type=int, default=3)
    args = parser.parse_args()
    return parser, args


def main():
    parser, args = initArguments()
    if args.target:
        print('开始查找', args.target, args.area)
        domain, iplist = myutils.run_core(args.target, args.area)
    elif args.read:
        name = args.read
        f = open('./' + name, 'r')
        iplist = []
        for i in f.readlines():
            line = i.strip()
            domain = line
            t = Thread_read(line)
            t.start()
            time.sleep(5)                      
    else:
        parser.print_help()

    if args.clean and args.read == False:
        myutils.output_dic(domain, myutils.clean(iplist))


class Thread_read(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        parser, args = initArguments()
        print('开始查找', self.name, args.area, time.ctime(time.time()))  
        Domain = self.name
        # print(Domain, args.area)
        lock=Lock()
        lock.acquire()  #加锁
        domain, iplist = myutils.run_core(Domain, args.area)
        lock.release() #释放锁
        if args.clean:
            myutils.output_dic(domain, myutils.clean(iplist))
        print('结束查找', self.name, args.area, time.ctime(time.time()))
        print(domain, iplist)


if __name__ == "__main__":
    main()
