from .ResultUnit import ResultUnit
from ..functions import indent


class BuildResult(ResultUnit):
    @property
    def body(self):
        return f"{self.process.name} ->\n{indent(self.result)}\n"

    def build(self, data: dict, pile: list) -> None:
        n_data = {}
        self.result.build(n_data, pile)
        n_data['__class__'] = self.process.identifier.name
        pile.append(n_data)
