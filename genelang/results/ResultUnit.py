from .Result import Result
from genelang.functions import indent


class ResultUnit(Result):
    def __init__(self, process, at_position, result):
        super().__init__(process, at_position)
        self.result = result

    @property
    def body(self):
        return f"\n{indent(self.result)}\n"

    def build(self, data: dict, pile: list) -> None:
        if self.result and self.result.valid:
            self.result.build(data, pile)

    @property
    def to_position(self):
        return self.result.to_position if self.result else self.to_position

    @property
    def valid(self):
        if self.result:
            return self.result.valid
        else:
            return False

    @property
    def empty(self):
        if self.result:
            return self.result.empty
        else:
            return True

    @property
    def error(self):
        if self.result:
            return self.result.error
        else:
            return True
