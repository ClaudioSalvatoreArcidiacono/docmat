import pytest
from docmat.google_format.summary import Summary


@pytest.mark.parametrize(
    ["test_input", "expected"],
    [
        (
            """\
        '''Here the summary starts at index 0'''\
        """,
            0,
        ),
        (
            """\
        '''
        Here there is the summary (wrongly) starts on a new line'''\
        """,
            1,
        ),
        (
            """\
         '''  
          Some variations of the previous one with some random spaces here and there 
         '''\
        """,
            1,
        ),
    ],
)
def test_start_offset(test_input, expected):
    assert Summary.find_start_offset(test_input.split("\n"), "'''") == expected


@pytest.mark.parametrize(
    ["test_input", "start_offset", "expected"],
    [
        (
            """\
        '''Here the summary starts at index 0'''\
        """,
            0,
            1,
        ),
        (
            """\
        '''
        Here there is the summary (wrongly) starts on a new line'''\
        """,
            1,
            2,
        ),
        (
            """\
        '''  
          Some variations of the previous one with some
          random spaces here and there 
           '''\
        """,
            1,
            4,
        ),
    ],
)
def test_end_offset(test_input, start_offset, expected):
    assert (
        Summary.find_end_offset(test_input.split("\n"), start_offset, "'''") == expected
    )


TEST_INPUTS = [
    {
        "test_input": ["summary line"],
        "should_wrap": False,
        "delimiter": '"""',
        "line_length": 60,
        "expected_output": '"""Summary line.',
    },
    {
        "test_input": ["Very long summary line which should not be wrapped."],
        "should_wrap": False,
        "delimiter": '"""',
        "line_length": 20,
        "expected_output": '"""Very long summary line which should not be wrapped.',
    },
    {
        "test_input": ["Very long summary line which should be wrapped."],
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
        "\n".join(Summary(test_input, delimiter, should_wrap, line_length).format())
        == expected_output
    )
