from .ResultUnit import ResultUnit
from genelang.functions import indent


class NamedProcessResult(ResultUnit):
    @property
    def body(self):
        return f"{self.process.name} ->\n{indent(self.result)}\n"
