import utils
from dds_file import DdsFile
from hkx_file import HkxFile
from patchable_file import PatchableFile
from tex_file import TexFile
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    Tk().withdraw()
    pac_filename = askopenfilename(title="Select a .pac file",
                                   filetypes=[("Pac files", "*.pac"), ("All Files", "*.*")])
    mpc_filename = askopenfilename(title="Select a .mpc file",
                                   filetypes=[("Mpc files", "*.mpc"), ("All Files", "*.*")])

    pac_input = output_pac = pac_filename
    mpc_input = output_mpc = mpc_filename

    hkx_pac_files = []
    tex_files = []
    dds_files = []
    hkx_mpc_files = []
    if pac_input != "":
        utils.backup_file(pac_input)
        hkx_pac_files = list[HkxFile](utils.extract_pac_path(pac_input, "hkx"))
        tex_files = list[TexFile](utils.extract_pac_path(pac_input, "tex"))
        if len(tex_files) == 1:
            dds_files = list[DdsFile](utils.extract_pac_buffer(tex_files[0].data, "dds"))
        else:
            logger.warning("More than one or no .tex files found.")
            return

    if mpc_input != "":
        utils.backup_file(mpc_input)
        hkx_mpc_files = list[HkxFile](utils.extract_mpc(mpc_input, "hkx"))

    all_files = list[PatchableFile](hkx_pac_files + hkx_mpc_files + dds_files)
    for file in all_files:
        file.decompress()
        file.patch()
    for file in dds_files:
        file.write_pac_buffer(tex_files[0])
    for file in hkx_mpc_files:
        file.write_mpc(output_mpc)
    for file in hkx_pac_files:
        file.write_pac_path(output_pac)
    for file in tex_files:
        file.write_pac_path(output_pac)

if __name__ == '__main__':
    main()