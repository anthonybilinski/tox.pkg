#!/bin/sh

set -e

GIT_REV="f790747f2adda60f8809bb0e1671f18c3f7c6168"
PACKAGE_NAME="qtox-alpha"
PACKAGE_DATE=$(LC_ALL=C date "+%a, %d %b %Y %H:%M:%S %z")
PACKAGE_VERSION=$(date "+%Y%m%d%H%M")
SPEC_DATE=$(LC_ALL=C date '+%a %b %d %Y')

BASE=`dirname $0`
cd "${BASE}"
BASE=$(pwd)

BUILD_DIR="${BASE}/../build/${PACKAGE_NAME}"
SOURCE_DIR="${BUILD_DIR}/${PACKAGE_NAME}"

mkdir -p "${BUILD_DIR}"

if [ ! -d "${SOURCE_DIR}/.git" ]; then
	rm -rf "${SOURCE_DIR}"
	git clone --recursive https://github.com/qTox/qTox.git "${SOURCE_DIR}"
fi

rm -rf "${SOURCE_DIR}/debian"

rm -f "${BUILD_DIR}/PKGBUILD"
rm -f "${BUILD_DIR}/${PACKAGE_NAME}.spec"
rm -f "${BUILD_DIR}/${PACKAGE_NAME}_"*.dsc
rm -f "${BUILD_DIR}/${PACKAGE_NAME}_"*.tar.bz2
rm -f "${BUILD_DIR}/${PACKAGE_NAME}_"*.changes
rm -f "${BUILD_DIR}/${PACKAGE_NAME}_"*.build

cp -rf "${BASE}/debian" "${SOURCE_DIR}/debian"

cd "${SOURCE_DIR}"

git checkout "${GIT_REV}"

"${BASE}/update-nodelist.py" > "${SOURCE_DIR}/res/settings.ini"

PACKAGE_REVISION=$(git rev-parse HEAD)
PACKAGE_REVISION_SHORT=$(expr substr "${PACKAGE_REVISION}" 1 7)
PACKAGE_VERSION="${PACKAGE_VERSION}~${PACKAGE_REVISION_SHORT}"

sed -i -r -e "s|GIT_VERSION = (.*)|GIT_VERSION = ${PACKAGE_REVISION}|g" "qtox.pro"
sed -i -r -e "s|GIT_DESCRIBE = (.*)|GIT_DESCRIBE = `git describe --always --tags`-obs|g" "qtox.pro"

sed -i -e "s/%PACKAGE%/${PACKAGE_NAME}/g"      "debian/changelog"
sed -i -e "s/%DATE%/${PACKAGE_DATE}/g"         "debian/changelog"
sed -i -e "s/%VERSION%/${PACKAGE_VERSION}/g"   "debian/changelog"
sed -i -e "s/%REVISION%/${PACKAGE_REVISION}/g" "debian/changelog"

debuild -S

SHA_512=$(openssl sha512 "${BUILD_DIR}/${PACKAGE_NAME}_${PACKAGE_VERSION}.tar.bz2" | awk '{ print $NF; }')

sed -e "s/%PACKAGE%/${PACKAGE_NAME}/g" "${BASE}/spec.template" | \
sed -e "s/%DATE%/${SPEC_DATE}/g"                               | \
sed -e "s/%VERSION%/${PACKAGE_VERSION}/g"                        \
> "${BUILD_DIR}/${PACKAGE_NAME}.spec"

sed -e "s/%PACKAGE%/${PACKAGE_NAME}/g" "${BASE}/PKGBUILD.template" | \
sed -e "s/%VERSION%/${PACKAGE_VERSION}/g"                          | \
sed -e "s/%SHA_512%/${SHA_512}/g"                                    \
> "${BUILD_DIR}/PKGBUILD"
