from pathlib import Path
from typing import List
import re
import ast


class FileHandler:
    def __init__(self, path: str) -> None:
        self._file = Path(path)
        self._file_content = self._file.read_text()

    def iter_doc(self):
        """Iterate over blocks of docstring."""

        def recurse_yield(element):
            if element.body and type(element.body[0]) is ast.Expr:
                expression = element.body[0]
                expression_lines = self._file_content.split("\n")[
                    expression.lineno - 1 : expression.end_lineno
                ]
                for docstring_separator in ('"""', "'''"):
                    if expression_lines[0].strip().startswith(
                        docstring_separator
                    ) and expression_lines[-1].strip().endswith(docstring_separator):
                        yield expression_lines
            for sub_element in element.body:
                if type(sub_element) in (ast.ClassDef, ast.FunctionDef):
                    yield from recurse_yield(sub_element)

        yield from recurse_yield(ast.parse(self._file_content))
