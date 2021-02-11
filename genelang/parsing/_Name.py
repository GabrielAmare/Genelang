from .Process import Process


class _Name(Process):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.name)})"

    @classmethod
    def ast2py(cls, ast: dict, _parser: callable):
        return cls(name=ast['name'])
