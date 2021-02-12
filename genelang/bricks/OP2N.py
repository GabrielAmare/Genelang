from .OP2 import OP2


class OP2N(OP2):
    def __str__(self):
        return f"{str(self.items[0])}{str(self.symbols[0])}{str(self.items[1])}"
