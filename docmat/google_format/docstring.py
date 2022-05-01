from textwrap import dedent

from docmat.google_format.other import NewLine
from docmat.google_format.section import IndentedSection, UnindentedSection
from docmat.google_format.summary import Summary


class GoogleFormatter:
    possible_subsections = [IndentedSection, UnindentedSection]

    def __init__(self, docstring_lines, line_length, wrap_summary) -> None:
        self.line_length = line_length
        self.wrap_summary = wrap_summary
        self.dedented_lines = self.dedent_lines(docstring_lines)
        self.delimiter = self.get_docstring_delimiter(self.dedented_lines[0])
        self._indentation = self.get_indentation(docstring_lines[0], self.delimiter)
        self.sections = self.parse_sections()

    @staticmethod
    def get_indentation(line, docstring_delimiter):
        return line.split(docstring_delimiter)[0]

    def parse_sections(self):
        sections = []
        summary, end_summary_offset = Summary.from_raw_docstring(
            self.dedented_lines,
            delimiter=self.delimiter,
            should_wrap=self.wrap_summary,
            line_length=self.line_length - len(self._indentation),
        )
        if summary:
            sections.append(summary)
            left_to_parse = self.dedented_lines[end_summary_offset:]
            assigned = True
            while left_to_parse and assigned:
                assigned = False
                for possible_section in self.possible_subsections:  # TODO
                    if possible_section.is_start_of_section(
                        left_to_parse, self.delimiter
                    ):  # TODO
                        (
                            section,
                            end_section_offset,
                        ) = possible_section.from_raw_docstring(  # TODO
                            left_to_parse,
                            self.delimiter,
                            line_length=self.line_length - len(self._indentation),
                        )
                        sections.append(section)
                        left_to_parse = left_to_parse[end_section_offset:]
                        assigned = True
                        break
        else:
            sections.append(NewLine())
        return sections

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

    def _doc_fits_in_one_line(self):
        summary = self.sections[0]
        return (
            len(self.sections) == 1
            and len(summary.format()) == 1
            and len(str(summary)) + len(self.delimiter) + len(self._indentation)
            <= self.line_length
        )

    def _indent_lines(self, lines):
        return [self._indentation + line if line else line for line in lines]

    def format(self):
        if self._doc_fits_in_one_line():
            text_to_indent = [f"{self.sections[0].format()[0]}{self.delimiter}"]
        else:
            text_to_indent = []
            for el in self.sections[:-1]:
                text_to_indent += el.format()
                text_to_indent += [""]
            text_to_indent += self.sections[-1].format()
            text_to_indent += [self.delimiter]
        return self._indent_lines(text_to_indent)
