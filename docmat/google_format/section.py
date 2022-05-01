import re
from textwrap import wrap

from docmat.google_format.base import BaseElement
from docmat.string_utils import (
    capitalize,
    check_dot,
    count_indentation_level,
    remove_delimiter,
    replace_double_spaces,
    strip_all,
)


class UnindentedSection(BaseElement):
    def format(self):
        text = " ".join(self.raw_lines)
        text = text.rstrip()
        text = remove_delimiter(text, self.delimiter)
        text = text.rstrip()
        text = replace_double_spaces(text)
        text = check_dot(text)
        text = capitalize(text)

        return wrap(text, width=self.line_length)

    @staticmethod
    def find_end_offset(lines, start_offset, delimiter):
        lines = list(map(lambda l: l.rstrip(), lines))
        for i, line in enumerate(lines[start_offset:], start=start_offset):
            if (
                # Meet a new line
                not line
                # Line finishes with the delimiter while parsing summary
                or line.endswith(delimiter)
                or IndentedSection.is_start_of_indented_section(line)
            ):
                return i + 1

    @staticmethod
    def is_start_of_section(lines, delimiter):
        return UnindentedSection.find_start_offset(lines, delimiter) is not None

    @classmethod
    def from_raw_docstring(cls, lines, delimiter, line_length):
        start_offset = cls.find_start_offset(lines, delimiter)

        if start_offset is not None:
            end_offset = cls.find_end_offset(
                lines, start_offset=start_offset, delimiter=delimiter
            )
            return (
                cls(
                    lines[start_offset:end_offset],
                    delimiter=delimiter,
                    line_length=line_length,
                ),
                end_offset,
            )
        else:
            return None, None


class IndentedSection(BaseElement):
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

    def format(self):
        lines = [l.rstrip() for l in self.raw_lines]
        section_title = capitalize(lines[0].strip())
        start_body = self._find_start_body(lines)
        body_sections_lines = list(self.split_body_into_sections(lines, start_body))

        formatted_lines = [section_title]
        if section_title.endswith("::"):
            formatted_lines += [""]

        for section_lines in body_sections_lines:
            section_text = replace_double_spaces(
                check_dot(" ".join(strip_all(section_lines)))
            )
            formatted_lines += wrap(
                section_text,
                self.line_length,
                initial_indent=" " * 4,
                subsequent_indent=" " * 8,
            )
        return formatted_lines

    @staticmethod
    def get_section_name(line):
        match = re.match(r"^([^\n\:]+)\:\:?$", line)
        if match:
            return match.group(1)
        else:
            return None

    @staticmethod
    def is_start_of_indented_section(line):
        return bool(IndentedSection.get_section_name(line))

    @staticmethod
    def is_start_of_section(lines, delimiter):
        start_offset = IndentedSection.find_start_offset(lines, delimiter)
        if start_offset is not None:
            return IndentedSection.is_start_of_indented_section(lines[start_offset])
        else:
            return False

    @staticmethod
    def find_end_offset_wrongly_indented_section(lines, start_offset, delimiter):
        lines = list(map(lambda l: l.rstrip(), lines))
        for i, line in enumerate(lines[start_offset:], start=start_offset):
            if (
                # Meet a new line
                not line
                # Line finishes with the delimiter while parsing summary
                or line.endswith(delimiter)
                or IndentedSection.is_start_of_indented_section(line)
            ):
                return i + 1

    @staticmethod
    def find_end_offset_properly_indented_section(
        lines, start_offset, delimiter, initial_indentation_level
    ):
        lines = list(map(lambda l: l.rstrip(), lines))
        for i, line in enumerate(lines[start_offset:], start=start_offset):
            if (
                line.endswith(delimiter)
                or IndentedSection.is_start_of_indented_section(line)
                or bool(line)
                and count_indentation_level(line) >= initial_indentation_level
            ):
                return i + 1

    @staticmethod
    def find_end_offset(lines, start_offset, delimiter):
        section_title = lines[start_offset]
        if len(lines) > start_offset:
            first_line_idx = start_offset + IndentedSection.find_start_offset(
                lines[start_offset:], delimiter
            )
            if first_line_idx:
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
                    return IndentedSection.find_end_offset_wrongly_indented_section(
                        lines, first_line_idx, delimiter=delimiter
                    )
                if title_indentation_level < first_line_indentation_level:
                    # Scroll until the indentation level is the same as the title
                    # matches the case:
                    # Title:
                    #     Properly indented section
                    #     Properly indented section
                    # Other section
                    return IndentedSection.find_end_offset_wrongly_indented_section(
                        lines,
                        first_line_idx,
                        delimiter=delimiter,
                        initial_indentation_level=title_indentation_level,
                    )

        return start_offset + 1
    @classmethod
    def from_raw_docstring(cls, lines, delimiter, line_length):
        start_offset = cls.find_start_offset(lines, delimiter)

        if start_offset is not None:
            end_offset = cls.find_end_offset(
                lines, start_offset=start_offset, delimiter=delimiter
            )
            return (
                cls(
                    lines[start_offset:end_offset],
                    delimiter=delimiter,
                    line_length=line_length,
                ),
                end_offset,
            )
        else:
            return None, None
