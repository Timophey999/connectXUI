class NullLogger:
    """A null logger that mimics the behavior of Python's logging.Logger.

    This is used as a fallback when no actual logger is set.
    """

    def __init__(self, name: str):
        pass

    def debug(self, msg, *args, **kwargs) -> None:
        pass

    def info(self, msg, *args, **kwargs) -> None:
        pass

    def warning(self, msg, *args, **kwargs) -> None:
        pass

    def error(self, msg, *args, **kwargs) -> None:
        pass

    def critical(self, msg, *args, **kwargs) -> None:
        pass

    def exception(self, msg, *args, **kwargs) -> None:
        """Handles exceptions, commonly used with logging.exception()."""
        pass

    def log(self, level, msg, *args, **kwargs) -> None:
        pass
