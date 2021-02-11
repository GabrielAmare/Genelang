import os
import re
from .parsing import *
from .lexing import *
from .sugar import *
from .Parser import Parser
from .Engine import Engine


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
        try:
            exec(content, globals(), new_locals)
        except:
            raise Exception(f"Unable to read :\n{content}")
        return new_locals['engine']

    @classmethod
    def save_engine(cls, engine, lang="genelang", version=None, tag=""):
        if version is None:
            major, minor, patch = cls.latest_version(lang=lang)
            version = (major, minor, patch + 1)

        filepath = cls.make_filepath(lang=lang, version=version, type="python", tag=tag)
        with open(filepath, mode="w", encoding="utf-8") as file:
            file.write(f"from genelang import *\n\nengine = {repr(engine)}\n")

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
