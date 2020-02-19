import os
from typing import Optional

from markdown_subtemplate.exceptions import MarkdownTemplateException

__template_folder: Optional[str] = None


def set_template_folder(full_path: str):
    global __template_folder

    test_path = os.path.abspath(full_path)
    if test_path != full_path:
        raise MarkdownTemplateException(f"{full_path} is not an absolute path.")

    if not os.path.exists(full_path):
        raise MarkdownTemplateException(f"{full_path} does not exist.")

    if not os.path.isdir(full_path):
        raise MarkdownTemplateException(f"{full_path} is not a directory.")

    __template_folder = full_path
