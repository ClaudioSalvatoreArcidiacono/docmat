import ast
from collections import namedtuple
from pathlib import Path
from typing import List

OffsetShift = namedtuple("OffsetShift", ["offset", "shift"])


class FileHandler:
    def __init__(self, path: str) -> None:
        self._file = Path(path)
        self._initial_file_content = self._file.read_text()
        self._file_lines = self._initial_file_content.split("\n")
        self._offset_shifts = []

    @property
    def formatted_file_content(self):
        return "\n".join(self._file_lines)

    def iter_doc(self):
        """Iterate over blocks of docstring."""

        def recurse_yield(element):
            if element.body and type(element.body[0]) is ast.Expr:
                expression = element.body[0]
                start = expression.lineno - 1
                end = expression.end_lineno
                expression_lines = self._file_lines[start:end]
                for docstring_separator in ('"""', "'''"):
                    if expression_lines[0].strip().startswith(
                        docstring_separator
                    ) and expression_lines[-1].strip().endswith(docstring_separator):
                        yield start, expression_lines
            for sub_element in element.body:
                if type(sub_element) in (ast.ClassDef, ast.FunctionDef):
                    yield from recurse_yield(sub_element)

        return list(recurse_yield(ast.parse(self._initial_file_content)))

    def _calculate_new_file_offset(self, file_offset):
        for offset_shift in self._offset_shifts:
            if file_offset >= offset_shift.offset:
                file_offset += offset_shift.shift
        return file_offset

    def _append_offset_shift(self, old_lines, new_lines, offset):
        shift = len(new_lines) - len(old_lines)
        if shift != 0:
            self._offset_shifts.append(OffsetShift(offset + len(old_lines), shift))

    def replace_lines(self, old_lines, new_lines, offset):
        file_offset_start = self._calculate_new_file_offset(offset)
        file_offset_end = file_offset_start + len(old_lines)
        self._file_lines = (
            self._file_lines[:file_offset_start]
            + new_lines
            + self._file_lines[file_offset_end:]
        )
        self._append_offset_shift(old_lines, new_lines, file_offset_start)

    def write_formatted_file(self):
        self._file.write_text(self.formatted_file_content)
