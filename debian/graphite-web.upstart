#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
GRAPHITE_ROOT="/opt/graphite"
GRAPHITE_MANAGE_SCRIPT="$GRAPHITE_ROOT/webapp/graphite/manage.py"
DAEMON="/usr/bin/python"
PID_FILE="/var/run/graphite.pid"
DARGS="$GRAPHITE_MANAGE_SCRIPT runfcgi method=prefork host=127.0.0.1 port=6031 pidfile=$PID_FILE workdir=$GRAPHITE_ROOT/webapp outlog=/var/log/graphite_out.log errlog=/var/log/graphite_err.log maxrequests=0 maxchildren=24 minspare=24 maxspare=24"
NAME=graphite-web
DESC="graphite web interface"


test -e $GRAPHITE_MANAGE_SCRIPT || exit 0

set -e

case "$1" in
  start)
	echo -n "Starting $DESC: "
	start-stop-daemon --start -u www-data --pidfile $PID_FILE --exec $DAEMON -- $DARGS
	echo "$NAME."
	;;
  stop)
	echo -n "Stopping $DESC: "
	start-stop-daemon --stop --quiet --pidfile $PID_FILE --retry 2 --oknodo --exec $DAEMON -- $DARGS
	echo "$NAME."
	;;
  #reload)
  restart|force-reload)
	#
	#	If the "reload" option is implemented, move the "force-reload"
	#	option to the "reload" entry above. If not, "force-reload" is
	#	just the same as "restart".
	#
	echo -n "Restarting $DESC: "
	start-stop-daemon --stop --quiet --pidfile $PID_FILE --retry 2 --oknodo --exec $DAEMON -- $DARGS
	sleep 1
	start-stop-daemon --start -u www-data --pidfile $PID_FILE --exec $DAEMON -- $DARGS
	echo "$NAME."
	;;
  *)
	N=/etc/init.d/$NAME
	# echo "Usage: $N {start|stop|restart|reload|force-reload}" >&2
	echo "Usage: $N {start|stop|restart|force-reload}" >&2
	exit 1
	;;
esac

exit 0
