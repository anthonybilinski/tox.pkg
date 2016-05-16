#! /bin/sh
### BEGIN INIT INFO
# Provides:          tuntoxd
# Required-Start:    $network $syslog
# Required-Stop:     $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Starts the tuntox server daemon
# Description:       Starts the tuntox server daemon
### END INIT INFO

NAME=tuntoxd
DAEMON=/usr/bin/$NAME
PIDDIR=/var/run/$NAME
PIDFILE=$PIDDIR/$NAME.pid
USER=tuntoxd
GROUP=tuntoxd
PASSWORD=P@ssw0rd
SAVEDIR=/var/lib/$NAME
LOGLEVEL=""

# Exit if the package is not installed
[ -x $DAEMON ] || exit 0

# source dynamic variables
[ -f /etc/default/$NAME ] && . /etc/default/$NAME
[ -f /etc/sysconfig/$NAME ] && . /etc/sysconfig/$NAME

DAEMON_ARGS="-D -S $LOGLEVEL -C $SAVEDIR -F $PIDFILE -U $USER -s $PASSWORD"

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
