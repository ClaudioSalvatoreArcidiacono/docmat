from textwrap import TextWrapper

from .string_utils import capitalize, check_dot


def clean_text(text):
    for delimiter in ('"""', "'''"):
        if text.startswith(delimiter):
            text = text[len(delimiter) :]

        if text.endswith(delimiter):
            text = text[: -len(delimiter)]
    text = text.rstrip()
    return capitalize(check_dot(text))


class Summary:
    def __init__(
        self,
        summary,
        delimiter,
        should_wrap=False,
        line_length=None,
    ) -> None:
        clean_summary = clean_text(summary)
        clean_summary = delimiter + clean_summary
        if should_wrap:
            self.lines = TextWrapper(line_length).wrap(clean_summary)
        else:
            self.lines = [clean_summary]

    def __str__(self) -> str:
        return "\n".join(self.lines)


class NewLine:
    def __init__(self) -> None:
        self.lines = [""]

    def __str__(self) -> str:
        return ""


class UnindentedSection:
    def __init__(self, raw_lines, line_length) -> None:
        text = " ".join(l.strip() for l in raw_lines)
        cleaned_text = clean_text(text)
        self.lines = TextWrapper(line_length).wrap(cleaned_text)

    def __str__(self) -> str:
        return "\n".join(self.lines) + "\n"

    def __repr__(self) -> str:
        return f"UnindentedSection({str(self)})"

    def __eq__(self, __o: object) -> bool:
        return str(self) == str(__o)


class IndentedSection:
    def __init__(self, raw_lines, line_length) -> None:
        text = " ".join(l.strip() for l in raw_lines)
        cleaned_text = clean_text(text)
        self.lines = TextWrapper(line_length).wrap(cleaned_text)

    def __str__(self) -> str:
        return "\n".join(self.lines) + "\n"

    def __repr__(self) -> str:
        return f"IndentedSection({str(self)})"

    def __eq__(self, __o: object) -> bool:
        return str(self) == str(__o)
