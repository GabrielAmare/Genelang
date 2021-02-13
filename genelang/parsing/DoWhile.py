from .Process import Process
from .Branch import Branch
from genelang.lexing import TokenList
from genelang.results import DoWhileResult


class DoWhile(Process):
    def __init__(self, left: Branch, right: Branch):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(left=parser(ast['left']), right=parser(ast['right']))

    def build(self, parser, tokens: TokenList, at_position: int) -> DoWhileResult:
        result = DoWhileResult(self, at_position)

        while True:
            do_result = self.left.build(parser, tokens, at_position)

            result.append(do_result)

            if do_result.error:
                break

            at_position = do_result.to_position

            while_result = self.right.build(parser, tokens, at_position)

            if while_result.empty or while_result.error:
                break

            at_position = while_result.to_position

            result.append(while_result)

        return result
