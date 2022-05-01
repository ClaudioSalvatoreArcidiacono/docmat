import argparse
import fnmatch
import glob
import os
from pathlib import Path

from docmat.file import FileHandler
from docmat.google_format.docstring import GoogleFormatter

ARGS_DEFAULT = {
    "line_length": 88,
    "wrap_summary": False,
}


def parse_args() -> argparse.Namespace:
    """Parse Command line arguments.

    Returns:
        argparse.Namespace: Namespace containing the parsed arguments.
    """

    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument(
        "files",
        type=str,
        nargs="+",
        help="File(s) to format",
    )

    parser.add_argument(
        "--line-length",
        dest="line_length",
        type=int,
        default=ARGS_DEFAULT["line_length"],
        help="Maximum line length",
    )

    parser.add_argument(
        "--wrap-summary",
        dest="wrap_summary",
        action="store_true",
        default=ARGS_DEFAULT["wrap_summary"],
        help="Whether to wrap the summary line so it will fit within the maximum line "
        "length",
    )

    args = parser.parse_args()
    return args


def format_file(handler: FileHandler, line_length: int, wrap_summary: bool):
    """Format a file using the docstring formatter.

    Args:
        handler (FileHandler): file handler to be used to iterate over docstring lines
            and to save the formatted code.
        line_length (int): maximum line length.
        wrap_summary (bool): whether to wrap the summary line.
    """
    for (
        initial_start_offset,
        initial_end_offset,
        docstring_lines,
    ) in handler.iter_doc():
        docstring_lines_formatted = GoogleFormatter(
            docstring_lines, line_length=line_length, wrap_summary=wrap_summary
        ).format()
        handler.replace_lines(
            docstring_lines_formatted, initial_start_offset, initial_end_offset
        )


def main():
    """Format each file passed from CLI."""
    args = parse_args()
    line_length = args.line_length
    wrap_summary = args.wrap_summary
    for file_glob in args.files:
        if os.path.isdir(file_glob):
            for file in Path(file_glob).rglob("*.py"):
                handler = FileHandler(str(file))
                format_file(handler, line_length, wrap_summary)
                handler.write_formatted_file()
        else:
            for file in glob.glob(file_glob):
                if fnmatch.fnmatch(file, "*.py"):
                    handler = FileHandler(file)
                    format_file(handler, line_length, wrap_summary)
                    handler.write_formatted_file()
