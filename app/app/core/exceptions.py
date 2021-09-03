"""
These exceptions are provided as an example of the types of custom exceptions that
can be added to the application.
"""


class ApiError(Exception):
    """ Base class for exceptions that occur during API requests """

    def __init__(self, *args, **kwargs):
        self.api_endpoint = kwargs.pop("api_endpoint", None)
        super(ApiError, self).__init__(*args, **kwargs)

    def __str__(self):
        """
        Combines the docstring of the exception with the defined endpoint provided.
        """
        return f"{self.__doc__}{self.api_endpoint or ''}"


class ApiAuthenticationError(ApiError, ValueError):
    """ Error occurred during API authentication process with """

    def __str__(self):
        return f"{super().__str__()} ({self.args[0]})"


class ApiNotFoundError(ApiError, ValueError):
    """ Failed to locate the requested resource within the API from """


class ApiIntegrationError(ApiError, ValueError):
    """ Issue with the configuration supporting the API integration from """

    def __str__(self):
        return f"{super().__str__()} ({self.args[0]})"


class ApiRateLimitError(ApiError, ValueError):
    """ Rate limits have been exceeded for """

    pass


class ApiSerializationError(ApiError, ValueError):
    """ Serialization/validation issue occurred when parsing API's response content from """

    pass


class ApiTimeoutError(ApiError, TimeoutError):
    """ Timeout occurred during API request to """

    pass
