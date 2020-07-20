import asyncio
import aiohttp
import uvloop

import time
import subprocess
import re


class MyConnector(aiohttp.TCPConnector):
    def __init__(self, ip):
        self.__ip = ip
        super().__init__()

    async def _resolve_host(
        self, host: str, port: int,
        traces: None = None,
    ):
        return [{
            'hostname': host, 'host': self.__ip, 'port': port,
            'family': self._family, 'proto': 0, 'flags': 0,
        }]


def now(): return time.time()


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
    try:
        async with aiohttp.ClientSession(connector=MyConnector(ip), timeout=aiohttp.ClientTimeout(total=10)) as client:
            async with client.get("https://{0}".format(ip), ssl=False, timeout=10) as resp:
                if resp.status == 200:
                    time_list[ip] = now() - st
    except asyncio.TimeoutError:
        pass

async def dns_test(domain):
    task_list = [asyncio.create_task(
        run('dig @{0} {1} +short'.format(dns, domain))) for dns in dns_list]
    done, pending = await asyncio.wait(task_list, timeout=5)

    task_speed = [asyncio.create_task(test_doamin_ip(ip))
                  for ip in set(ip_list)]
    done, pending = await asyncio.wait(task_speed)

def multi_local_dns(domain):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    start = now()
    asyncio.run(dns_test(domain))
    print("Time: ", now() - start)
    return domain, time_list
