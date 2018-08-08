def main(args):
    if args.init:
        main_name = os.getcwd().split(os.path.sep)[-1] + '.py'
        new_main_name = input('What would you like your main program to be called? [' + main_name + '] ')
        if new_main_name is not None and new_main_name != "":
            main_name = new_main_name

        print("Initializing git repository")
        if not os.path.exists(DEPS_DIR):
            os.mkdir(DEPS_DIR)

        os.system("git init")
        os.system("git add " + str(__file__))

        os.system("git submodule add https://github.com/m-labs/migen.git deps/migen")
        os.system("git add deps/migen")

        os.system("git submodule add https://github.com/enjoy-digital/litex.git deps/litex")
        os.system("git add deps/litex")

        os.system("git submodule add https://github.com/enjoy-digital/litescope deps/litescope")
        os.system("git add deps/litescope")

        os.system("git submodule add https://github.com/pyserial/pyserial.git deps/pyserial")
        os.system("git add deps/pyserial")

        os.system("git submodule update --init --recursive")

        bin_tools = {
            'litex_server': 'litex.soc.tools.remote.litex_server',
            'litex_term': 'litex.soc.tools.litex_term',
            'mkmscimg': 'litex.soc.tools.mkmscimg',
        }
        bin_template = """
#!/usr/bin/env python3
import sys
import os
# This script lives in the "bin" directory, but uses a helper script in the parent
# directory.  Obtain the current path so we can get the absolute parent path.
script_path = os.path.dirname(os.path.realpath(
    __file__)) + os.path.sep + os.path.pardir + os.path.sep
sys.path.insert(0, script_path)it
import lxbuildenv
from litex.soc.tools.mkmscimg import main
main()"""
        # Create binary programs under bin/
        if not os.path.exists("bin"):
            print("Creating binaries")
            os.mkdir("bin")
            for bin_name, python_module in bin_tools.items():
                with open('bin' + os.path.sep + bin_name, 'w') as new_bin:
                    new_bin.write(bin_template)
                    new_bin.write('from ' + python_module + ' import main\n')
                    new_bin.write('main()\n')
                os.system('git add --chmod=+x bin' + os.path.sep + bin_name)

        with open(main_name, 'w') as m:
            program_template = """#!/usr/bin/env python3
# This variable defines all the external programs that this module
# relies on.  lxbuildenv reads this variable in order to ensure
# the build will finish without exiting due to missing third-party
# programs.
LX_DEPENDENCIES = ["riscv", "vivado"]
# Import lxbuildenv to integrate the deps/ directory
import lxbuildenv
from migen import *
from litex.build.generic_platform import *
_io = [
    ("clk50", 0, Pins("J19"), IOStandard("LVCMOS33")),
]
class Platform(XilinxPlatform):
    def __init__(self, toolchain="vivado", programmer="vivado", part="35"):
        part = "xc7a" + part + "t-fgg484-2"
    def create_programmer(self):
        if self.programmer == "vivado":
            return VivadoProgrammer(flash_part="n25q128-3.3v-spi-x1_x2_x4")
        else:
            raise ValueError("{} programmer is not supported"
                             .format(self.programmer))
    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
class BaseSoC(SoCSDRAM):
    csr_peripherals = [
        "ddrphy",
#        "dna",
        "xadc",
        "cpu_or_bridge",
    ]
    csr_map_update(SoCSDRAM.csr_map, csr_peripherals)
    def __init__(self, platform, **kwargs):
        clk_freq = int(100e6)
def main():
    platform = Platform()
    soc = BaseSoC(platform)
    builder = Builder(soc, output_dir="build", csr_csv="test/csr.csv")
    vns = builder.build()
    soc.do_exit(vns)
if __name__ == "__main__":
    main()
"""
            m.write(program_template)
        return
