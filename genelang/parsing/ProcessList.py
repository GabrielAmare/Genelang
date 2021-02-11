from .Process import Process


class ProcessList(Process):
    def __init__(self, *instructions):
        assert all(isinstance(instruction, Process) for instruction in instructions)
        self.instructions = instructions

    def __repr__(self):
        return f"{self.__class__.__name__}(" + ", ".join(map(repr, self.instructions)) + ")"

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(*map(parser, ast['instructions']))
