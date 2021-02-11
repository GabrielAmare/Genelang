import os
import re
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
        body = indent(",\n".join(map(python2str, obj.instructions)), prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Optional):
        body = indent(",\n".join(map(python2str, obj.instructions)), prefix=INDENT)
        return f"{obj.__class__.__name__}(\n{body}\n)"
    elif isinstance(obj, Match):
        return f"{obj.__class__.__name__}({repr(obj.name)})"
    elif isinstance(obj, As):
        return f"{obj.__class__.__name__}({repr(obj.name)}, {python2str(obj.process)})"
    elif isinstance(obj, In):
        return f"{obj.__class__.__name__}({repr(obj.name)}, {python2str(obj.process)})"
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
        raise Exception(f"Unable to python2str for obj of class {obj.__class__.__name__} : {obj}")


class Genelang:
    __versions__ = dict(
        genelang="C:/Users/gabri/Documents/projets/Genelang/genelang/versions"
    )

    __builders__ = dict(
        genelang=dict(
            Engine=Engine,
            Lexer=Lexer,
            Pattern=Pattern,
            Parser=Parser,
            Any=Any,
            As=As,
            Branch=Branch,
            Build=Build,
            Call=Call,
            In=In,
            Match=Match,
            NamedProcess=NamedProcess,
            Optional=Optional,
            While=While,
            Binary=Binary,
            Bloc=Bloc,
            LUnary=LUnary,
            RUnary=RUnary
        )
    )

    @classmethod
    def parse_filename(cls, filename: str):
        if match := re.match(fr"^([a-zA-Z][a-zA-Z0-9]*)_([0-9]+)_([0-9]+)_([0-9]+).(gl|py)$", filename):
            lang, major, minor, patch, ext = match.groups()
            return dict(
                lang=lang,
                major=int(major),
                minor=int(minor),
                patch=int(patch),
                version=(int(major), int(minor), int(patch)),
                type={'gl': 'genelang', 'py': 'python'}[ext]
            )
        else:
            return None

    @classmethod
    def make_filename(cls, lang, version, type='python', tag=""):
        ext = {'genelang': 'gl', 'python': 'py'}[type]
        major, minor, patch = version
        if tag:
            return f"{lang}_{major}_{minor}_{patch}_{tag}.{ext}"
        else:
            return f"{lang}_{major}_{minor}_{patch}.{ext}"

    @classmethod
    def make_filepath(cls, lang, version, type='python', tag=""):
        return f"{cls.__versions__[lang]}/{cls.make_filename(lang, version, type, tag)}"

    @classmethod
    def ast2py(cls, ast: dict, lang="genelang"):
        builders = cls.__builders__[lang]

        def parser(ast: dict):
            return builders[ast['__class__']].ast2py(ast, parser)

        return parser(ast)

    @classmethod
    def latest_version(cls, lang="genelang") -> tuple:
        versions = []
        for filename in os.listdir(cls.__versions__[lang]):
            if data := cls.parse_filename(filename):
                if data['lang'] == lang:
                    if data['type'] == 'python':
                        versions.append(data['version'])

        if not versions:
            raise Exception(f"No available version of {lang} in {cls.__versions__[lang]}")

        return sorted(versions)[-1]

    @classmethod
    def load_engine(cls, lang="genelang", version=None):
        if version is None:
            version = cls.latest_version(lang)

        filepath = cls.make_filepath(lang=lang, version=version, type="python")
        with open(filepath, mode="r", encoding="utf-8") as file:
            content = file.read()

        new_locals = {}
        exec(content, globals(), new_locals)
        return new_locals['engine']

    @classmethod
    def save_engine(cls, engine, lang="genelang", version=None, tag=""):
        if version is None:
            major, minor, patch = cls.latest_version(lang=lang)
            version = (major, minor, patch + 1)

        filepath = cls.make_filepath(lang=lang, version=version, type="python", tag=tag)
        with open(filepath, mode="w", encoding="utf-8") as file:
            file.write(f"from genelang import *\n\nengine = {cls.python2str(engine)}\n")

    @classmethod
    def make_engine(cls, lang, version, gl_version=None) -> Engine:
        if gl_version is None:
            gl_version = cls.latest_version(lang="genelang")

        gl_engine = cls.load_engine(lang="genelang", version=gl_version)

        filepath = cls.make_filepath(lang=lang, version=version, type="genelang")

        ast = gl_engine.read_file(filepath=filepath)

        engine = cls.ast2py(ast, lang="genelang")

        return engine

    @classmethod
    def build_engine(cls, lang, version, gl_version=None, tag="") -> None:
        """
            From a genelang file `target` and a genelang `version` indicator,
            create a .py file corresponding to target
        """
        engine = cls.make_engine(lang=lang, version=version, gl_version=gl_version)

        cls.save_engine(engine=engine, lang=lang, version=version, tag=tag)

    python2str = staticmethod(python2str)
