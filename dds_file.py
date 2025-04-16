from file import File
try:
    from wand.image import Image as WandImage
except ImportError:
    import gui_error
    gui_error.imagemagick_not_installed()

import logging

logger = logging.getLogger(__name__)

class DdsFile(File):

    def __init__(self, name: str, size: int, data: bytes, isCompressed: bool):
        super().__init__(name, size, data, isCompressed, "dds")

    def patch(self):
        width = 0
        height = 0
        name_without_id = self.name[3:] # File name without fighter ID
        if name_without_id == "_skin":
            width = height = 1024
        elif name_without_id == "_skin_n":
            width = height = 512
        elif name_without_id == "_trunks_c" or name_without_id == "_trunks_c2":
            width = 512
            height = 256
        elif name_without_id == "_eye":
            width = height = 64
        else:
            logger.info(f"{self.get_name_with_extension()} is not a patchable file.")
            return

        self.downscale(width, height)

    def downscale(self, width: int, height: int):
        if self.isCompressed:
            self.decompress()

        logger.info(f"Downscaling {self.get_name_with_extension()} to {width}x{height} ...")
        with WandImage(blob=self.data) as image:
            image.resize(width, height)
            self.data = image.make_blob()
            self.size = len(self.data)

            logger.info(f"{self.get_name_with_extension()} downscaled!")

    def write_pac(self, tex_path: str):
        if not self.isCompressed:
            self.compress()
        super().write_pac(tex_path)