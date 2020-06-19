from ping3 import ping


def ping_host(ip):
    response = ping(ip)
    if response is not None:
        delay = int(response * 1000)
        return delay

def clean(iplist):
    # TODO
    print("[+]Cleaning...")
    ip_dic = dict()
    for ip in iplist:
        ip_dic[ip] = ping_host(ip)
    ip_dic = sorted(ip_dic.items(), key=lambda kv: (kv[1], kv[0]))
    return(ip_dic)

def output_dic(domain, ip_dic):
    for ip, delay in ip_dic:
        print(str(domain) + "    " + str(ip) + "    " + str(delay))


def test(wtf):
    print(wtf)
