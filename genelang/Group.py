from genelang.parsing._Name import _Name


class Group(_Name):
    def __eq__(self, other):
        return isinstance(other, Group) and self.name == other.name