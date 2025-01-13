from dds_file import DdsFile
from hkx_file import HkxFile
from tex_file import TexFile
from file import File
import zlib
import logging

logger = logging.getLogger(__name__)

def backup_file(input_path: str):
    logger.info(f"Creating copy of {input_path} ...")
    with open(input_path, "rb") as fr:
        buffer = fr.read()
        with open(input_path + ".bak", "wb") as fw:
            fw.write(buffer)
            logger.info(f"    - Copy created at {input_path}.bak.")

def decompress_yzli(data: bytes) -> bytes:
    return zlib.decompress(data[16:])

def extract_pac_path(input_path: str, extension: str) -> list[File]:
    logger.info(f"Attempting to extract .{extension} files from {input_path} ...")
    with open(input_path, "rb") as file:
        buffer = file.read()

    return extract_pac_buffer(buffer, extension)

def extract_pac_buffer(buffer: bytes, extension: str) -> list[File]:
    if extension not in ["hkx", "tex", "dds"]:
        logger.warning(f"Unsupported extension: .{extension} cannot be extracted.")
        return []

    files = []
    files_count = int.from_bytes(buffer[:4], byteorder="big")
    row_index = 0
    for i in range((files_count * 2) + 1): # Info sections of files occupy each "2 rows"(2 * 0x10 bytes)
        if buffer[row_index:row_index + 3] == extension.encode():
            file_name = buffer[row_index - 16: row_index].decode("utf-8", errors="ignore").replace("\x00", "")
            file_offset = int.from_bytes(buffer[row_index + 8: row_index + 12], byteorder="big")
            #file_size = int.from_bytes(buffer[row_index + 4: row_index + 8], byteorder="big")
            # Size is calculated this way: (next_file.offset - current_file.offset)
            # However, if this is the last file, then: (pac_file.size - current_file.offset)
            file_size = 0
            if i == (files_count * 2): # Last file
                file_size = len(buffer) - file_offset
            else:
                next_file_offset = int.from_bytes(buffer[row_index + 0x20 +  8: row_index + 0x20 + 12], byteorder="big")
                file_size = next_file_offset - file_offset

            data = buffer[file_offset: file_offset + file_size]

            if extension == "hkx":
                files.append(HkxFile(file_name, file_size, data, True))
            elif extension == "tex":
                files.append(TexFile(file_name, file_size, data, False))
            elif extension == "dds":
                files.append(DdsFile(file_name, file_size, data, True))

            logger.info(f"    - {file_name}.{extension}; size: {hex(file_size)} bytes; offset: {hex(file_offset)} extracted.")

        row_index += 0x10
    logger.info(f"Extraction of .{extension} files finished! {len(files)} files extracted!")
    return files

def extract_mpc(input_path: str, extension: str) -> list[File]:
    if extension != "hkx":
        logger.warning(f"Unsupported extension .{extension} cannot be extracted from {input_path}.")
        return []

    logger.info(f"Attempting to extract .{extension} files from {input_path} ...")

    files = []
    with open(input_path, "rb") as file:
        info_size = int.from_bytes(file.read(4), byteorder="big")
        mpc_size = int.from_bytes(file.read(4), byteorder="big")
        info_offset = int.from_bytes(file.read(4), byteorder="big")
        base_offset = int.from_bytes(file.read(4), byteorder="big")
        files_count = int((info_size - info_offset) / 0x28)

        file.seek(info_offset)
        files_info_buffer = file.read(files_count * 0x28)

        byte_index = 0
        while (byte_index < len(files_info_buffer)):
            # File size when most significant byte = 0xFF
            entries = int.from_bytes(files_info_buffer[byte_index: byte_index + 4], byteorder="big")
            byte_index += 4

            file_name = files_info_buffer[byte_index: byte_index + 0x20].decode("utf-8", errors="ignore").replace("\x00", "")
            file_extension = file_name[-3:]
            # Remove file extension from its name
            file_name = file_name[:-4]
            byte_index += 0x20

            if file_extension == extension:
                file_offset = int.from_bytes(files_info_buffer[byte_index: byte_index + 4], byteorder="big")
                file.seek(file_offset + base_offset)
                size = (entries & 0x00FFFFFF) * 0x20
                data = file.read(size)

                logger.info(f"    - {file_name}.{extension}; size: {hex(size)} bytes; offset: {hex(file_offset)} extracted.")
                files.append(HkxFile(file_name, size, data, True))

            byte_index += 4
    logger.info(f"Extraction from {input_path} finished! {len(files)} files extracted!")
    return files

def compress_yzli(data: bytes, name: str) -> bytes:
    data_size = len(data)
    header = b"YZLI" + data_size.to_bytes(4, byteorder="little") + (0).to_bytes(8, "little")
    compressed_data = zlib.compress(data, level=9)
    return header + compressed_data

# def decompress_yzli(input_path: str, output_path: str):
#     with open(input_path, "rb") as file:
#         buffer = file.read()
#
#     decompressed_data = zlib.decompress(buffer)
#     with open(output_path, "wb") as file:
#         file.write(decompressed_data)