from abc import ABC, abstractclassmethod, abstractmethod, abstractstaticmethod
from functools import partial

from docmat.string_utils import remove_delimiter


class BaseElement(ABC):
    def __init__(self, raw_lines, delimiter, line_length) -> None:
        self.raw_lines = raw_lines
        self.delimiter = delimiter
        self.line_length = line_length

    @staticmethod
    def find_start_offset(lines, delimiter):
        lines = map(lambda l: l.rstrip(), lines)
        lines = map(partial(remove_delimiter, delimiter=delimiter), lines)
        lines = map(lambda l: l.rstrip(), lines)
        for i, line in enumerate(lines):
            if line:
                return i

    @abstractclassmethod
    def from_raw_docstring(cls, lines, delimiter, line_length):
        raise NotImplementedError()

    @abstractstaticmethod
    def find_end_offset(lines, start_offset, delimiter):
        raise NotImplementedError()

    @abstractmethod
    def format(self):
        raise NotImplementedError()
