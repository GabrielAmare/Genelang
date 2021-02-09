from .Result import Result


class MatchResult(Result):
    def __init__(self, process, at_position: int, token, valid: bool):
        super().__init__(process, at_position)
        self.token = token
        self.valid = valid

    @property
    def to_position(self):
        if self.token and self.valid:
            return self.token.to_position
        else:
            return self.at_position

    @property
    def empty(self):
        return not self.token or not self.valid

    @property
    def error(self):
        return self.empty or not self.valid

    @property
    def body(self):
        if self.token:
            return f" {self.process.name} : {repr(self.token.content)} "
        else:
            return f" {self.process.name} : None "

    def build(self, data: dict, pile: list) -> None:
        if self.token:
            pile.append(self.token.content)
