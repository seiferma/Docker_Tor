#!/bin/sh

# Create tor user account
TOR_USER_NAME=tor-dckr
TOR_GROUP_NAME=tor-dckr
getent passwd $TOR_USER_NAME > /dev/null
if [ $? -ne 0 ]; then
	echo "Generating user account for tor"
	if [ "$TOR_GID" == "" ]; then
		export TOR_GID=1500
	fi
	if [ "$TOR_UID" == "" ]; then
		export TOR_UID=1500
	fi
	addgroup -g $TOR_GID $TOR_GROUP_NAME
	adduser -D -H -G $TOR_GROUP_NAME -u $TOR_UID $TOR_USER_NAME
	mkdir /home/$TOR_USER_NAME/
	chown $TOR_USER_NAME:$TOR_GROUP_NAME /home/$TOR_USER_NAME/
fi

# Run tor under user "tor"
su-exec $TOR_USER_NAME tor "$@"
