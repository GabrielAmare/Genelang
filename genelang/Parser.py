from genelang.lexing import TokenList
from genelang.parsing import Build, NamedProcess


class Parser:
    def __init__(self, *builds):
        assert all(isinstance(build, (Build, NamedProcess)) for build in builds)
        self.builds = builds

    @property
    def default(self):
        return self.builds[-1]

    def __repr__(self):
        return f"Parser(" + ", ".join(map(repr, self.builds)) + ")"

    def get_builder(self, name):
        for build in self.builds:
            if build.name == name:
                return build

    def build(self, tokens: TokenList):
        return self.default.build(parser=self, tokens=tokens, at_position=0)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(*map(parser, ast['builds']))
