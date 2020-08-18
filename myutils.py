import multi
from fake_useragent import UserAgent
import requests
import re
from prettytable import PrettyTable

import os
import sys
import subprocess

global platform
if "linux" in sys.platform:
    from crontab import CronTab
    platform = "linux"
elif "win" in sys.platform:
    platform = "win"


def run_core(domain):
    # Encrypt!
    print("[+]Finding ips local core...")
    print("[+]platform detect: "+platform)
    ipdict = multi.multi_local_dns(domain, platform)
    print("[+]Got domain! \n" + str(list(ipdict[1].keys())))
    return domain, ipdict


def run_remote_core(domain, area):
    print("[+]Finding ips remote core...")
    ua = UserAgent()
    headers = {"User-Agent": ua.random, }
    head = ["http://www.", "https://www."]
    status = []
    for i in head:
        try:
            r = requests.get(i+domain)
            status.append(r.status_code)
        except:
            pass
        continue
    if 200 in status:
        r = requests.get("https://en.ipip.net/dns.php?a=dig&host=" +
                         domain+"&area%5B%5D="+area, headers=headers)
        iplist = re.findall("\\d+\\.\\d+\\.\\d+\\.\\d+", r.text)
        print("[+]Got domain! \n" + str(iplist))
        return domain, iplist
    else:
        raise domainError


def output_dic(domain, ip_dic):
    print("[+]Output:")

    table = PrettyTable(["Domain", "ip", "delay(/s)"])
    table.align["Domain"] = "l"
    for ip, delay in ip_dic.items():
        # print(str(domain) + "    " + str(ip) + "    " + str(delay))
        table.add_row([domain, ip, delay])

    print(table)


def update_hosts(domain, new_ip):
    if os.getuid() != 0:
        print("[-] Not root?")
        return

    if len(new_ip) != 0:
        print("[-]Start updating hosts")
        read_proc = subprocess.Popen(
            ["cat", "/etc/hosts"], stdout=subprocess.PIPE)
        grep_proc = subprocess.Popen(
            ["grep", domain], stdin=read_proc.stdout, stdout=subprocess.PIPE)
        output = grep_proc.communicate()[0].decode()

        if output != '':
            ip = new_ip[0]
            cmd = [
                'sed', '-i', rf'/^[0-9.]\+[[:space:]]\+{domain}\>/s/[^[:space:]]\+/{ip}/', '/etc/hosts']
            try:
                subprocess.check_call(cmd)
                print("Add {0} {1}".format(domain, ip))
            except:
                print("Error: {0} {1}".format(domain, ip))
        else:
            write_str = new_ip[0].ljust(16, ' ') + domain
            cmd = [
                'sed', '-i', rf'/# The following lines are desirable for IPv6 capable hosts/i\{write_str}', '/etc/hosts']

            try:
                subprocess.check_call(cmd)
                print("Add {0} {1}".format(domain, new_ip[0]))
            except:
                print("Error: {0} {1}".format(domain, new_ip[0]))
        print("[+]Done!")


def update_crontab(program_file, domain):
    os.system('service cron start')
    my_user_cron = CronTab(user=True)  # 创建当前用户的crontab
    # 删除原有的crontab文件中重复的内容

    objs = my_user_cron.find_comment(domain)
    if objs:
        for obj in objs:
            my_user_cron.remove(obj)

    job = my_user_cron.new(
        command='python3 ' + program_file + ' -t ' + domain + ' --update')
    job.setall('30 8 * * *')  # 设置执行时间
    job.set_comment(domain)

    my_user_cron.write()


class domainError(Exception):
    def __init__(self, err='invalid domian'):
        Exception.__init__(self, err)
