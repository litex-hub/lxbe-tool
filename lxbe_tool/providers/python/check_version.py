


"python --version"
"Python 2.7.13"
"Python 3.5.3"

"""
Just check you can import a module.

function check_import {
	MODULE=$1
	if python3 -c "import $MODULE"; then
		echo "$MODULE found"
		return 0
	else
		echo "$MODULE *NOT* found!"
		echo "Please try running the $SETUP_DIR/download-env.sh script again."
		return 1
	fi
}
"""

"""
Just check you can import a module and it is of the correct version.

function check_import_version {
	MODULE=$1
	EXPECT_VERSION=$2
	ACTUAL_VERSION=$(python3 -c "import $MODULE; print($MODULE.__version__)")
	if echo "$ACTUAL_VERSION" | grep -q $EXPECT_VERSION > /dev/null; then
		echo "$MODULE found at $ACTUAL_VERSION"
		return 0
	else
		echo "$MODULE (version $EXPECT_VERSION) *NOT* found!"
		echo "Please try running the $SETUP_DIR/download-env.sh script again."
		return 1
	fi
}
"""

def check_python_version(args):
    import platform
    # Litex / Migen require Python 3.5 or newer.  Ensure we're running
    # under a compatible version of Python.
    if sys.version_info[:3] < (3, 5):
        return (False,
            "python: You need Python 3.5+ (version {} found)".format(sys.version_info[:3]))
    return (True, "python 3.5+: ok (Python {} found)".format(platform.python_version()))
