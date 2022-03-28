import re
from textwrap import TextWrapper

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
        clean_summary = clean_text(summary)
        clean_summary = delimiter + clean_summary
        if should_wrap:
            self.lines = TextWrapper(line_length).wrap(clean_summary)
        else:
            self.lines = [clean_summary]

    def __str__(self) -> str:
        return "\n".join(self.lines)


class NewLine:
    def __init__(self) -> None:
        self.lines = [""]

    def __str__(self) -> str:
        return ""


class UnindentedSection:
    def __init__(self, raw_lines, line_length) -> None:
        text = " ".join(l.strip() for l in raw_lines)
        cleaned_text = clean_text(text)
        self.lines = TextWrapper(line_length).wrap(cleaned_text)

    def __str__(self) -> str:
        return "\n".join(self.lines) + "\n"

    def __repr__(self) -> str:
        return f"UnindentedSection({str(self)})"

    def __eq__(self, __o: object) -> bool:
        return str(self) == str(__o)


class IndentedSection:
    @staticmethod
    def _find_start_body(lines):
        for i, line in enumerate(lines[1:]):
            if line != "":
                return i + 1

    @staticmethod
    def split_body_into_sections(lines, offset):
        def next_start_element(offset):
            for i, line in enumerate(lines[offset:]):
                if line:
                    return i + offset
            return None

        def find_end_of_section(offset):
            init_indentation_level = count_indentation_level(lines[offset])
            offset += 1
            if len(lines) > offset:
                for i, line in enumerate(lines[offset:]):
                    if count_indentation_level(line) <= init_indentation_level:
                        return i + offset
                return i + offset + 1
            return offset

        start = next_start_element(offset)
        while start is not None:
            end = find_end_of_section(start)
            yield lines[start:end]
            offset = end
            start = next_start_element(offset)

    def __init__(self, raw_lines, line_length) -> None:

        lines = [l.rstrip() for l in raw_lines]
        section_title = capitalize(lines[0].strip())
        start_body = self._find_start_body(lines)
        body_sections_lines = list(self.split_body_into_sections(lines, start_body))

        self.lines = [section_title]
        if section_title.endswith("::"):
            self.lines += [""]

        for section_lines in body_sections_lines:
            section_text = replace_double_spaces(
                check_dot(" ".join(strip_all(section_lines)))
            )
            self.lines += TextWrapper(
                line_length, initial_indent=" " * 4, subsequent_indent=" " * 8
            ).wrap(section_text)

    def __str__(self) -> str:
        return "\n".join(self.lines) + "\n"

    def __repr__(self) -> str:
        return f"IndentedSection({str(self)})"

    def __eq__(self, __o: object) -> bool:
        return str(self) == str(__o)
