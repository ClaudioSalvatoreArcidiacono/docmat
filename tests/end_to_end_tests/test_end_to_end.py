import glob
import os
from pathlib import Path

import pytest
from docmat.__main__ import format_file
from docmat.file import FileHandler


@pytest.mark.parametrize(
    "test_input_folder", glob.glob("tests/end_to_end_tests/test_inputs/*")
)
def test_end_to_end(test_input_folder):
    handler = FileHandler(os.path.join(test_input_folder, "input.py"))
    expected_file = Path(test_input_folder) / "expected.py"
    format_file(handler, 88)
    assert handler.formatted_file_content == expected_file.read_text()
