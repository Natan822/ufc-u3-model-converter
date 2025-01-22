from file import File
import logging

logger = logging.getLogger(__name__)

class TexFile(File):

    def __init__(self, name: str, size: int, data: bytes, isCompressed: bool):
        super().__init__(name, size, data, isCompressed, "tex")