import os
from typing import Optional, List

from markdown_subtemplate.exceptions import TemplateNotFoundException, ArgumentExpectedException, \
    InvalidOperationException
from . import SubtemplateStorage


class FileStore(SubtemplateStorage):
    __template_folder: Optional[str] = None

    def get_markdown_text(self, template_path) -> str:
        if not template_path or not template_path.strip():
            raise TemplateNotFoundException("No template file specified: template_path=''.")

        file_name = os.path.basename(template_path)
        file_parts = os.path.dirname(template_path).split(os.path.sep)
        folder = FileStore.get_folder(file_parts)
        full_file = os.path.join(folder, file_name).lower()

        if not os.path.exists(full_file):
            raise TemplateNotFoundException(full_file)

        with open(full_file, 'r', encoding='utf-8') as fin:
            return fin.read()

    def get_shared_markdown(self, import_name):
        folder = FileStore.get_folder(['_shared'])
        file = os.path.join(folder, import_name.strip().lower() + '.md')

        if not os.path.exists(file):
            raise TemplateNotFoundException(file)

        with open(file, 'r', encoding='utf-8') as fin:
            return fin.read()

    def is_initialized(self) -> bool:
        return bool(FileStore.__template_folder)

    @staticmethod
    def get_folder(path_parts: List[str]) -> str:
        if not path_parts:
            raise ArgumentExpectedException('path_parts')

        if not FileStore.__template_folder:
            raise InvalidOperationException("You must set the template folder before calling this method.")

        parts = [
            p.strip().strip('/').strip('\\').lower()
            for p in path_parts
        ]
        parent_folder = os.path.abspath(FileStore.__template_folder)
        folder = os.path.join(parent_folder, *parts)

        return folder

    @staticmethod
    def set_template_folder(full_path: str):
        from ..exceptions import PathException
        import markdown_subtemplate.logging as logging
        log = logging.get_log()

        test_path = os.path.abspath(full_path)
        if test_path != full_path:
            msg = f"{full_path} is not an absolute path."
            log.error("engine.set_template_folder: " + msg)
            raise PathException(msg)

        if not os.path.exists(full_path):
            msg = f"{full_path} does not exist."
            log.error("engine.set_template_folder: " + msg)
            raise PathException(msg)

        if not os.path.isdir(full_path):
            msg = f"{full_path} is not a directory."
            log.error("engine.set_template_folder: " + msg)
            raise PathException(msg)

        log.info(f"Template folder set: {full_path}")

        FileStore.__template_folder = full_path

    def clear_settings(self):
        FileStore.__template_folder = None
