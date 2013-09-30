import settings
from subprocess import Popen, PIPE
import glob
import socket

#code

ip = []
raid = []
cpu = []
dev = glob.glob('/sys/block/md*')
disks = []
iwriters = ""
irelays = ""
CPUINFO = "/proc/cpuinfo"
flag = "/tmp/standalone"
dests = []
hosts = []
ha_balance = []
me = socket.gethostbyname(socket.getfqdn())

if not settings.HOSTNAMES:
    print "It will be stand alone server! Settings is empty..."
    a = open(flag, "w")
    a.close()
    ip.append("127.0.0.1")
else:
    for h in settings.HOSTNAMES:
        ip.append(socket.gethostbyname(h))

if settings.INTELLECT == 0:
    shard = {'ip': "127.0.0.1", 'writers': settings.WRITERS, 'relays': settings.RELAYS}
    for i in ip:
        shard['ip'] = i
        hosts.append(shard.copy())
else:
    if settings.WRITERS == 'disks':
        for a in dev:
            md = "/dev/" + a.split('/')[3]
            disks = Popen(['mdadm', '-D', md], stdout=PIPE).stdout.readlines()
        for el in disks:
            if "Raid Devices" in el:
                raid.append(el.split(": ")[1])
        iwriters = int(max(raid))
    else:
        iwriters = settings.WRITERS

    if settings.RELAYS == 'cpu':
            with open(CPUINFO) as c:
                content = c.readlines()
                for line in content:
                    if line.startswith("processor"):
                        irelays += 1
    else:
        irelays = settings.RELAYS

    shard = {'ip': "127.0.0.1", 'writers': iwriters, 'relays': irelays}
    for i in ip:
            shard['ip'] = i
            hosts.append(shard.copy())

for h in hosts:
    for i in xrange(1, h['writers']+1, 1):
        dests.append("%s:%d:st%02d" % (h['ip'], 2300 + i, i))

ip_count = len(ip)
for r in range(1, settings.RELAYS + 1, 1):
    for i, el in enumerate(ip):
        ha_balance.append("server relay-%02d %s:%d check port %d inter 5000 rise 3 fall 3" % ((r-1)*ip_count+i+1, el, 4100 + r, 4100 + r))

