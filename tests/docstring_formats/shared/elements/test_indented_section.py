import pytest
from docmat.docstring_formats.shared.elements import IndentedSection


@pytest.mark.parametrize(
    ["test_input", "expected"],
    [
        (
            ["section: 1", "    text 1", "section: 2", "    text 2"],
            [["section: 1", "    text 1"], ["section: 2", "    text 2"]],
        )
    ],
)
def test_split_body_into_sections(test_input, expected):
    assert list(IndentedSection.split_body_into_sections(test_input, 0)) == expected
