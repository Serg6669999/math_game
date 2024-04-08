class UserAnswer:
    _message = str()

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, text: str):
        self._message = text

    @message.deleter
    def message(self):
        self._message = str()