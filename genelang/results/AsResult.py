from .ResultUnit import ResultUnit
from ..functions import indent


class AsResult(ResultUnit):
    @property
    def body(self):
        return f"{self.process.key} ->\n{indent(self.result)}\n"

    def build(self, data: dict, pile: list) -> None:
        self.result.build({}, pile)
        data[self.process.name] = pile.pop(-1)
