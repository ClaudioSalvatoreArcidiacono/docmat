# docmat

Python docstring formatter.

## Main Functionalities

- Adjusts indentation and spacing.
- Wraps all docstring text.

## Installation

```bash
pip install docmat
```

## Usage

In order to format the docstring of a file, run in a terminal shell:

```bash
docmat <filename>|<folder>|<glob>
```

Examples:

```bash
docmat to_format.py
```

```bash
docmat to_format.py other_file_to_format.py
```

```bash
docmat to_format.py --line-length 79
```

```bash
docmat directory
```

```bash
docmat directory/*
```

## Supported docstring formats

- Google

Adding support for other docstring formats is in the Roadmap.

## Examples

Before:

```python
def func():
    """
    This fits in one line.
    """
```

After:

```python
def func():
    """This fits in one line."""
```

---
Before:

```python
def func():
    """start with lower capital, dot missing"""
```

After:

```python
def func():
    """Start with lower capital, dot missing."""
```

---
Before:

```python
def func():
    """
    In this docstring a newline after the summary is missing.
    Summary and description should be separated by a newline.
    """
```

After:

```python
def func():
    """
    In this docstring a newline after the summary is missing.

    Summary and description should be separated by a newline.
    """
```

---
Before:

```python
def func():
    """
    Summary.

    The length of the function description in this specific function exceeds the maximum line length, that in this case is left to the default value `88`. This block of text should be wrapped.
    """
```

After:

```python
def func():
    """Summary.

    The length of the function description in this specific function exceeds the maximum
    line length, that in this case is left to the default value `88`. This block of text
    should be wrapped.
    """
```

---
Adding the parameter `--wrap-summary`

Before:

```python
def func():
    """By default, the summary line is not wrapped even if it exceeds the maximum line length.

    This behavior can be overriden by adding the `--wrap-summary` command line parameter
    """
```

After:

```python
def func():
    """By default, the summary line is not wrapped even if it exceeds the maximum line
    length.

    This behavior can be overriden by adding the `--wrap-summary` command line
    parameter.
    """
```

---
Before:

```python
def func(arg1, arg2):
    """Summary.

    args:
    arg1(type): The indentation level of this argument is not correct.
    arg2(type): In this case, the description of this argument exceeds the maximum line length and it needs to be wrapped.
    """
```

After:

```python
def func(arg1, arg2):
    """Summary.

    Args:
        arg1(type): The indentation level of this argument is not correct.
        arg2(type): In this case, the description of this argument exceeds the maximum
            line length and it needs to be wrapped.
    """
```

## Roadmap

- Add support for bullet lists.
- Add support for other docstring formats:
  - Numpydoc
  - reST
  - Epytext
- Integrate with pre-commit.
- Integrate with VSCode.
