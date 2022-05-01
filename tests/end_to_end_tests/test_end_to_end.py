import glob
import os
from pathlib import Path

import pytest
import yaml
from docmat.__main__ import ARGS_DEFAULT, format_file
from docmat.file import FileHandler


@pytest.mark.parametrize(
    "test_input_folder", glob.glob("tests/end_to_end_tests/test_inputs/*")
)
def test_end_to_end(test_input_folder):
    handler = FileHandler(os.path.join(test_input_folder, "input.py"))
    expected_file = Path(test_input_folder) / "expected.py"
    extra_params_file = Path(test_input_folder) / "extra_params.yml"
    extra_params = ARGS_DEFAULT
    if extra_params_file.is_file():
        extra_params.update(yaml.safe_load(extra_params_file.read_text()))
    format_file(handler, **extra_params)
    assert handler.formatted_file_content == expected_file.read_text()
