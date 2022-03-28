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


def get_section_name(line):
    match = re.match(r"^([^\n\:]+)\:\:?$", line)
    if match:
        return match.group(1)
    else:
        return None


def count_indentation_level(line):
    return len(line) - len(line.lstrip())


def is_start_of_indented_section(line):
    return bool(get_section_name(line))
