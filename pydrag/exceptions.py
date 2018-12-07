class ApiError(Exception):
    def __init__(self, message, error, links) -> None:
        super(ApiError, self).__init__(message)
        self.message = message
        self.error = error
        self.links = links
