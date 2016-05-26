#! /bin/sh
### BEGIN INIT INFO
# Provides:          tox-bootstrapd
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Starts the Tox DHT bootstrapping server daemon
# Description:       Starts the Tox DHT bootstrapping server daemon
### END INIT INFO

NAME=tox-bootstrapd
DAEMON=/usr/bin/$NAME
CFGFILE=/etc/$NAME.conf
DAEMON_ARGS="--config $CFGFILE"
PIDDIR=/var/run/$NAME
PIDFILE=$PIDDIR/$NAME.pid
USER=tox-bootstrapd
GROUP=tox-bootstrapd

# Source function library
. /etc/rc.d/init.d/functions

RETVAL=0

start()
{
	[ $UID -eq 0 ] || exit 4
	[ -x $DAEMON ] || exit 5
	[ -f $CFGFILE ] || exit 6
	echo -n $"Starting $NAME: "
	if [ ! -d $PIDDIR ]
	then
		mkdir $PIDDIR
	fi
	chown $USER:$GROUP $PIDDIR
	daemon --user $USER $DAEMON $DAEMON_ARGS
	RETVAL=$?
	echo
	[ $RETVAL = 0 ] && touch $PIDFILE
	return $RETVAL
}

stop()
{
	[ $UID -eq 0 ] || exit 4
	echo -n $"Shutting down $NAME: "
	killproc -p $PIDFILE $DAEMON
	RETVAL=$?
	echo
	rm -f $PIDFILE
	return $RETVAL
}

case "$1" in
	start)
		start
	;;
	stop)
		stop
	;;
	restart)
		stop
		start
	;;
	status)
		status -p $PIDFILE $NAME
		RETVAL=$?
	;;
	*)
		echo $"Usage: $0 {start|stop|restart|status}"
		RETVAL=2
		[ "$1" = 'usage' ] && RETVAL=0
	;;
esac

exit $RETVAL
