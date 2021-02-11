from .Process import Process


class _Name_Process(Process):
    def __init__(self, name, process):
        self.name = name
        self.process = process

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.name)}, {repr(self.process)})"

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(name=ast['name'], process=parser(ast['process']))
