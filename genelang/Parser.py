from genelang.lexing import TokenList
from genelang.parsing import Build


class Parser:
    def __init__(self, *builds, default: Build):
        self.builds = builds
        self.default = default

    def get_builder(self, name):
        for build in self.builds:
            if build.name == name:
                return build

    def build(self, tokens: TokenList):
        return self.default.build(parser=self, tokens=tokens, at_position=0)
