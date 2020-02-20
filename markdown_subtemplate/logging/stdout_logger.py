from .log_level import LogLevel
from .subtemplate_logger import SubtemplateLogger


class StdOutLogger(SubtemplateLogger):
    prefix = 'Markdown Subtemplates'

    def verbose(self, text: str):
        if not self.should_log(LogLevel.verbose, text):
            return

        self._publish(text, LogLevel.verbose)

    def trace(self, text: str):
        if not self.should_log(LogLevel.trace, text):
            return

        self._publish(text, LogLevel.trace)

    def info(self, text: str):
        if not self.should_log(LogLevel.info, text):
            return

        self._publish(text, LogLevel.info)

    def error(self, text: str):
        if not self.should_log(LogLevel.error, text):
            return

        self._publish(text, LogLevel.error)

    def _publish(self, text: str, level: int):
        print(f"[{self.prefix}: {LogLevel.names[level].capitalize()}] {text}")
