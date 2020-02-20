from .log_level import LogLevel
from .stdout_logger import StdOutLogger
from .null_logger import NullLogger
from .subtemplate_logger import SubtemplateLogger

# log: SubtemplateLogger = NullLogger()
log: SubtemplateLogger = StdOutLogger(LogLevel.info)
