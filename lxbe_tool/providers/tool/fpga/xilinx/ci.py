"""

Extension to get the "cut back" Xilinx toolchain when running on CI.

# Cutback Xilinx ISE for CI
# --------
# Save the passphrase to a file so we don't echo it in the logs
if [ ! -z "$XILINX_PASSPHRASE" ]; then
	XILINX_PASSPHRASE_FILE=$(tempfile -s .passphrase | mktemp --suffix=.passphrase)
	trap "rm -f -- '$XILINX_PASSPHRASE_FILE'" EXIT
	echo $XILINX_PASSPHRASE >> $XILINX_PASSPHRASE_FILE

	# Need gpg to do the unencryption
	export XILINX_DIR=$BUILD_DIR/Xilinx
	export LIKELY_XILINX_LICENSE_DIR=$XILINX_DIR
	if [ ! -d "$XILINX_DIR" -o ! -d "$XILINX_DIR/opt" ]; then
		(
			cd $BUILD_DIR
			mkdir -p Xilinx
			cd Xilinx

			wget -q http://xilinx.timvideos.us/index.txt -O xilinx-details.txt
			XILINX_TAR_INFO=$(cat xilinx-details.txt | grep tar.bz2.gpg | tail -n 1)
			XILINX_TAR_FILE=$(echo $XILINX_TAR_INFO | sed -e's/[^ ]* //' -e's/.gpg$//')
			XILINX_TAR_MD5=$(echo $XILINX_TAR_INFO | sed -e's/ .*//')

			# This setup was taken from https://github.com/m-labs/artiq/blob/master/.travis/get-xilinx.sh
			wget --no-verbose -c http://xilinx.timvideos.us/${XILINX_TAR_FILE}.gpg
			cat $XILINX_PASSPHRASE_FILE | gpg --batch --passphrase-fd 0 ${XILINX_TAR_FILE}.gpg
			tar -xjf $XILINX_TAR_FILE

			# Remove the tar file to free up space.
			rm ${XILINX_TAR_FILE}*

			# FIXME: Hacks to try and make Vivado work.
			mkdir -p $XILINX_DIR/opt/Xilinx/Vivado/2017.3/scripts/rt/data/svlog/sdbs
			mkdir -p $XILINX_DIR/opt/Xilinx/Vivado/2017.3/tps/lnx64/jre

			# Make ISE stop complaining about missing wbtc binary
			mkdir -p $XILINX_DIR/opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64
			ln -s /bin/true $XILINX_DIR/opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/wbtc

			# Relocate ISE from /opt to $XILINX_DIR
			for i in $(grep -l -Rsn "/opt/Xilinx" $XILINX_DIR/opt)
			do
				sed -i -e "s!/opt/Xilinx!$XILINX_DIR/opt/Xilinx!g" $i
			done
			wget --no-verbose http://xilinx.timvideos.us/Xilinx.lic.gpg
			cat $XILINX_PASSPHRASE_FILE | gpg --batch --passphrase-fd 0 Xilinx.lic.gpg

			#git clone https://github.com/mithro/impersonate_macaddress
			#cd impersonate_macaddress
			#make
		)
	fi
	rm $XILINX_PASSPHRASE_FILE
	trap - EXIT
fi
if [ -z "$LIKELY_XILINX_LICENSE_DIR" ]; then
	LIKELY_XILINX_LICENSE_DIR="$HOME/.Xilinx"
fi
"""
