#!/bin/sh

PKGNAME="$1"
PKGDIR="$2"

cd img/icons

for SIZE in $(find . -mindepth 1 -type d | sed -e 's|^./||g')
do
    install -d "${PKGDIR}/usr/share/icons/hicolor/${SIZE}/apps"
    install -m644 "${SIZE}/${PKGNAME}.png" "${PKGDIR}/usr/share/icons/hicolor/${SIZE}/apps/${PKGNAME}.png"
done

install -d "${PKGDIR}/usr/share/icons/hicolor/scalable/apps"
install -m644 "${PKGNAME}.svg" "${PKGDIR}/usr/share/icons/hicolor/scalable/apps/${PKGNAME}.svg"
