from .input import Input


class Day:
    def __init__(self, input: str) -> None:
        self._input = Input(input)
        pass

    @property
    def data(self) -> list:
        return self._input.data