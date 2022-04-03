import ast
from collections import namedtuple
from pathlib import Path
from typing import List

OffsetShift = namedtuple("OffsetShift", ["offset", "shift"])


class FileHandler:
    """Handle file I/O operations."""

    def __init__(self, path: str) -> None:
        """Class constructor.

        Args:
            path (str): file path.
        """
        self._file = Path(path)
        self._initial_file_content = self._file.read_text()
        self._file_lines = self._initial_file_content.split("\n")
        self._offset_shifts = []

    @property
    def formatted_file_content(self):
        return "\n".join(self._file_lines)

    def iter_doc(self):
        """Iterate over blocks of docstring."""
        for element in ast.walk(ast.parse(self._initial_file_content)):
            if type(element) in (
                ast.AsyncFunctionDef,
                ast.FunctionDef,
                ast.ClassDef,
                ast.Module,
            ):
                if docstring_text := ast.get_docstring(element):
                    docstring = element.body[0]
                    start = docstring.lineno - 1
                    # end_lineno attribute not available in python 3.7
                    length_docstring = len(docstring_text.split("\n"))
                    end = start + length_docstring
                    if self._file_lines[end - 1].strip()[-3:] in ('"""', "'''"):
                        yield start, self._file_lines[start:end]
                    else:
                        yield start, self._file_lines[start : end + 1]

    def _calculate_new_file_offset(self, file_offset: int):
        for offset_shift in self._offset_shifts:
            if file_offset >= offset_shift.offset:
                file_offset += offset_shift.shift
        return file_offset

    def _append_offset_shift(
        self, old_lines: List[str], new_lines: List[str], offset: int
    ):
        shift = len(new_lines) - len(old_lines)
        if shift != 0:
            self._offset_shifts.append(OffsetShift(offset + len(old_lines), shift))

    def replace_lines(self, old_lines: List[str], new_lines: List[str], offset: int):
        """Replace lines of the file.

        Args:
            old_lines (List[str]): old lines to be replaced.
            new_lines (List[str]): new lines to replace the old one.
            offset (int): File offset (aka line number) where the old lines began in the
                original file content.
        """
        file_offset_start = self._calculate_new_file_offset(offset)
        file_offset_end = file_offset_start + len(old_lines)
        self._file_lines = (
            self._file_lines[:file_offset_start]
            + new_lines
            + self._file_lines[file_offset_end:]
        )
        self._append_offset_shift(old_lines, new_lines, file_offset_start)

    def write_formatted_file(self):
        """Overwrite the original file with the formatted file content."""
        self._file.write_text(self.formatted_file_content)
