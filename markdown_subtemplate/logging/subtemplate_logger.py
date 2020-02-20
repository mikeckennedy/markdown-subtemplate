import abc


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
