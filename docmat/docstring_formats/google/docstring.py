from textwrap import dedent
from typing import Any, Callable, List

from docmat.docstring_formats.shared import (
    BaseFormatter,
    IndentedSection,
    Summary,
    UnindentedSection,
)
from docmat.docstring_formats.shared.string_utils import (
    count_indentation_level,
    is_start_of_indented_section,
)


def flatten(list_of_lists: List[List[Any]]) -> List[Any]:
    """Fatten a list of lists of items into a single list of items.

    Args:
        list_of_lists (List[List[Any]]): nested list of lists.

    Returns:
        List[Any]: flattend list of items.
    """
    return sum(list_of_lists, [])


class GoogleFormatter(BaseFormatter):
    def __init__(
        self,
        docstring_lines: List[str],
        line_length: int = 88,
        wrap_summary: bool = False,
    ) -> None:
        """Class Constructor.

        Args:
            docstring_lines (List[str]): docstring lines to format.
            line_length (int): maximum line length. Defaults to 88.
            wrap_summary (bool): whether to wrap the summary line. Defaults to False.
        """
        super().__init__()
        self._delimiter = self.get_docstring_delimiter(docstring_lines[0])
        self._indentation = self.get_indentation(docstring_lines[0], self._delimiter)
        self._dedented_lines = self.dedent_lines(docstring_lines)
        self._line_length = line_length
        summary_starts, summary_ends = self.find_summary(self._dedented_lines)
        self._elements = [
            Summary(
                " ".join(self._dedented_lines[summary_starts:summary_ends]),
                should_wrap=wrap_summary,
                line_length=line_length - len(self._indentation),
                delimiter=self._delimiter,
            )
        ]
        self._elements += list(self.iter_elements(summary_ends))

    def find_offset(self, from_offset: int, condition: Callable[[str], bool]) -> int:
        """Find the next offset that satisfies a condition.

        If no offset that satisfy the condition could be found, return the last offset.

        Args:
            from_offset (int): offset from which to start looking.
            condition (Callable[[str], bool]): condition to check.

        Returns:
            int: offset that satisfies the condition or last offset.
        """
        for i, line in enumerate(self._dedented_lines[from_offset:]):
            if condition(line) or line == self._delimiter:
                break
        return from_offset + i

    def iter_elements(self, offset):
        lines = self._dedented_lines

        def find_end_of_indented_section(offset):
            section_title = lines[offset]
            if len(lines) > offset:
                first_line_idx = self.find_offset(offset + 1, bool)
                first_line = lines[first_line_idx]
                title_indentation_level = count_indentation_level(section_title)
                first_line_indentation_level = count_indentation_level(first_line)
                if title_indentation_level == first_line_indentation_level:
                    # Scroll until you meet an empty line, this is the case
                    # Title:
                    # Wrongly indented section
                    # Wrongly indented section
                    #
                    # Other section
                    return self.find_offset(first_line_idx, lambda line: not line)
                if title_indentation_level < first_line_indentation_level:
                    # Scroll until the indentation level is the same as the title
                    # matches the case:
                    # Title:
                    #     Properly indented section
                    #     Properly indented section
                    # Other section
                    return self.find_offset(
                        first_line_idx,
                        lambda line: line
                        and count_indentation_level(line) <= title_indentation_level,
                    )
            return offset

        def find_end_of_unindented_section(offset):
            for i, line in enumerate(lines[offset:]):
                if (
                    line == ""
                    or line == self._delimiter
                    or is_start_of_indented_section(line)
                ):
                    return i + offset
            return i + offset

        def next_start_element(offset):
            for i, line in enumerate(lines[offset:]):
                if line and line != self._delimiter:
                    return i + offset
            return None

        start = next_start_element(offset)
        while start is not None:
            if is_start_of_indented_section(lines[start]):
                end = find_end_of_indented_section(start)
                yield IndentedSection(
                    lines[start:end], self._line_length - len(self._indentation)
                )
            else:
                end = find_end_of_unindented_section(start)
                yield UnindentedSection(
                    lines[start:end], self._line_length - len(self._indentation)
                )
            offset = end
            start = next_start_element(offset)

    def find_summary(self, lines):
        summary_starts = None
        for i, line in enumerate(lines):
            if line.strip() == self._delimiter and summary_starts is None:
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
        return "\n".join(self.get_formatted_docstring()) + "\n"

    def get_formatted_docstring(self):
        if self._doc_fits_in_one_line():
            text_to_indent = [f"{self._elements[0]}{self._delimiter}"]
        else:
            text_to_indent = []
            for el in self._elements[:-1]:
                text_to_indent += el.lines
                text_to_indent += [""]
            text_to_indent += self._elements[-1].lines
            text_to_indent += [self._delimiter]
        return self._indent_lines(text_to_indent)
