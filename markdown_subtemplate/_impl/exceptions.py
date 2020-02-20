class MarkdownTemplateException(Exception):
    pass


class ArgumentExpectedException(MarkdownTemplateException):
    pass


class InvalidOperationException(MarkdownTemplateException):
    pass


class PathException(MarkdownTemplateException):
    pass


class TemplateNotFoundException(PathException):
    def __init__(self, template_path):
        super().__init__(f'Template not found: {template_path}.')


