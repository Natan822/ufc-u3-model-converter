from file import File
import extraction_utils
import os
import zlib
import logging

logger = logging.getLogger(__name__)

failed_files = []
converted_files = []

def convert_folder(folder_path: str):
    global failed_files, converted_files

    dirs = os.listdir(folder_path)
    for dir in dirs:
        full_path = os.path.join(folder_path, dir)

        # It's a folder
        if os.path.isdir(full_path):
            convert_folder(full_path)
        # It's a file
        else:
            file_extension = full_path[-4:]
            try:
                if file_extension == ".pac":
                    convert_files(full_path, "")
                    converted_files.append(full_path)
                elif file_extension == ".mpc":
                    convert_files("", full_path)
                    converted_files.append(full_path)

            except zlib.error or Exception as e:
                failed_files.append(full_path)
                logger.critical(f"Error: {e}\n.")
                logger.warning(f"Failed to convert {full_path}.")

def convert_files(pac_filepath: str, mpc_filepath: str):
    pac_input = output_pac = pac_filepath
    mpc_input = output_mpc = mpc_filepath

    if pac_input != "":
        logger.info(f"Attempting to convert {pac_input} ...")
    if mpc_input != "":
        logger.info(f"Attempting to convert {mpc_input} ...")

    hkx_pac_files = []
    tex_files = []
    dds_files = []
    hkx_mpc_files = []
    if pac_input != "":
        extraction_utils.backup_file(pac_input, pac_input)
        hkx_pac_files = list[File](extraction_utils.extract_pac_path(pac_input, "hkx"))
        tex_files = list[File](extraction_utils.extract_pac_path(pac_input, "tex"))
        if len(tex_files) == 1:
            dds_files = list[File](extraction_utils.extract_pac_buffer(tex_files[0].data, "dds"))
        else:
            logger.critical("More than one or no .tex files found.")
            return

    if mpc_input != "":
        extraction_utils.backup_file(mpc_input, mpc_input)
        hkx_mpc_files = list[File](extraction_utils.extract_mpc(mpc_input, "hkx"))

    all_files = list[File](hkx_pac_files + hkx_mpc_files + dds_files)
    # Decompress and patch files
    for file in all_files:
        file.decompress()
        file.patch()
    # Write .dds files back into all.tex
    for file in dds_files:
        file.write_pac_buffer(tex_files[0])
    # Write .mpc's .hxk files back into (id)_acce.mpc
    for file in hkx_mpc_files:
        file.write_mpc(output_mpc)
    # Write .mpc's .hxk files back into (id).pac
    for file in hkx_pac_files:
        file.write_pac_path(output_pac)
    # Write all.tex back into (id).pac
    for file in tex_files:
        file.write_pac_path(output_pac)

    if pac_input != "":
        print(f"Successfully converted {pac_input}.")
    if mpc_input != "":
        print(f"Successfully converted {mpc_input}.")

def display_results():
    global failed_files, converted_files

    print(f"{len(converted_files)} files converted:")
    for file in converted_files:
        print(f" - {file}")

    print(f"{len(failed_files)} files failed to convert:")
    for file in failed_files:
        print(f" - {file}")

    converted_files = failed_files = []