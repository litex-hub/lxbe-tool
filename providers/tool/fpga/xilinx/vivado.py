def check_vivado(args):
    vivado_path = get_command("vivado")
    if vivado_path == None:
        # Look for the default Vivado install directory
        if os.name == 'nt':
            base_dir = r"C:\Xilinx\Vivado"
        else:
            base_dir = "/opt/Xilinx/Vivado"
        if os.path.exists(base_dir):
            for file in os.listdir(base_dir):
                bin_dir = base_dir + os.path.sep + file + os.path.sep + "bin"
                if os.path.exists(bin_dir + os.path.sep + "vivado"):
                    os.environ["PATH"] += os.pathsep + bin_dir
                    vivado_path = bin_dir
                    break
    if vivado_path == None:
        return (False, "toolchain not found in your PATH", "download it from https://www.xilinx.com/support/download.html")
    return (True, "found at {}".format(vivado_path))

