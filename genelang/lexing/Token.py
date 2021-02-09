class Token:
    def __init__(self, pattern, content, at_index, at_position):
        self.pattern = pattern
        self.content = content
        self.at_index = at_index
        self.at_position = at_position

    @property
    def to_index(self):
        return self.at_index + len(self.content)

    @property
    def to_position(self):
        return self.at_position + 1

    def __repr__(self):
        return f"{self.pattern.name} : {repr(self.content)} : [{self.at_index} -> {self.to_index}]"
