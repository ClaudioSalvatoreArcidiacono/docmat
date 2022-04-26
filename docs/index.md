<!-- omit in TOC -->
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
    """start with lower letter, dot missing"""
```

After:

```python
def func():
    """Start with lower letter, dot missing."""
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

## Integration with VSCode

`docmat` will be integrated with `VSCode` using a dedicated extension (see also [roadmap](#roadmap)).

In the meantime, `docmat` can be used from `VSCode` with a keyboard shortcut. Here are the steps to make it work:

1. Install `docmat` in the python environment used by VSCode following the [installation steps](#installation)
2. Open the Keyboard Shortcuts configuration file in VSCode `Preferences > Keyboard Shortcuts > Open Keyboard Shortcuts (JSON) [icon in the top-right]` this will open the `keybindings.json` file containing the keyboard shortcuts.
3. Associate the docmat command to a key-binding by adding the following entry to the keybindings list:

```json
[
    {
        "key": "shift+alt+d",
        "command": "workbench.action.terminal.sendSequence",
        "args": {
            "text": "docmat '${file}'\u000D"
        }
    }
]
```

    The suggested key-binding is `shift`+`alt`+`D`, but you can change it to whatever you like.

4. Save the file.

Now, every time you are working on a python file you can hit `shift`+`alt`+`D` and the `docmat` command will be executed in the VSCode terminal on the file that you have currently opened. Eventual errors or log messages will be shown there. Please note that the environment where `docmat` is installed should be active in the VSCode integrated terminal prior to using the shortcut.

## Roadmap

- Add support for a no-format comment token.
- Add support for bullet lists.
- Add support for other docstring formats:
  - Numpydoc
  - reST
  - Epytext
- Integrate with pre-commit.
- Create VSCode extension.
- Add support for code examples in docstring.
