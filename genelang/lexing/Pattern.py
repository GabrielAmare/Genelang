import re
from .Token import Token


class Pattern:
    def __init__(self, name: str, mode: str, expr: str, flag: int = 0, ignore: bool = False):
        self.name = name
        self.mode = mode
        self.expr = expr
        self.flag = flag

        self.ignore = ignore

        if self.mode == "re":
            self.regex = re.compile(pattern=self.expr, flags=self.flag)
        elif self.mode == "kw":
            self.regex = re.compile(pattern=r"(?<!\w)" + self.expr + r"(?!\w)", flags=self.flag)
        elif self.mode == "lkw":
            self.regex = re.compile(pattern=self.expr + r"(?!\w)", flags=self.flag)
        elif self.mode == "rkw":
            self.regex = re.compile(pattern=r"(?<!\w)" + self.expr, flags=self.flag)
        else:
            self.regex = None

    @property
    def as_python(self):
        optionals = ""
        if self.flag != 0:
            optionals += f", flag={self.flag}"
        if self.ignore:
            optionals += f", ignore=True"
        return f"{self.__class__.__name__}(name={repr(self.name)}, mode={repr(self.mode)}, expr={repr(self.expr)}{optionals})"

    @property
    def as_genelang(self):
        optionals = ""
        if self.flag != 0:
            optionals += f" {self.flag}"
        if self.ignore:
            optionals += f" ignore"
        return f"@ {self.name} {self.mode} {repr(self.expr)}{optionals}"

    @classmethod
    def from_ast(cls, ast: dict):
        name = ast['name']
        mode = ast['mode']
        expr = eval(ast['expr'])
        flag = int(ast.get('flag', '0'))
        ignore = bool(ast.get('ignore', ''))
        return cls(name=name, mode=mode, expr=expr, flag=flag, ignore=ignore)

    def read(self, text, at_index, at_position):
        if self.regex:
            if match := self.regex.match(text, at_index):
                return Token(pattern=self, content=match.group(), at_index=at_index, at_position=at_position)
        else:
            if text.startswith(self.expr, at_index):
                return Token(pattern=self, content=self.expr, at_index=at_index, at_position=at_position)
