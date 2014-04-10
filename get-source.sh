#!/bin/sh

REPO_URL="https://github.com/ariya/phantomjs.git"
VERSION="1.9.7"
PREFIX="phantomjs-${VERSION}"
ARCHIVE_NAME="${PREFIX}-source.tar.gz"

#
#

if ! which git >/dev/null 2>&1 ; then
	echo "Missing 'git' executable. Git is necessary to download sources."
	exit 1
fi

if ! which rpmbuild >/dev/null 2>&1 ; then
	echo "Missing 'rpmbuild' executable. You want to build an .rpm using rpmbuild, so where's your rpmbuild? (It's neccessary to determine your %{_topdir}/SOURCE ;)"
	exit 1
fi


TEMP_DIR="$( mktemp -d )"

echo "Created temporary directory ${TEMP_DIR}"

CHECKOUT_DIR="${TEMP_DIR}/phantomjs"

mkdir ${CHECKOUT_DIR}

pushd ${CHECKOUT_DIR} >/dev/null

git clone ${REPO_URL} .

ARCHIVE="$( readlink -f ../${ARCHIVE_NAME} )"

echo "Creating archive ${ARCHIVE}"

git archive --format=tar -o ${ARCHIVE} --prefix ${PREFIX}/ refs/tags/${VERSION}

echo -n "The current Git Hash is: "

git rev-parse refs/tags/${VERSION}

popd >/dev/null


# Try to evaluate default rpm build top dir
#
# TODO: add option to specify SOURCE directory 
#
RPMBUILD_DIR="$( rpmbuild -E '%{_topdir}' 2>/dev/null )"


if [ -z "${RPMBUILD_DIR}" ]; then
	echo "Error: rpmbuild '_topdir' not found (through rpmbuild -E)."
	exit 1
fi

echo "Found rpmbuild directory '${RPMBUILD_DIR}"

RPMBUILD_SOURCES_DIR="${RPMBUILD_DIR}/SOURCES"

if [ ! -d "${RPMBUILD_SOURCES_DIR}" ]; then
	echo "Directory 'SOURCES' does not exist in rpmbuild directory '${RPMBUILD_DIR}'"
	exit 1
fi

if [ -e "${RPMBUILD_SOURCES_DIR}/${ARCHIVE}" ]; then
	echo "File ${ARCHIVE} already exists at ${RPMBUILD_SOURCES_DIR}. Exit."
	exit 1
fi

echo "Copying archive to '${RPMBUILD_SOURCES_DIR}' ..."

cp ${ARCHIVE} ${RPMBUILD_SOURCES_DIR}




echo "Left checked out repository and archive at ${TEMP_DIR}"

