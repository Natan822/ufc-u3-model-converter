from abc import abstractmethod, ABC
from file import File

class PatchableFile(ABC, File):

    @abstractmethod
    def patch(self):
        pass