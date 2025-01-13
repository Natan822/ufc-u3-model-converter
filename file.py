import io
import utils
import logging

logger = logging.getLogger(__name__)

class File:

    def __init__(self, name: str, size: int, data: bytes, isCompressed: bool, extension: str):
        self.name = name
        self.size = size
        self.data = data
        self.isCompressed = isCompressed
        self.extension = extension

    def save(self, output_path: str):
        output_path = f"{output_path}\\{self.get_name_with_extension()}"
        with open(output_path, "wb") as file:
            file.write(self.data)

            logger.info(f"{self.get_name_with_extension()} saved at {output_path}.")


    def decompress(self):
        logger.info(f"Decompressing {self.get_name_with_extension()} ...")
        if self.isCompressed:
            self.data = utils.decompress_yzli(self.data)
            self.isCompressed = False
            self.size = len(self.data)

            logger.info(f"    - {self.get_name_with_extension()} decompressed!")
        else:
            logger.info(f"{self.get_name_with_extension()} is already decompressed.")

    def compress(self):
        logger.info(f"Compressing {self.get_name_with_extension()} ...")
        if not self.isCompressed:
            self.data = utils.compress_yzli(self.data, self.name)
            self.isCompressed = True
            self.size = len(self.data)

            logger.info(f"    - {self.get_name_with_extension()} compressed!")
        else:
            logger.info(f"{self.get_name_with_extension()} is already compressed.")

    def get_name_with_extension(self) -> str:
        return f"{self.name}.{self.extension}"

    def write_pac_path(self, pac_path: str):
        logger.info(f"Writing {self.get_name_with_extension()} into {pac_path} ...")

        with open(pac_path, "r+b") as file:
            files_count = int.from_bytes(file.read(4), byteorder="big")
            file.read(0xC) # Skip rest of the header
            for i in range(files_count):
                _name = file.read(0x10).decode("utf-8").replace("\x00", "")
                _extension = file.read(4).decode("utf-8").replace("\x00", "")
                size_position = file.tell()
                file.read(4) # Skip size for now
                _offset = int.from_bytes(file.read(4), byteorder="big")
                file.read(4) # Skip zeroes

                if _name == self.name and _extension == self.extension:
                    file.seek(_offset)
                    header = file.read(4)
                    if header.decode() == "YZLI" and not self.isCompressed:
                        self.compress()

                    file.seek(_offset)

                    file.write(self.data[:8])
                    file.read(8)  # Skip filename writing
                    file.write(self.data[16:])

                    # Update data size
                    file.seek(size_position)
                    file.write(self.size.to_bytes(4, byteorder="big"))

                    logger.info(f"    - {self.get_name_with_extension()} successfully written into .pac.")
                    return
            logger.warning(f"Failed to write {self.get_name_with_extension()} into {pac_path}: File not found within {pac_path}.")

    def write_pac_buffer(self, pac_file: "File"):
        logger.info(f"Writing {self.get_name_with_extension()} into .pac file ...")

        file = io.BytesIO(pac_file.data)
        files_count = int.from_bytes(file.read(4), byteorder="big")
        file.read(0xC)  # Skip rest of the header
        for i in range(files_count):
            _name = file.read(0x10).decode("utf-8").replace("\x00", "")
            _extension = file.read(4).decode("utf-8").replace("\x00", "")
            size_position = file.tell()
            file.read(4)  # Skip size for now
            _offset = int.from_bytes(file.read(4), byteorder="big")
            file.read(4)  # Skip zeroes

            if _name == self.name and _extension == self.extension:
                file.seek(_offset)
                header = file.read(4)
                if header.decode() == "YZLI" and not self.isCompressed:
                    self.compress()

                file.seek(_offset)

                file.write(self.data[:8])
                file.read(8) # Skip filename writing
                file.write(self.data[16:])

                # Update data size
                file.seek(size_position)
                file.write(self.size.to_bytes(4, byteorder="big"))

                file.seek(0)
                pac_file.data = file.read()
                pac_file.size = len(pac_file.data)
                logger.info(f"    - {self.get_name_with_extension()} successfully written into .pac.")
                return
        logger.warning(
            f"Failed to write {self.get_name_with_extension()} into .pac file: File not found within .pac file.")

    def write_mpc(self, mpc_path: str):
        logger.info(f"Writing {self.get_name_with_extension()} into {mpc_path} ...")

        with open(mpc_path, "r+b") as file:
            info_size = int.from_bytes(file.read(4), byteorder="big")
            mpc_size = int.from_bytes(file.read(4), byteorder="big")
            info_offset = int.from_bytes(file.read(4), byteorder="big")
            base_offset = int.from_bytes(file.read(4), byteorder="big")
            files_count = int((info_size - info_offset) / 0x28)

            file.seek(info_offset)
            files_info_buffer = file.read(files_count * 0x28)

            byte_index = 0
            while (byte_index < len(files_info_buffer)):
                entries = int.from_bytes(files_info_buffer[byte_index: byte_index + 4], byteorder="big")
                byte_index += 4

                file_name = files_info_buffer[byte_index: byte_index + 0x20].decode("utf-8", errors="ignore").replace("\x00", "")
                byte_index += 0x20

                if file_name == self.get_name_with_extension():
                    file_offset = int.from_bytes(files_info_buffer[byte_index: byte_index + 4], byteorder="big")
                    file.seek(file_offset + base_offset)

                    header = file.read(4)
                    if header.decode(errors="ignore") == "YZLI" and not self.isCompressed:
                        self.compress()

                    file.seek(file_offset + base_offset)

                    file.write(self.data[:8])
                    file.read(8) # Skip filename writing
                    file.write(self.data[16:])

                    logger.info(f"    - {self.get_name_with_extension()} successfully written into {mpc_path}.")
                    return
                byte_index += 4
            logger.warning(f"Failed to write {self.get_name_with_extension()} into {mpc_path}: File not found within {mpc_path}.")


