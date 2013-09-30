#allow to set number of writers by count of disks and number of relays by count of CPUs
#DON'T USE INTELLECT IF YOU HAVE SERVERS WITH DIFFERENT NUMBER OF CPU AND DISKS!
INTELLECT = 0
#hostnames of shards
HOSTNAMES = []
#count of writers. may be number or 'disk'. works only with software raid and only if intellect != 0
WRITERS = 24
#count of relays. May be number or 'cpu'. works only if intellect != 0
RELAYS = 24

