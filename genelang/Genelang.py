import os
import re
from importlib import import_module
from .parsing import *
from .lexing import *
from .sugar import *
from .Parser import Parser
from .Engine import Engine
from .functions import indent

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
        body = indent(",\n".join(map(python2str, obj.builds)) + f",\ndefault={python2str(obj.default)}", prefix=INDENT)
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
    elif isinstance(obj, LUnary):
        body = indent(f"{repr(obj.key)},\n" + ",\n".join(map(python2str, obj.instructions)), prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, RUnary):
        body = indent(f"{repr(obj.key)},\n" + ",\n".join(map(python2str, obj.instructions)), prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Binary):
        body = indent(f"{repr(obj.key)},\n{python2str(obj.left)},\n{python2str(obj.right)}", prefix=INDENT)
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
    __versions__ = "C:/Users/gabri/Documents/projets/Genelang/genelang/versions"

    @classmethod
    def ast2py(cls, ast: dict):
        return eval(ast['__class__']).ast2py(ast, cls.ast2py)

    @classmethod
    def latest_version(cls):
        versions = []
        for filename in os.listdir(cls.__versions__):
            if match := re.match(r"^genelang_([0-9]+)_([0-9]+)_([0-9]+).py$", filename):
                major, minor, patch = map(int, match.groups())
                versions.append((major, minor, patch))

        return sorted(versions)[-1]

    @classmethod
    def load_engine(cls, version=None):
        if version is None:
            version = cls.latest_version()

        module = import_module(name=f".{cls.filename(version)}", package="genelang.versions")
        return module.engine

    @classmethod
    def save_engine(cls, version, engine):
        with open(f"{cls.__versions__}/{cls.filename(version)}.py", mode="w", encoding="utf-8") as file:
            file.write(f"from genelang import *\n\nengine = {cls.python2str(engine)}\n")

    @classmethod
    def filename(cls, version):
        return f"genelang_{version[0]}_{version[1]}_{version[2]}"

    @classmethod
    def make_transpiler(cls, target, version=None):
        """
            From a genelang file `target` and a genelang `version` indicator,
            create a .py file corresponding to target
        """
        if version is None:
            version = cls.latest_version()
        engine = cls.load_engine(version)

        ast = engine.read(f"{target}.gl")

        transpiler = cls.ast2py(ast)

        content = f"from genelang import *\n\nengine = {cls.python2str(transpiler)}\n"

        with open(f"{target}.py", mode="w", encoding="utf-8") as file:
            file.write(content)

    python2str = staticmethod(python2str)
