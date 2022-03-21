from docmat.docstring_formats.shared import Summary
import pytest

TEST_INPUTS = [
    {
        "test_input": "summary line",
        "should_wrap": False,
        "delimiter": '"""',
        "line_length": 60,
        "expected_output": '"""Summary line.',
    },
    {
        "test_input": "Very long summary line which should not be wrapped.",
        "should_wrap": False,
        "delimiter": '"""',
        "line_length": 20,
        "expected_output": '"""Very long summary line which should not be wrapped.',
    },
    {
        "test_input": "Very long summary line which should be wrapped.",
        "should_wrap": True,
        "delimiter": '"""',
        "line_length": 20,
        "expected_output": '"""Very long summary\nline which should be\nwrapped.',
    },
]


@pytest.mark.parametrize(
    list(TEST_INPUTS[0].keys()),
    [tuple(test_case.values()) for test_case in TEST_INPUTS],
)
def test_word_wrapping(
    test_input, delimiter, should_wrap, line_length, expected_output
):
    assert (
        str(Summary(test_input, delimiter, should_wrap, line_length)) == expected_output
    )
