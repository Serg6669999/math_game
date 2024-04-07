class UserAnswer:
    _message = str()

    @property
    def message(self) -> str:
        text = self._message[:]
        self._message = str()

        return text

    @message.setter
    def message(self, text: str):
        self._message = text

    @message.deleter
    def message(self):
        self._message = str()