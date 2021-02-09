class Result:
    valid: bool
    error: bool
    empty: bool

    at_position: int
    to_position: int

    def __init__(self, process, at_position: int):
        self.process = process
        self.at_position = at_position

    def __repr__(self):
        icon = 'X' if self.error else 'I' if self.valid else ' '
        return f"[{icon}]{self.process.__class__.__name__}[{self.body}]"

    body = ""

    def build(self, data: dict, pile: list) -> None:
        raise NotImplementedError
