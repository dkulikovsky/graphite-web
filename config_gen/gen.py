import os
import shutil
import settings
import intellect

dests = []
carbonlink = []
cluster = []

#paths
LOCAL_SETTINGS = "/opt/graphite/webapp/graphite/local_settings.py"
HAPROXY_CONFIG = "/etc/haproxy/haproxy.cfg"
w_dir = '/opt/graphite/conf/carbon-daemons/carbon-writer-st'
r_dir = '/opt/graphite/conf/carbon-daemons/carbon-relay-st'
p = "/opt/graphite/conf/carbon-daemons/"

# LOCAL_SETTINGS = "./local_settings.py"
# HAPROXY_CONFIG = "./haproxy.cfg"
# w_dir = './carbon-writer-st'
# r_dir = './carbon-relay-st'
# p = './'

#text /opt/graphite/bin/templates

local_set = """
REMOTE_FIND_TIMEOUT = 5.0             # Timeout for metric find requests
REMOTE_FETCH_TIMEOUT = 10.0            # Timeout to fetch series data
REMOTE_RETRY_DELAY = 20.0             # Time before retrying a failed remote webapp
REMOTE_READER_CACHE_SIZE_LIMIT = 10000 # Maximum number of remote URL queries to cache
FIND_CACHE_DURATION = 600             # Time to cache remote metric find results
FIND_TOLERANCE = 2 * FIND_CACHE_DURATION

REMOTE_RENDERING = False 
REMOTE_RENDER_CONNECT_TIMEOUT = 1.0

"""

#create dirs & and carbon configs
if settings.INTELLECT == 0:
    for i in range(1, settings.WRITERS + 1, 1):
        if not os.path.exists(os.path.join(p, "carbon-writer-st%02d" % i)):
            os.mkdir(os.path.join(p, "carbon-writer-st%02d" % i))
        shutil.copy("/opt/graphite/bin/template/writer.conf", os.path.join(p, "carbon-writer-st%02d" % i))
        w = open(os.path.join(p, "carbon-writer-st%02d" % i + "/writer.conf"), "a")
        w.write("%s%02d" % ("CACHE_QUERY_PORT = ", 2500 + i))
        w.close()
        shutil.copy("/opt/graphite/bin/template/daemon.conf", os.path.join(p, "carbon-writer-st%02d" % i))
        d = open(os.path.join(p, "carbon-writer-st%02d" % i + "/daemon.conf"), "a")
        d.write("PIPELINE = write")
        d.close()
        shutil.copy("/opt/graphite/bin/template/db.conf", os.path.join(p, "carbon-writer-st%02d" % i))
        shutil.copy("/opt/graphite/bin/template/storage-rules.conf", os.path.join(p, "carbon-writer-st%02d" % i))
        shutil.copy("/opt/graphite/bin/template/listeners.conf", os.path.join(p, "carbon-writer-st%02d" % i))
        l = open(os.path.join(p, "carbon-writer-st%02d" % i + "/listeners.conf"), "a")
        l.write("%s%02d" % ("port = ", 2300 + i))
        l.close()
    for i in range(1, settings.RELAYS + 1, 1):
        if not os.path.exists(os.path.join(p, "carbon-relay-st%02d" % i)):
            os.mkdir(os.path.join(p, "carbon-relay-st%02d" % i))
        shutil.copy("/opt/graphite/bin/template/relay.conf", os.path.join(p, "carbon-relay-st%02d" % i))
        r = open(os.path.join(p, "carbon-relay-st%02d" % i + "/relay.conf"), "a")
        r.write("DESTINATIONS = " + ", ".join(intellect.dests))
        r.close()
        shutil.copy("/opt/graphite/bin/template/daemon.conf", os.path.join(p, "carbon-relay-st%02d" % i))
        d = open(os.path.join(p, "carbon-relay-st%02d" % i + "/daemon.conf"), "a")
        d.write("PIPELINE = relay")
        d.close()
        shutil.copy("/opt/graphite/bin/template/listeners.conf", os.path.join(p, "carbon-relay-st%02d" % i))
        l = open(os.path.join(p, "carbon-relay-st%02d" % i + "/listeners.conf"), "a")
        l.write("%s%02d" % ("port = ", 4300 + i))
        l.write("\n[plaintext-receiver]\ntype = plaintext-receiver %s%02d" % ("\nport = ", 4100 + i))
        l.close()
        shutil.copy("/opt/graphite/bin/template/db.conf", os.path.join(p, "carbon-relay-st%02d" % i))
else:
    print "Don't do this!"

for i in range(1, settings.WRITERS + 1, 1):
    for j, el in enumerate(intellect.ip):
        carbonlink.append("%s:%d:st%02d" % (el, 2500 + i, i))

shutil.copy("/opt/graphite/bin/template/local_settings.py", "/opt/graphite/webapp/graphite/")
s = open(LOCAL_SETTINGS, "a")
s.write("CARBONLINK_HOSTS = " + str(carbonlink) + "\nCLUSTER_SERVERS = " + str(intellect.ip) + local_set + "RENDERING_HOSTS = " + str(intellect.ip))
s.close()


hp = "\n\t".join(intellect.ha_balance)
h = open(HAPROXY_CONFIG, 'w')
h.write("listen graphite-relay 0.0.0.0:2024\n\tbalance roundrobin\n\t" + hp + "\nlog 127.0.0.1 local7 notice")
h.close()

dh = open('/etc/default/haproxy', "w")
# dh = open('./haproxy', "w")
dh.write("ENABLED=1")
dh.close()
