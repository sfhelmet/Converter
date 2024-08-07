class InvalidUsageError(Exception):
    """Exception for invalid usage of a module."""
    pass

class NotSupportedError(Exception):
    """Exception for a file type that is not supported yet."""
    pass