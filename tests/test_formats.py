from textwrap import dedent

import pytest
from docmat.docstring_formats.google.docstring import GoogleFormatter
from docmat.docstring_formats.shared import IndentedSection, UnindentedSection

TEST_INPUTS_DETECT_SUMMARY = [
    {
        "test_input": ["'''summary line'''"],
        "wrap_summary": False,
        "line_length": 60,
        "expected_output": "'''Summary line.'''\n",
    },
    {
        "test_input": ["'''\nsummary line\n'''"],
        "wrap_summary": False,
        "line_length": 60,
        "expected_output": "'''Summary line.'''\n",
    },
    {
        "test_input": ["'''\n\n\nsummary line'''"],
        "wrap_summary": False,
        "line_length": 60,
        "expected_output": "'''Summary line.'''\n",
    },
    {
        "test_input": ["'''summary line\n\n'''"],
        "wrap_summary": False,
        "line_length": 60,
        "expected_output": "'''Summary line.'''\n",
    },
    {
        "test_input": dedent(
            """\
                '''
            summary line
                '''
            """
        ).split("\n"),
        "wrap_summary": False,
        "line_length": 60,
        "expected_output": "    '''Summary line.'''\n",
    },
    {
        "test_input": dedent(
            """\
                '''
            summary line
                '''  
            """  # In this test example blank spaces are left intentionally
        ).split("\n"),
        "wrap_summary": False,
        "line_length": 60,
        "expected_output": "    '''Summary line.'''\n",
    },
]


@pytest.mark.parametrize(
    list(TEST_INPUTS_DETECT_SUMMARY[0].keys()),
    [tuple(test_case.values()) for test_case in TEST_INPUTS_DETECT_SUMMARY],
)
def test_detect_summary(test_input, wrap_summary, line_length, expected_output):
    assert (
        str(
            GoogleFormatter(
                test_input, wrap_summary=wrap_summary, line_length=line_length
            )
        )
        == expected_output
    )


TEST_INPUTS_WRAP_SUMMARY = [
    {
        "test_input": ["'''Very long summary line which should not be wrapped.'''"],
        "wrap_summary": False,
        "line_length": 20,
        "expected_output": "'''Very long summary line which should not be wrapped.\n'''\n",
    },
    {
        "test_input": ["'''Very long summary line which should be wrapped.'''"],
        "wrap_summary": True,
        "line_length": 20,
        "expected_output": "'''Very long summary\nline which should be\nwrapped.\n'''\n",
    },
    {
        "test_input": dedent(
            """\
                    '''All of this
                    is technically a
                    summary even if
                    it is broken into
                    multiple lines.
                    '''
                """
        ).split("\n"),
        "wrap_summary": True,
        "line_length": 17,
        "expected_output": dedent(
            """\
                    '''All of this is
                    technically a
                    summary even if
                    it is broken into
                    multiple lines.
                    '''
                """
        ),
    },
    {
        "test_input": dedent(
            """\
                    '''
                    All of this
                    is technically a
                    summary even if
                    it is broken into
                    multiple lines.
                    '''
                """
        ).split("\n"),
        "wrap_summary": True,
        "line_length": 17,
        "expected_output": dedent(
            """\
                    '''All of this is
                    technically a
                    summary even if
                    it is broken into
                    multiple lines.
                    '''
                """
        ),
    },
    {
        "test_input": ["'''20 characters --'''"],
        "wrap_summary": True,
        "line_length": 20,
        "expected_output": "'''20 characters --.\n'''\n",
    },
    {
        "test_input": ["'''This should fit in one line.'''"],
        "wrap_summary": True,
        "line_length": 34,
        "expected_output": "'''This should fit in one line.'''\n",
    },
]


@pytest.mark.parametrize(
    list(TEST_INPUTS_WRAP_SUMMARY[0].keys()),
    [tuple(test_case.values()) for test_case in TEST_INPUTS_WRAP_SUMMARY],
)
def test_wrap_summary(test_input, wrap_summary, line_length, expected_output):
    assert (
        str(
            GoogleFormatter(
                test_input, wrap_summary=wrap_summary, line_length=line_length
            )
        )
        == expected_output
    )


TEST_INPUTS_ITER_ELEMENTS = [
    {
        "test_input": dedent(
            """\
                    '''
                    Fist text block.

                    Section wrong indentation:
                    Second text block over
                    two lines

                    Section correct indentation:
                        Third text is 2 blank lines away
                        and it is over
                        3 lines

                    Text with multiple levels
                        other level here

                    '''
            """
        ).split("\n"),
        "offset": 0,
        "expected_output": [
            UnindentedSection,
            IndentedSection,
            IndentedSection,
            UnindentedSection,
        ],
    },
    {
        "test_input": dedent(
            """\
                    '''
                    Fist text block.

                    Section wrong indentation:
                    Second text block over
                    two lines

                    Section correct indentation::
                        Third text is 2 blank lines away
                        and it is over

                            3 lines

                    Text with multiple levels
                        other level here
                    '''
            """
        ).split("\n"),
        "offset": 0,
        "expected_output": [
            UnindentedSection,
            IndentedSection,
            IndentedSection,
            UnindentedSection,
        ],
    },
]


@pytest.mark.parametrize(
    list(TEST_INPUTS_ITER_ELEMENTS[0].keys()),
    [tuple(test_case.values()) for test_case in TEST_INPUTS_ITER_ELEMENTS],
)
def test_iter_elements(test_input, offset, expected_output):
    assert [
        type(el)
        for el in GoogleFormatter(test_input, line_length=60).iter_elements(offset)
    ] == expected_output


TEST_INPUTS_WRAP_TEXT_BLOCKS = [
    {
        "test_input": dedent(
            """\
                    '''Summary.
                    Fist text block.

                    Second text block over
                    two lines


                    Third text is 2 blank lines away
                    and it is over
                    3 lines
                    '''
            """
        ).split("\n"),
        "wrap_summary": False,
        "line_length": 20,
        "expected_output": dedent(
            """\
                    '''Summary.

                    Fist text block.

                    Second text block
                    over two lines.

                    Third text is 2
                    blank lines away and
                    it is over 3 lines.
                    '''
            """
        ),
    },
    {
        "test_input": dedent(
            """\
                    '''
                    Summary.
                    weird text block'''
            """
        ).split("\n"),
        "wrap_summary": False,
        "line_length": 20,
        "expected_output": dedent(
            """\
                    '''Summary.

                    Weird text block.
                    '''
            """
        ),
    },
]


@pytest.mark.parametrize(
    list(TEST_INPUTS_WRAP_TEXT_BLOCKS[0].keys()),
    [tuple(test_case.values()) for test_case in TEST_INPUTS_WRAP_TEXT_BLOCKS],
)
def test_wrap_text_blocks(test_input, wrap_summary, line_length, expected_output):
    assert (
        str(
            GoogleFormatter(
                test_input, wrap_summary=wrap_summary, line_length=line_length
            )
        )
        == expected_output
    )
