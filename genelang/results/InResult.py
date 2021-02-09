from .ResultUnit import ResultUnit
from genelang.functions import indent


class InResult(ResultUnit):
    @property
    def body(self):
        return f"{self.process.key} ->\n{indent(self.result)}\n"

    def build(self, data: dict, pile: list) -> None:
        self.result.build({}, pile)
        data.setdefault(self.process.key, [])
        data[self.process.key].append(pile.pop(-1))
