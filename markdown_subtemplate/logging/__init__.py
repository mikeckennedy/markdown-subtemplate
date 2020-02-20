from .log_level import LogLevel
from .stdout_logger import StdOutLogger
from .null_logger import NullLogger
from .subtemplate_logger import SubtemplateLogger

from ..exceptions import MarkdownTemplateException

__log: SubtemplateLogger = StdOutLogger(LogLevel.info)


def get_log() -> SubtemplateLogger:
    return __log


def set_log(log: SubtemplateLogger):
    global __log

    if not log or not isinstance(log, SubtemplateLogger):
        raise MarkdownTemplateException('log')

    __log = log
