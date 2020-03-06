# Extensibility

`markdown-subtemplate` has three axis of extensibility:

* **Storage** - Load markdown content from disk, db, or elsewhere.
* **Caching** - Cache generated markdown and HTML in memory, DB, or you pick!
* **Logging** - If you are using a logging framework, plug in logging messages from the library.

## Storage

Out of the box, `markdown-subtemplate` will load markdown files from a structure directory:

```
TEMPLATE_FOLDER
   |
   |- shared
       | - contact.md
       | - social.md
   |- home             # arbitrary organizing directories
       | - index.md    # Use template_path: home/index.md
       | - about.md
```

This is implemented by the `markdown_subtemplate.storage.file_storage.FileStore` class. It must be configured as follows:

```python
from markdown_subtemplate.storage.file_storage import FileStore
folder = FULL_PATH_TO-TEMPLATE_FOLDER
FileStore.set_template_folder(folder)
```

If you want to configure the storage engine, just create a base class of `markdown_subtemplate.storage.SubtemplateStorage`. It's an abstract class so just implement the abstract methods.

Here is an example from SQLAlchemy. Define a model to read/write data:

```python
# SQLAlchemy entity class:
class MarkdownPage(SqlAlchemyBase):
    __tablename__ = 'markdown_pages'

    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String, index=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    is_shared = sa.Column(sa.Boolean, index=True, default=False)
    text = sqlalchemy.Column(sa.String)
```

Then implement the storage engine class:

```python
class MarkdownSubTemplateDBStorage(storage.SubtemplateStorage):
    def get_markdown_text(self, template_path: str) -> Optional[str]:
        if not template_path:
            return None

        template_path = template_path.strip().lower()
        session = DbSession.create() # Method to generate a SQLAlchemy session.

        mk: MarkdownPage = session.query(MarkdownPage) \
            .filter(MarkdownPage.id == template_path) \
            .first()

        session.close()

        if not mk:
            return None

        return mk.text

    def get_shared_markdown(self, import_name) -> Optional[str]:
        if not import_name:
            return None

        import_name = import_name.strip().lower()
        session = DbSession.create()

        mk: MarkdownPage = session.query(MarkdownPage) \
            .filter(MarkdownPage.name == import_name, MarkdownPage.is_shared == True) \
            .first()

        session.close()

        if not mk:
            return None

        return mk.text

    def is_initialized(self) -> bool:
        # Check whether connection string, etc set in SQLAlchemy
        return True

    def clear_settings(self):
        pass
```

Of course, you'll need a way to enter these into the DB but that's technically outside of the content of this discussion. 

Finally, you'll need to set this storage engine as the implementation at process startup:

```python
from markdown_subtemplate import storage

store = MarkdownSubTemplateDBStorage()
storage.set_storage(store)
```

## Caching

## Logging



