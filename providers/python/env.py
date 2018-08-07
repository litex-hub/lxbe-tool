


# Python randomizes the order in which it traverses hashes, and Migen uses
# hashes an awful lot when bringing together modules.  As such, the order
# in which Migen generates its output Verilog will change with every run,
# and the addresses for various modules will change.
# Make builds deterministic so that the generated Verilog code won't change
# across runs.
os.environ["PYTHONHASHSEED"] = "1"
