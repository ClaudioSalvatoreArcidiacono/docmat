from functools import partial
from textwrap import wrap

from docmat.google_format.base import BaseElement
from docmat.string_utils import (
    capitalize,
    check_dot,
    remove_delimiter,
    replace_double_spaces,
)


class Summary(BaseElement):
    def __init__(
        self,
        lines,
        delimiter,
        should_wrap=False,
        line_length=None,
    ) -> None:
        super().__init__(lines, delimiter=delimiter, line_length=line_length)
        self.should_wrap = should_wrap

    def format(self):
        summary_text = " ".join(self.raw_lines)
        summary_text = summary_text.rstrip()
        summary_text = remove_delimiter(summary_text, self.delimiter)
        summary_text = summary_text.rstrip()
        summary_text = replace_double_spaces(summary_text)
        summary_text = check_dot(summary_text)
        summary_text = capitalize(summary_text)
        clean_summary = self.delimiter + summary_text
        if self.should_wrap:
            return wrap(clean_summary, width=self.line_length)
        else:
            return [clean_summary]


    @staticmethod
    def find_end_offset(lines, start_offset, delimiter):
        lines = list(map(lambda l: l.rstrip(), lines))
        for i, line in enumerate(lines[start_offset:], start=start_offset):
            if (
                # Line finishes with a dot
                line.endswith(".")
                # Meet a new line while parsing summary
                or not line
                # Line finishes with the delimiter while parsing summary
                or line.endswith(delimiter)
            ):
                return i + 1

    @classmethod
    def from_raw_docstring(cls, lines, delimiter, should_wrap, line_length):
        start_offset = cls.find_start_offset(lines, delimiter=delimiter)
        if start_offset is not None:
            end_offset = cls.find_end_offset(
                lines, start_offset=start_offset, delimiter=delimiter
            )
            return (
                cls(
                    lines[start_offset:end_offset],
                    delimiter=delimiter,
                    should_wrap=should_wrap,
                    line_length=line_length,
                ),
                end_offset,
            )
        else:
            return None, None
