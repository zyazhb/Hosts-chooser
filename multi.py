import asyncio
import aiohttp

import time
import subprocess
import re
import gc


now = lambda : time.time()


with open("dns.txt") as f:
    a = f.readlines()
dns_list = [i.strip() for i in a]

ip_list = []
time_list = {}


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        ip_find = re.findall("\\d+\\.\\d+\\.\\d+\\.\\d+", stdout.decode())
        ip_list.extend(ip_find)
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')


async def test_doamin_ip(ip):
    st = now()
    async with aiohttp.ClientSession() as client:
        async with client.get("https://{0}".format(ip), ssl=False, timeout=59) as resp:
            if resp.status == 200:
                time_list[ip] = now() - st


async def dns_test(domain):
    task_list = [asyncio.create_task(
        run('dig @{0} {1} +short'.format(dns, domain))) for dns in dns_list]
    done, pending = await asyncio.wait(task_list, timeout=5)

    task_speed = [asyncio.create_task(test_doamin_ip(ip))
                  for ip in set(ip_list)]
    done, pending = await asyncio.wait(task_speed)


def multi_local_dns(domain):
    asyncio.run(dns_test(domain))
    return domain, time_list
