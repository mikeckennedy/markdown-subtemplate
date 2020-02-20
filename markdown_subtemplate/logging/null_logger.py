from .subtemplate_logger import SubtemplateLogger
from .log_level import LogLevel


class NullLogger(SubtemplateLogger):
    def __init__(self):
        super().__init__(LogLevel.error)

    def verbose(self, text: str):
        pass

    def trace(self, text: str):
        pass

    def info(self, text: str):
        pass

    def error(self, text: str):
        pass
