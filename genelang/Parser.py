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

    def get_builders(self, identifier):
        for build in self.builds:
            if identifier.match(build.identifier):
                yield build

    def get_builder(self, name):
        for build in self.builds:
            if build.identifier.name == name:
                return build

    def build(self, tokens: TokenList, base=None):
        if base:
            process = self.get_builder(base) or self.default
        else:
            process = self.default

        return process.build(parser=self, tokens=tokens, at_position=0)

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(*map(parser, ast['builds']))
