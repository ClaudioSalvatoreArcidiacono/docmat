import argparse
import glob

from docmat.docstring_formats.google import GoogleDocString
from docmat.file import FileHandler


def parse_args():

    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument(
        "files",
        type=str,
        nargs="+",
        help="Files to format",
    )

    parser.add_argument(
        "--line-length",
        dest="line_length",
        type=int,
        default=88,
        help="maximum line length",
    )

    args = parser.parse_args()
    return args


def format_file(file, line_length):
    handler = FileHandler(file)
    for offset, docstring_lines in handler.iter_doc():
        docstring_lines_formatted = GoogleDocString(
            docstring_lines, line_length=line_length
        ).get_formatted_docstring()
        handler.replace_lines(docstring_lines, docstring_lines_formatted, offset)
    handler.write_formatted_file()


def main():
    args = parse_args()
    line_length = args.line_length
    for file_glob in args.files:
        for file in glob.glob(file_glob):
            format_file(file, line_length)
