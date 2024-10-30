class TokenClass:
    def __init__(self, lexeme, tkn, pos, line):
        self.lexeme = lexeme
        self.tkn = tkn
        self.pos = pos
        self.line = line


def __repr__(self):
    return (
        f"TokenClass(lexeme={self.lexeme!r}, tkn={self.tkn!r}, "
        f"pos={self.pos}, line={self.line})"
    )
