import abc


class SubtemplateStorage(abc.ABC):
    @abc.abstractmethod
    def get_markdown_text(self, template_path) -> str:
        pass

    @abc.abstractmethod
    def get_shared_markdown(self, import_name) -> str:
        pass

    @abc.abstractmethod
    def is_initialized(self) -> bool:
        pass

    @abc.abstractmethod
    def clear_settings(self):
        pass
