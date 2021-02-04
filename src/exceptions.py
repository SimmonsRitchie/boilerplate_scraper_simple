import logging

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""

    pass


class NoJsonDataError(Error):
    """Raised when response from server has provided an empty JSON response"""

    def __init__(
        self,
        message="No JSON data was returned from request. Something about the request may be bad or the endpoint may have changed.",
    ):
        self.message = message
        super().__init__(self.message)


class NoEnvVarError(Error):
    def __init__(
        self,
        env_var,
        message="Environment variable should be defined.",
    ):
        self.env_var = env_var
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.env_var} -> {self.message}"
