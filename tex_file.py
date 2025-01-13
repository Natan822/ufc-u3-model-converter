from dds_file import DdsFile
from file import File
import utils
import logging

logger = logging.getLogger(__name__)

class TexFile(File):

    def __init__(self, name: str, size: int, data: bytes, isCompressed: bool):
        super().__init__(name, size, data, isCompressed, "tex")

    def extract_dds(self):
        logger.info(f"Extracting dds files from {self.get_name_with_extension()} ...")

        dds_files = []
        row_index = 0
        while sum(self.data[row_index: row_index + 16]) != 0:
            if self.data[row_index:row_index + 3] == b"dds":
                name = self.data[row_index - 16: row_index].decode("utf-8").replace("\x00", "")
                offset = utils.get_offset(self.data, row_index)
                size = utils.get_size(self.data, row_index)
                data = self.data[offset: size]
                dds_files.append(DdsFile(name, size, data))

                logger.info(f"    - {name}.dds; size: {size} bytes; offset: {offset} extracted.")

            row_index += 16

        logger.info(f"{len(dds_files)} files extracted from {self.get_name_with_extension()}.")
        return dds_files