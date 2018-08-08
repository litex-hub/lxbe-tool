#!/usr/bin/env python3

"""
Conda based provider.

https://conda.io/docs/

Conda is an open source package management system and environment management
system that runs on Windows, macOS and Linux. Conda quickly installs, runs and
updates packages and their dependencies. Conda easily creates, saves, loads and
switches between environments on your local computer. It was created for Python
programs, but it can package and distribute software for any language.
"""

import os
import re
import platform
import requests
from collections import namedtuple

from . import Provider


CondaVersionTuple = namedtuple("CondaVersionTuple", ("version", "system", "machine", "file"))


def _parse_version(filename):
    """Parse a Miniconda file name into a CondaVersionTuple object.

    >>> _parse_version('Miniconda-1.9.1-Linux-x86_64.sh')
    CondaVersionTuple(version=(1, 9, 1), system='Linux', machine='x86_64', file='Miniconda-1.9.1-Linux-x86_64.sh')
    >>> _parse_version('Miniconda3-2.2.8-Windows-x86.exe')
    CondaVersionTuple(version=(2, 2, 8), system='Windows', machine='x86', file='Miniconda3-2.2.8-Windows-x86.exe')
    >>> _parse_version('Miniconda-3.16.0-Linux-armv7l.sh')
    CondaVersionTuple(version=(3, 16, 0), system='Linux', machine='armv7l', file='Miniconda-3.16.0-Linux-armv7l.sh')
    """
    s = os.path.splitext(filename)[0]
    assert '-' in s, s
    m, version, system, arch = s.split('-')
    if version != 'latest':
        assert '.' in version, version
        version = tuple(int(v) for v in version.split('.'))
    assert m.startswith('Miniconda')
    return CondaVersionTuple(version, system, arch, filename)


def _extract_versions(s):
    """Extract the available Miniconda version tuples from index page.

    >>> versions = _extract_versions('''
    ...             <tr>
    ...       <td><a href="Miniconda3-1.9.1-Linux-x86_64.sh">Miniconda-1.9.1-Linux-x86_64.sh</a></td>
    ...      <td class="s">18.9M</td>
    ...      <td>2013-09-06 15:52:09</td>
    ...      <td>7e446886360e48bf937c3b6eca610790</td>
    ...    </tr>
    ...    <tr>
    ...      <td><a href="Miniconda3-1.6.0-Linux-x86_64.sh">Miniconda-1.6.0-Linux-x86_64.sh</a></td>
    ...      <td class="s">18.7M</td>
    ...      <td>2013-06-21 15:30:53</td>
    ...      <td>892d6abdfe274765036ff174f2b360b0</td>
    ...    </tr>
    ...  </table>
    ...  <address>Updated: 2018-06-07 00:11:09 CDT - Files: 376</address>
    ...  <div>
    ... ''')
    >>> for v in versions:
    ...     print(v)
    CondaVersionTuple(version=(1, 9, 1), system='Linux', machine='x86_64', file='Miniconda3-1.9.1-Linux-x86_64.sh')
    CondaVersionTuple(version=(1, 6, 0), system='Linux', machine='x86_64', file='Miniconda3-1.6.0-Linux-x86_64.sh')

    """
    for x in re.findall('a href="([^"]*)"', s):
        if not x.startswith('Miniconda3'):
            continue
        v = _parse_version(x)
        if v.version == "latest":
            continue
        yield v


# FIXME: Cache the live_versions in some way?
def live_versions():
    """Get the versions currently live on conda website."""
    versions = {}
    for ver in _extract_versions(requests.get('https://repo.continuum.io/miniconda').text):
        if ver.system not in versions:
            versions[ver.system] = {}
        system_versions = versions[ver.system]
        if ver.machine not in system_versions:
            system_versions[ver.machine] = []
        machine_versions = system_versions[ver.machine]
        machine_versions.append(ver)
        machine_versions.sort()
    return versions


def installed_version():
    """
    ~/conda/bin/conda --version
    conda 4.5.9
    """
    pass



class Conda(Provider):
    """

    The Conda provider can provide;
     * Python environment which modules can be installed into.
     * Tools (such as gcc / openocd)

    """


    def __init__(self, download_dir):
        # platform.machine() == 'x86'     32bit x86 computer
        # platform.machine() == 'x86_64'  64bit x86 computer
        # platform.machine() == 'armv6l'  Older RPi
        # platform.machine() == 'armv7l'  Newest RPi
        self.installer_url = self.INSTALLER_URL[platform.system()][platform.machine()]
        pass

    def install_module(self, module):
        """
# lite
for LITE in $LITE_REPOS; do
	LITE_DIR=$THIRD_DIR/$LITE
	(
		echo
		cd $LITE_DIR
		echo "Installing $LITE from $LITE_DIR (local python module)"
		python setup.py develop
	)
	check_import $LITE
done
        """
        pass

    def install_tool(self, toolname):
        """
# binutils for the target
echo
echo "Installing binutils for ${CPU} (assembler, linker, and other tools)"
conda install -y $CONDA_FLAGS binutils-${CPU}-elf=$BINUTILS_VERSION
check_version ${CPU}-elf-ld $BINUTILS_VERSION

# gcc for the target
echo
echo "Installing gcc for ${CPU} ('bare metal' C cross compiler)"
conda install -y $CONDA_FLAGS gcc-${CPU}-elf-nostdc=$GCC_VERSION
check_version ${CPU}-elf-gcc $GCC_VERSION

# gdb for the target
#echo
#echo "Installing gdb for ${CPU} (debugger)"
#conda install -y $CONDA_FLAGS gdb-${CPU}-elf=$GDB_VERSION
#check_version ${CPU}-elf-gdb $GDB_VERSION

# openocd for programming via Cypress FX2
echo
echo "Installing openocd (jtag tool for programming and debug)"
conda install -y $CONDA_FLAGS openocd=$OPENOCD_VERSION
check_version openocd $OPENOCD_VERSION
        """
        pass

    def setup(self):
        """

# Hot patch conda so to not use the systems environments.
function fix_conda {
	for py in $(find $CONDA_DIR -name envs_manager.py); do
		START_SUM=$(sha256sum $py | sed -e's/ .*//')
		sed -i -e"s^expand(join('~', '.conda', 'environments.txt'))^join('$CONDA_DIR', 'environments.txt')^" $py
		END_SUM=$(sha256sum $py | sed -e's/ .*//')
		if [ $START_SUM != $END_SUM ]; then
			sed -i -e"s/$START_SUM/$END_SUM/" $(find $CONDA_DIR -name paths.json)
		fi
	done
}

if [[ ! -e $CONDA_DIR/bin/conda ]]; then
    wget -c https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    chmod a+x Miniconda3-latest-Linux-x86_64.sh
    # -p to specify the install location
    # -b to enable batch mode (no prompts)
    # -f to not return an error if the location specified by -p already exists
    ./Miniconda3-latest-Linux-x86_64.sh -p $CONDA_DIR -b -f
    fix_conda
    conda config --system --set always_yes yes
    conda config --system --set changeps1 no
    conda config --system --add envs_dirs $CONDA_DIR/envs
    conda config --system --add pkgs_dirs $CONDA_DIR/pkgs
    conda update -q conda
fi
fix_conda
conda config --system --add channels timvideos
conda info
        """
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import pprint
    print()
    print("Current live conda versions")
    print("-"*75)
    pprint.pprint(live_versions())
