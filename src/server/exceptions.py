
class myException(Exception):
    def __init__(self, message="An error occurred", code=400):
        super().__init__(message)
        self.code = code