from .Result import Result
from genelang.functions import indent


class ResultList(Result):
    def __init__(self, process, at_position):
        super().__init__(process, at_position)
        self.results = []

    @property
    def to_position(self):
        return self.results[-1].to_position if self.results else self.at_position

    @property
    def empty(self):
        return all(result.empty for result in self.results)

    @property
    def error(self):
        return any(result.error for result in self.results)

    @property
    def valid(self):
        return not self.empty and not self.error

    @property
    def body(self):
        return f"\n{indent(result for result in self.results)}\n"

    def build(self, data: dict, pile: list) -> None:
        for result in self.results:
            if result.valid:
                result.build(data, pile)

    def append(self, result: Result):
        if self.results:
            assert self.results[-1].to_position == result.at_position
        else:
            assert self.at_position == result.at_position

        self.results.append(result)
