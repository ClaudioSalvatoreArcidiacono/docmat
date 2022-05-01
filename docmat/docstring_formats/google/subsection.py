from abc import ABC, abstractclassmethod

class Subsection(ABC):

    @abstractclassmethod
    def find_end_offset():
        raise NotImplementedError()

    @abstractclassmethod
    def from_raw_docstring(cls):
        raise NotImplementedError()
