from pygments import lexers
from pygments.formatters import TerminalFormatter
from pygments import highlight

formatter_default = TerminalFormatter(style='default')


def highlight_code(code: str, lexer_name: str = 'python') -> str:
    lexer = lexers.get_lexer_by_name(lexer_name)
    highlighted = highlight(code, lexer, formatter_default)
    # TODO: исправить костыль
    highlighted = highlighted.replace("\x1b[39;49;00m", "\x1b[0;32m")
    highlighted = highlighted.replace("04", "4")
    highlighted = highlighted.replace("90", "0")

    return highlighted

