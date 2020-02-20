import abc


class LogLevel:
    verbose = 0
    trace = 1
    info = 2
    error = 3

    names = {
        0: 'verbose',
        1: 'trace',
        2: 'info',
        3: 'error'
    }


class SubtemplateLogger(abc.ABC):

    def __init__(self, log_level: int):
        self.log_level = log_level

    @abc.abstractmethod
    def verbose(self, text: str):
        pass

    @abc.abstractmethod
    def trace(self, text: str):
        pass

    @abc.abstractmethod
    def info(self, text: str):
        pass

    @abc.abstractmethod
    def error(self, text: str):
        pass

    def should_log(self, level: int, text: str) -> bool:
        return self.log_level <= level and (text and text.strip())


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


# log: SubtemplateLogger = NullLogger()
log: SubtemplateLogger = StdOutLogger(LogLevel.info)
