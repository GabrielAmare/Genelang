from genelang.bricks import Brick
from .Group import Group


class Identifier(Brick):
    def __init__(self, name, *groups: Group):
        self.name = name
        self.groups = groups

    def match(self, obj):
        if isinstance(obj, str):
            return self.name == obj
        elif isinstance(obj, Identifier):
            if self.name == "":
                return self.name in ("", obj.name) and \
                       all(group in obj.groups for group in self.groups)
        else:
            raise Exception

    def __repr__(self):
        args = [self.name, *self.groups]
        return f"{self.__class__.__name__}(" + ", ".join(map(repr, args)) + ")"

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(ast.get('name', ''), *map(parser, ast.get('groups', [])))

