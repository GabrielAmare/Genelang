from .Process import Process
from .Branch import Branch
from genelang.lexing import TokenList
from genelang.results import WhileResult


class While(Process):
    def __init__(self, *instructions):
        self.branch = Branch(*instructions)

    def build(self, parser, tokens: TokenList, at_position: int) -> WhileResult:
        while_result = WhileResult(self, at_position)

        while True:
            branch_result = self.branch.build(parser, tokens, at_position)

            if branch_result.error:
                break

            if branch_result.empty:
                break

            while_result.append(branch_result)

            at_position = branch_result.to_position

        return while_result

    @classmethod
    def ast2py(cls, ast: dict, parser: callable):
        return cls(*map(parser, ast['instructions']))