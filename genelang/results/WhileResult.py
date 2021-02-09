from .ResultList import ResultList


class WhileResult(ResultList):
    valid = True
    error = False

    @property
    def empty(self):
        return all(result.empty for result in self.results)
