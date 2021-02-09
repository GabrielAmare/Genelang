from importlib import import_module
from .parsing import *
from .lexing import *
from .sugar import *
from .Parser import Parser
from .Engine import Engine
from .functions import indent


def ast2genelang(ast: dict):
    __class__ = ast['__class__']
    if __class__ == "Engine":
        return Engine(
            lexer=ast2genelang(ast['lexer']),
            parser=ast2genelang(ast['parser'])
        )
    elif __class__ == "Parser":
        *builds, default = map(ast2genelang, ast['builds'])
        return Parser(*builds, default=default)
    elif __class__ == "Lexer":
        return Lexer(*map(ast2genelang, ast['patterns']))
    elif __class__ == "Build":
        return Build(
            name=ast['name'],
            process=ast2genelang(ast['process'])
        )
    elif __class__ == "Branch":
        return Branch(*map(ast2genelang, ast['instructions']))
    elif __class__ == "Match":
        return Match(
            name=ast['name']
        )
    elif __class__ == "As":
        return As(
            key=ast['key'],
            process=ast2genelang(ast['process'])
        )
    elif __class__ == "In":
        return In(
            key=ast['key'],
            process=ast2genelang(ast['process'])
        )
    elif __class__ == "Any":
        return Any(*map(ast2genelang, ast['instructions']))
    elif __class__ == "Optional":
        return Optional(*map(ast2genelang, ast['instructions']))
    elif __class__ == "While":
        return While(*map(ast2genelang, ast['instructions']))
    elif __class__ == "Call":
        return Call(name=ast['name'])
    elif __class__ == "NamedProcess":
        return NamedProcess(name=ast['name'], process=ast2genelang(ast['process']))
    elif __class__ == "Pattern":
        return Pattern(
            name=ast['name'],
            mode=ast['mode'],
            expr=eval(ast['expr']),
            flag=int(ast.get('flag', 0)),
            ignore=bool(ast.get('ignore_'))
        )
    elif __class__ == "Bloc":
        return Bloc(
            ast['left'],
            ast['right'],
            *map(ast2genelang, ast['instructions'])
        )
    else:
        raise Exception(f"Unable to ast2genelang code corresponding to {__class__}, {ast}")


INDENT = "    "


def python2str(obj):
    if isinstance(obj, Engine):
        body = indent(f"{python2str(obj.lexer)},\n{python2str(obj.parser)}", prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Lexer):
        body = indent(",\n".join(map(python2str, obj.patterns)), prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Pattern):
        return f"{obj.__class__.__name__}({repr(obj.name)}, {repr(obj.mode)}, {repr(obj.expr)}, {repr(obj.flag)}, {repr(obj.ignore)})"
    elif isinstance(obj, Parser):
        body = indent(",\n".join(map(python2str, obj.builds)) + f",\ndefault={python2str(obj.default)}",prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Build):
        body = indent(f"{repr(obj.name)},\n{python2str(obj.process)}", prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Branch):
        body = indent(",\n".join(map(python2str, obj.instructions)), prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, While):
        body = indent(",\n".join(map(python2str, obj.branch.instructions)), prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Optional):
        body = indent(",\n".join(map(python2str, obj.branch.instructions)), prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Match):
        return f"{obj.__class__.__name__}({repr(obj.name)})"
    elif isinstance(obj, As):
        return f"{obj.__class__.__name__}({repr(obj.key)}, {python2str(obj.process)})"
    elif isinstance(obj, In):
        return f"{obj.__class__.__name__}({repr(obj.key)}, {python2str(obj.process)})"
    elif isinstance(obj, Any):
        body = indent(",\n".join(map(python2str, obj.instructions)), prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Call):
        return f"{obj.__class__.__name__}({repr(obj.name)})"
    elif isinstance(obj, NamedProcess):
        body = indent(f"{repr(obj.name)},\n{python2str(obj.process)}", prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Bloc):
        body = ",\n".join(map(python2str, obj.instructions))
        body = indent(f"{repr(obj.left)},\n{repr(obj.right)},\n{body}", prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    else:
        raise Exception(f"Unable to python2str for obj of class {obj.__class__.__name__}")


class Genelang:
    @classmethod
    def load_engine(cls, version):
        module = import_module(name=f"genelang.versions.{cls.filename(version)}")
        return module.engine

    @classmethod
    def save_engine(cls, version, engine):
        with open(f"genelang/versions/{cls.filename(version)}.py", mode="w", encoding="utf-8") as file:
            file.write(f"from genelang import *\n\nengine = {cls.python2str(engine)}\n")

    @classmethod
    def filename(cls, version):
        return f"genelang_{version[0]}_{version[1]}_{version[2]}"

    ast2genelang = staticmethod(ast2genelang)
    python2str = staticmethod(python2str)
