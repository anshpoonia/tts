class ParameterError(Exception):
    def __init__(self, message="Parameters not found."):
        self.message = message
        super().__init__(self.message)


class FileSizeError(Exception):
    def __init__(self, message="File Size exceeds 25MB."):
        self.message = message
        super().__init__(self.message)


class LanguageError(Exception):
    def __init__(self, message="Language not available."):
        self.message = message
        super().__init__(self.message)


class SpeakerNotFoundError(Exception):
    def __init__(self, message="Given speaker doesn't exists."):
        self.message = message
        super().__init__(self.message)


class FileNotSelectedError(Exception):
    def __init__(self, message="No file selected."):
        self.message = message
        super().__init__(self.message)
