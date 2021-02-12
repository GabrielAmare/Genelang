from .OP1 import OP1


class OP1L(OP1):
    def __str__(self):
        return f"{str(self.symbols[0])}{str(self.items[0])}"
