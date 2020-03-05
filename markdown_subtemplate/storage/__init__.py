from markdown_subtemplate.exceptions import ArgumentExpectedException
from markdown_subtemplate.storage.subtemplate_storage import SubtemplateStorage
from markdown_subtemplate.storage import file_storage

__storage: SubtemplateStorage = None


def set_storage(storage_instance: SubtemplateStorage):
    global __storage
    if not storage_instance or not isinstance(storage_instance, SubtemplateStorage):
        raise ArgumentExpectedException('storage_instance')

    __storage = storage_instance


def get_storage() -> SubtemplateStorage:
    global __storage
    if not __storage:
        from markdown_subtemplate.storage.file_storage import FileStore
        __storage = FileStore()
    return __storage


def is_initialized() -> bool:
    return get_storage().is_initialized()
