class Input:
    def __init__(self, filename: str):
        self.filename = filename

    def _read(self):
        with open(self.filename) as f:
            return [line.strip() for line in f.readlines()]

    @property
    def data(self) -> list:
        return self._read()
