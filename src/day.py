class Day:
    def __init__(self, input: str) -> None:
        self._input = input
        pass

    @property
    def raw_data(self) -> list[str]:
        with open(self._input) as f:
            return [line.strip() for line in f.readlines()]

    @property
    def data(self) -> list:
        return self.raw_data
