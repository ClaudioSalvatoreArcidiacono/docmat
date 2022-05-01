import re


def check_dot(line):
    punctuation = ".!?"
    if not any(line.endswith(p) for p in punctuation):
        return line + "."
    else:
        return line


def capitalize(line):
    if line:
        return line[0].upper() + line[1:]
    return ""

def count_indentation_level(line):
    return len(line) - len(line.lstrip())


