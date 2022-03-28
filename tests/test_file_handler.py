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
        (12, ['        """Iterate over blocks of docstring"""']),
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
        (12, ['        """Iterate over blocks', '        of docstring"""']),
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
        (8, ['    """Iterate over blocks', '        of docstring"""']),
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
        (1, ['"""Iterate over blocks', '    of docstring"""']),
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
        (1, ['"""Test a blank line', "", '    of docstring"""']),
    ),
]


@pytest.mark.parametrize(
    ["document_content", "expected_outcome"],
    TEST_INPUTS,
)
def test_iter_doc(document_content, expected_outcome, tmp_path):
    test_file = tmp_path / "test"
    test_file.write_text(document_content)

    assert FileHandler(test_file).iter_doc() == [expected_outcome]


def test_iter_doc_empty_file(tmp_path):
    test_file = tmp_path / "test"
    test_file.touch()
    assert FileHandler(test_file).iter_doc() == []


@pytest.mark.parametrize(
    ["init_lines", "replace_params", "expected"],
    [
        (
            ["a", "b", "c", "d"],
            [{"old_lines": ["b"], "new_lines": ["foo"], "offset": 1}],
            ["a", "foo", "c", "d"],
        ),
        (
            ["a", "b", "c", "d"],
            [
                {"old_lines": ["b"], "new_lines": ["foo", "bar"], "offset": 1},
                {"old_lines": ["c"], "new_lines": ["fizz"], "offset": 2},
            ],
            ["a", "foo", "bar", "fizz", "d"],
        ),
        (
            ["a", "b", "c", "d"],
            [
                {"old_lines": ["b"], "new_lines": ["foo", "bar", "rat"], "offset": 1},
                {"old_lines": ["c", "d"], "new_lines": ["fizz", "yyy"], "offset": 2},
            ],
            ["a", "foo", "bar", "rat", "fizz", "yyy"],
        ),
        (
            ["a", "b", "|", "c", "d"],
            [
                {
                    "old_lines": ["a", "b"],
                    "new_lines": ["foo"],
                    "offset": 0,
                },
                {"old_lines": ["c", "d"], "new_lines": ["fizz"], "offset": 3},
            ],
            [
                "foo",
                "|",
                "fizz",
            ],
        ),
    ],
)
def test_replace_lines(tmp_path, init_lines, replace_params, expected):
    test_file = tmp_path / "test"
    test_file.write_text("\n".join(init_lines))
    handler = FileHandler(test_file)
    for param in replace_params:
        handler.replace_lines(**param)
    assert handler.formatted_file_content == "\n".join(expected)


def test_write_file(tmp_path):
    test_file = tmp_path / "test"
    test_file.write_text("\n".join(["a", "b", "c"]))
    handler = FileHandler(test_file)
    handler.replace_lines(["b"], ["foo"], 1)
    handler.write_formatted_file()
    assert test_file.read_text() == "\n".join(["a", "foo", "c"])
