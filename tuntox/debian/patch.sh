#!/bin/sh

set -e

for PATCH in $(cat debian/patches/series)
do
	patch -p0 < debian/patches/${PATCH}
done
