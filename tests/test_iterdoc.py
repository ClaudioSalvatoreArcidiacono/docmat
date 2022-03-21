import pytest
from docmat.file import FileHandler

TEST_INPUTS = [
    (
        """from pathlib import Path
from typing import List
import re
import ast


class FileHandler:
    def __init__(self, path: str) -> None:
        self._file = Path(path)
        self._file_content = self._file.read_text()

    def iter_doc(self):
        \"\"\"Iterate over blocks of docstring\"\"\"
        def recurse_yield(element):
            if type(element.body[0] is ast.Expr):
                expression = element.body[0]
                expression_code_lines = self._file_content.split("\\n")[
                    expression.lineno : expression.end_lineno
                ]
                expression_code = "\\n".join([l.strip() for l in expression_code_lines])
                for sub_element in element.body:
                    if type(sub_element) in (ast.ClassDef, ast.FunctionDef):
                        yield from recurse_yield(sub_element)

        yield from recurse_yield(ast.parse(self._file_content))""",
        ['        """Iterate over blocks of docstring"""'],
    ),
    (
        """from pathlib import Path
from typing import List
import re
import ast


class FileHandler:
    def __init__(self, path: str) -> None:
        self._file = Path(path)
        self._file_content = self._file.read_text()

    def iter_doc(self):
        \"\"\"Iterate over blocks
        of docstring\"\"\"
        def recurse_yield(element):
            if type(element.body[0] is ast.Expr):
                expression = element.body[0]
                expression_code_lines = self._file_content.split("\\n")[
                    expression.lineno : expression.end_lineno
                ]
                expression_code = "\\n".join([l.strip() for l in expression_code_lines])
                for sub_element in element.body:
                    if type(sub_element) in (ast.ClassDef, ast.FunctionDef):
                        yield from recurse_yield(sub_element)

        yield from recurse_yield(ast.parse(self._file_content))""",
        ['        """Iterate over blocks', '        of docstring"""'],
    ),
    (
        """# utf-8
from pathlib import Path
from typing import List
import re
import ast


class FileHandler:
    \"\"\"Iterate over blocks
        of docstring\"\"\"
    def __init__(self, path: str) -> None:
        self._file = Path(path)
        self._file_content = self._file.read_text()

    def iter_doc(self):
        def recurse_yield(element):
            if type(element.body[0] is ast.Expr):
                expression = element.body[0]
                expression_code_lines = self._file_content.split("\\n")[
                    expression.lineno : expression.end_lineno
                ]
                expression_code = "\\n".join([l.strip() for l in expression_code_lines])
                for sub_element in element.body:
                    if type(sub_element) in (ast.ClassDef, ast.FunctionDef):
                        yield from recurse_yield(sub_element)

        yield from recurse_yield(ast.parse(self._file_content))""",
        ['    """Iterate over blocks', '        of docstring"""'],
    ),
    (
        """# utf-8
\"\"\"Iterate over blocks
    of docstring\"\"\"
from pathlib import Path
from typing import List
import re
import ast


class FileHandler:
    def __init__(self, path: str) -> None:
        self._file = Path(path)
        self._file_content = self._file.read_text()

    def iter_doc(self):
        def recurse_yield(element):
            if type(element.body[0] is ast.Expr):
                expression = element.body[0]
                expression_code_lines = self._file_content.split("\\n")[
                    expression.lineno : expression.end_lineno
                ]
                expression_code = "\\n".join([l.strip() for l in expression_code_lines])
                for sub_element in element.body:
                    if type(sub_element) in (ast.ClassDef, ast.FunctionDef):
                        yield from recurse_yield(sub_element)

        yield from recurse_yield(ast.parse(self._file_content))""",
        ['"""Iterate over blocks', '    of docstring"""'],
    ),
    (
        """# utf-8
\"\"\"Test a blank line

    of docstring\"\"\"
from pathlib import Path
from typing import List
import re
import ast


class FileHandler:
    def __init__(self, path: str) -> None:
        self._file = Path(path)
        self._file_content = self._file.read_text()

    def iter_doc(self):
        def recurse_yield(element):
            if type(element.body[0] is ast.Expr):
                expression = element.body[0]
                expression_code_lines = self._file_content.split("\\n")[
                    expression.lineno : expression.end_lineno
                ]
                expression_code = "\\n".join([l.strip() for l in expression_code_lines])
                for sub_element in element.body:
                    if type(sub_element) in (ast.ClassDef, ast.FunctionDef):
                        yield from recurse_yield(sub_element)

        yield from recurse_yield(ast.parse(self._file_content))""",
        ['"""Test a blank line', "", '    of docstring"""'],
    ),
]


@pytest.mark.parametrize(
    ["document_content", "expected_outcome"],
    TEST_INPUTS,
)
def test_iter_doc(document_content, expected_outcome, tmp_path):
    test_file = tmp_path / "test"
    test_file.write_text(document_content)

    assert next(FileHandler(test_file).iter_doc()) == expected_outcome


def test_iter_doc_empty_file(tmp_path):
    test_file = tmp_path / "test"
    test_file.touch()
    with pytest.raises(StopIteration):
        next(FileHandler(test_file).iter_doc())
