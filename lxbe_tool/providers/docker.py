
"""

Based on this example -> https://github.com/open-power/pdbg/blob/master/.build.sh

TEMPDIR=`mktemp -d ${HOME}/pdbgobjXXXXXX`
RUN_TMP="docker run --rm=true --user=${USER} -w ${TEMPDIR} -v ${HOME}:${HOME} -t ${CONTAINER}"
${RUN_TMP} ${SRCDIR}/configure --host=arm-linux-gnueabi
${RUN_TMP} make
rm -rf ${TEMPDIR}



"""
