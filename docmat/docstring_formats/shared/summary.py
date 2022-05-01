import re
from textwrap import wrap

from .string_utils import capitalize, check_dot, count_indentation_level


def replace_double_spaces(s):
    return re.sub(r" +", " ", s)


def strip_all(l):
    return [s.strip() for s in l]


def clean_text(text):
    for delimiter in ('"""', "'''"):
        if text.startswith(delimiter):
            text = text[len(delimiter) :]

        if text.endswith(delimiter):
            text = text[: -len(delimiter)]
    text = text.rstrip()
    text = replace_double_spaces(text)
    return capitalize(check_dot(text))


class Summary:
    def __init__(
        self,
        summary,
        delimiter,
        should_wrap=False,
        line_length=None,
    ) -> None:
        self.raw_summary_lines = summary
        self.delimiter = delimiter
        self.should_wrap = should_wrap
        self.line_length = line_length

    def format(self):
        raw_summary = " ".join(self.raw_summary_lines)
        clean_summary = clean_text(raw_summary)
        clean_summary = self.delimiter + clean_summary
        if self.should_wrap:
            return wrap(clean_summary, width=self.line_length)
        else:
            return [clean_summary]

    def __str__(self) -> str:
        return "\n".join(self.format())

    @classmethod
    def find_start_end_summary(cls, lines, delimiter):
        summary_starts = None
        for i, line in enumerate(lines):
            if line.strip() == delimiter and summary_starts is None:
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
                or line.endswith(delimiter)
            ):
                return summary_starts, i + 1

    @classmethod
    def from_raw_docstring(cls, lines, delimiter, should_wrap, line_length):
        start_offset, end_offset = cls.find_start_end_summary(lines, delimiter)
        return (
            cls(
                lines[start_offset:end_offset],
                delimiter=delimiter,
                should_wrap=should_wrap,
                line_length=line_length,
            ),
            end_offset,
        )
