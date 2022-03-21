import re
from textwrap import dedent
from typing import List

from docmat.docstring_formats.shared import BaseDocstring, Summary, TextBlock
from docmat.docstring_formats.shared.elements import NewLine
from docmat.docstring_formats.shared.string_utils import is_start_of_section


def flatten(t):
    return [item for sublist in t for item in sublist]


class GoogleDocString(BaseDocstring):
    def __init__(
        self, docstring_lines: List[str], wrap_summary=True, line_length=88
    ) -> None:
        super().__init__()
        self._delimiter = self.get_docstring_delimiter(docstring_lines[0])
        self._indentation = self.get_indentation(docstring_lines[0], self._delimiter)
        dedented_lines = self.dedent_lines(docstring_lines)
        summary_starts, summary_ends = self.find_summary(dedented_lines)
        self._elements = [
            Summary(
                " ".join(dedented_lines[summary_starts:summary_ends]),
                should_wrap=wrap_summary,
                line_length=line_length - len(self._indentation),
                delimiter=self._delimiter,
            )
        ]
        text_blocks_idxs = self.find_text_blocks(
            dedented_lines, self._delimiter, offset=summary_ends
        )
        for start, end in text_blocks_idxs:
            self._elements.append(NewLine())
            self._elements.append(
                TextBlock(
                    " ".join(dedented_lines[start:end]),
                    line_length=line_length - len(self._indentation),
                )
            )
        self._line_length = line_length

    @staticmethod
    def find_text_blocks(lines, delimiter, offset):
        def find_next_block(lines):
            block_starts = None
            for i, line in enumerate(lines):
                if is_start_of_section(line):
                    if block_starts is not None:
                        return block_starts, i
                if line == delimiter or is_start_of_section(line):
                    if block_starts is not None:
                        return block_starts, i
                    else:
                        return None
                if line and block_starts is None:
                    block_starts = i
                if not line and block_starts is not None:
                    return block_starts, i
            return None

        text_blocks = []
        next_block = find_next_block(lines[offset:])
        while next_block:
            start, end = next_block
            start, end = start + offset, end + offset
            text_blocks.append((start, end))
            offset = end + 1
            next_block = find_next_block(lines[offset:])
        return text_blocks

    def find_summary(self, lines):
        summary_starts = None
        for i, line in enumerate(lines):
            if line == self._delimiter and summary_starts is None:
                continue
            if line:
                if summary_starts is None:
                    summary_starts = i
            if (
                # Line finishes with a dot
                line.endswith(".")
                # Meet a new line while parsing summary
                or (not line and summary_starts is not None)
                # Line finishes with the delimiter while parsing summary
                or line.endswith(self._delimiter)
            ):
                return summary_starts, i + 1

    @staticmethod
    def dedent_lines(docstring_lines):
        dedented_lines = dedent("\n".join(docstring_lines)).split("\n")
        return [line.rstrip() for line in dedented_lines]

    @staticmethod
    def get_docstring_delimiter(line):
        stripped_line = line.strip()
        docstring_delimiters = ('"""', "'''")
        for delimiter in docstring_delimiters:
            if stripped_line.startswith(delimiter):
                return delimiter
        raise RuntimeError(
            f'"{line}" does not start with any of these docstring '
            f"delimiters {docstring_delimiters}"
        )

    @staticmethod
    def get_indentation(line, docstring_delimiter):
        return line.split(docstring_delimiter)[0]

    def _doc_fits_in_one_line(self):
        summary = self._elements[0]
        return (
            len(self._elements) == 1
            and len(summary.lines) == 1
            and len(str(summary)) + len(self._delimiter) + len(self._indentation)
            <= self._line_length
        )

    def _indent_lines(self, lines):
        return [self._indentation + line if line else line for line in lines]

    def __str__(self) -> str:
        if self._doc_fits_in_one_line():
            text_to_indent = [f"{self._elements[0]}{self._delimiter}"]
        else:
            text_to_indent = [
                *flatten([el.lines for el in self._elements]),
                self._delimiter,
            ]
        return "\n".join(self._indent_lines(text_to_indent)) + "\n"
