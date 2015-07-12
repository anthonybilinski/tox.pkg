#!/bin/sh

PKGNAME="$1"
PKGDIR="$2"

cd img/icons

for ICON in *.png
do
    SIZE=$(echo "${ICON}" | sed 's|^[^-]*-||;s|\.png||')
    install -d "${PKGDIR}/usr/share/icons/hicolor/${SIZE}/apps"
    install -m644 "${ICON}" "${PKGDIR}/usr/share/icons/hicolor/${SIZE}/apps/${PKGNAME}.png"
done

install -d "${PKGDIR}/usr/share/icons/hicolor/scalable/apps"
install -m644 ${PKGNAME}.svg "${PKGDIR}/usr/share/icons/hicolor/scalable/apps/${PKGNAME}.svg"
