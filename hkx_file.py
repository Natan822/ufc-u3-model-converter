from file import File
import logging


logger = logging.getLogger(__name__)

class HkxFile(File):

    def __init__(self, name: str, size: int, data: bytes, isCompressed: bool):
        super().__init__(name, size, data, isCompressed, "hkx")

    def patch(self):
        logger.info(f"Patching {self.get_name_with_extension()} ...")

        if self.isCompressed:
            self.decompress()

        data_array = bytearray(self.data)
        data_array[0x12] = 0
        self.data = bytes(data_array)

        logger.info(f"{self.get_name_with_extension()} patched!")

    def write_pac(self, pac_path: str):
        if not self.isCompressed:
            self.compress()
        super().write_pac(pac_path)

    def write_mpc(self, mpc_path: str):
        if not self.isCompressed:
            self.compress()
        super().write_mpc(mpc_path)