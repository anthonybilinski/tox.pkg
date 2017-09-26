#!/bin/sh

set -e

PACKAGE_NAME="libtoxcore"
PACKAGE_DATE=$(LC_ALL=C date "+%a, %d %b %Y %H:%M:%S %z")
PACKAGE_VERSION=$(date "+%Y%m%d%H%M")
SPEC_DATE=$(LC_ALL=C date '+%a %b %d %Y')

BASE=`dirname $0`
cd "${BASE}"
BASE=$(pwd)

BUILD_DIR="${BASE}/../build/${PACKAGE_NAME}"
SOURCE_DIR="${BUILD_DIR}/${PACKAGE_NAME}"

mkdir -p "${BUILD_DIR}"

rm -rf "${SOURCE_DIR}"

git clone --recursive https://github.com/TokTok/c-toxcore.git "${SOURCE_DIR}"

cd "${SOURCE_DIR}"

GIT_REV=$1

if [ -n "${GIT_REV}" ]; then
	git checkout "${GIT_REV}"
fi

rm -f "${BUILD_DIR}/PKGBUILD"
rm -f "${BUILD_DIR}/${PACKAGE_NAME}.spec"
rm -f "${BUILD_DIR}/${PACKAGE_NAME}_"*.dsc
rm -f "${BUILD_DIR}/${PACKAGE_NAME}_"*.tar.bz2
rm -f "${BUILD_DIR}/${PACKAGE_NAME}_"*.changes
rm -f "${BUILD_DIR}/${PACKAGE_NAME}_"*.build

cp -rf "${BASE}/debian" "${SOURCE_DIR}/debian"

cp -f "${BASE}/tox-bootstrapd.sh"        "${SOURCE_DIR}/other/bootstrap_daemon/tox-bootstrapd.sh"
cp -f "${BASE}/tox-bootstrapd.centos.sh" "${SOURCE_DIR}/other/bootstrap_daemon/tox-bootstrapd.centos.sh"
cp -f "${BASE}/tox-bootstrapd.service"   "${SOURCE_DIR}/other/bootstrap_daemon/tox-bootstrapd.service"
cp -f "${BASE}/tox-bootstrapd.tmpfiles"  "${SOURCE_DIR}/other/bootstrap_daemon/tox-bootstrapd.tmpfiles"
cp -f "${BASE}/tox-bootstrapd.users"     "${SOURCE_DIR}/other/bootstrap_daemon/tox-bootstrapd.users"

PACKAGE_REVISION=$(git rev-parse HEAD)
PACKAGE_REVISION_SHORT=$(expr substr "${PACKAGE_REVISION}" 1 7)
PACKAGE_VERSION="${PACKAGE_VERSION}~${PACKAGE_REVISION_SHORT}"

sed -i -e "s/%PACKAGE%/${PACKAGE_NAME}/g"      "debian/changelog"
sed -i -e "s/%DATE%/${PACKAGE_DATE}/g"         "debian/changelog"
sed -i -e "s/%VERSION%/${PACKAGE_VERSION}/g"   "debian/changelog"
sed -i -e "s/%REVISION%/${PACKAGE_REVISION}/g" "debian/changelog"

sed -i -e "s/%VERSION%/${PACKAGE_VERSION}/g" "other/bootstrap_daemon/tox-bootstrapd.conf"

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

cp -f "${BASE}/PKGBUILD.install" "${BUILD_DIR}/${PACKAGE_NAME}.install"
