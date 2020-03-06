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

If you want to change the storage engine, just create a base class of `markdown_subtemplate.storage.SubtemplateStorage`. It's an abstract class so just implement the abstract methods.

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

    def get_shared_markdown(self, import_name: str) -> Optional[str]:
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

By default, `markdown-subtemplate` will cache generated markdown and HTML in memory. This often is fine.  If you do nothing, this will happen automatically and your page generation will be much faster if you reuse content or request it more than once.

But web environments typically have many processes serving their content. For example, at [Talk Python Training](https://training.talkpython.fm/) we currently have 8-10 uWSGI worker processes running in parallel. 

In this situation, caching all the content in memory has a few drawbacks.
* All content is cached in memory 10x what it would normally cost.
* Content that has to be generated, which can be much slower, is done 10x as often.
* Restarting the server for a new version of code requires everything to be regenerated 10x again making startup slow.
* Clearing the cache, if wanted, is effectively impossible (how to you cleanly signal all 10 processes exactly once?)

In these situations, storing the cache content in a database or Redis would be better. At Talk Python, we use MongoDB as the backing cache store. 

Below are two examples. They follow the pattern:

1. Create an entity to store in the DB for cache data
2. Create a base class of `markdown_subtemplate.caching.SubtemplateCache`
3. Override the abstract methods
4. Register your caching engine with `markdown-subtemplate` at startup.

### SQLAlchemy Cachine Engine:

**First, create the entity to store in the DB**.

```python
class MarkdownCache(SqlAlchemyBase):
    __tablename__ = 'markdown_cache'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    key = sa.Column(sa.String, index=True)
    type = sa.Column(sa.String, index=True)
    name = sa.Column(sa.String, index=True)
    contents = sa.Column(sa.String)

    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
```

**Second, implement the caching engine**:

```python
from markdown_subtemplate import caching
class MarkdownSubTemplateDBCache(caching.SubtemplateCache):
    def get_html(self, key: str) -> caching.CacheEntry:
        session = DbSession.create()

        cache_entry = session.query(MarkdownCache).filter(
            MarkdownCache.key == key, MarkdownCache.type == 'html'
        ).first()

        session.close()

        return cache_entry

    def add_html(self, key: str, name: str, html_contents: str) -> caching.CacheEntry:
        session = DbSession.create()

        item = self.get_html(key)
        if not item:
            item = MarkdownCache()
            session.add(item)

        item.type = 'html'
        item.key = key
        item.name = name
        item.contents = html_contents

        if html_contents:
            session.commit()

        session.close()

        # Not technical a base class, but duck-type equivalent.
        # noinspection PyTypeChecker
        return item

    def get_markdown(self, key: str) -> caching.CacheEntry:
        session = DbSession.create()

        cache_entry = session.query(MarkdownCache).filter(
            MarkdownCache.key == key, MarkdownCache.type == 'markdown'
        ).first()

        session.close()

        return cache_entry

    def add_markdown(self, key: str, name: str, markdown_contents: str) -> caching.CacheEntry:
        session = DbSession.create()

        item = self.get_markdown(key)
        if not item:
            item = MarkdownCache()
            session.add(item)

        item.type = 'markdown'
        item.key = key
        item.name = name
        item.contents = markdown_contents

        if markdown_contents:
            session.commit()
        session.close()

        # Not technical a base class, but duck-type equivalent.
        # noinspection PyTypeChecker
        return item

    def clear(self):
        session = DbSession.create()

        for entry in session.query(MarkdownCache):
            session.delete(entry)

        session.commit()

    def count(self) -> int:
        session = DbSession.create()
        count = session.query(MarkdownCache).count()
        session.close()

        return count
```

One minor oddity is the return value is `caching.CacheEntry` whereas that's not the real return value. But the SQLAlchemy entity does implement every field that is present in `CacheEntry`, so duck typing and all that.

**Finally, register the new caching engine at process startup**.

```python
from markdown_subtemplate import caching

cache = MarkdownSubTemplateDBCache()
caching.set_cache(cache)
```

### MongoDB Cachine Engine:

Using MongoDB as a backing store for the cache is basically the same as SQLAlchemy in principle. We'll be using MongoEngine.

**First, create the entity to store in the DB**.

```python
import mongoengine as me

class CmsCache(me.Document):
    key: str = me.StringField(required=True)
    type: str = me.StringField(required=True)
    name: str = me.StringField()
    contents: str = me.StringField(required=True)
    created_date: datetime.datetime = me.DateTimeField(default=datetime.now)

    meta = {
        'db_alias': 'core',
        'collection': 'cms_cache',
        'indexes': [
            {'fields': ['key', 'type']},
            'key',
            'type',
            'name',
            'created_date',
        ],
        'ordering': ['-created_date']
    }
```

**Second, implement the caching engine**:

```python
class MarkdownSubTemplateMongoDBCache(SubtemplateCache):
    def get_html(self, key: str) -> CacheEntry:
        return CmsCache.objects(key=key, type='html').first()

    def add_html(self, key: str, name: str, html_contents: str) -> CacheEntry:
        item = self.get_html(key)
        if item:
            return item

        item = CmsCache()
        item.type = 'html'
        item.key = key
        item.name = name
        item.contents = html_contents
        item.save()

        # Not technical a base class, but duck-type equivalent.
        # noinspection PyTypeChecker
        return item

    def get_markdown(self, key: str) -> CacheEntry:
        return CmsCache.objects(key=key, type='markdown').first()

    def add_markdown(self, key: str, name: str, markdown_contents: str) -> CacheEntry:
        item = self.get_markdown(key)
        if item:
            return item

        item = CmsCache()
        item.type = 'markdown'
        item.key = key
        item.name = name
        item.contents = markdown_contents
        item.save()

        # Not technical a base class, but duck-type equivalent.
        # noinspection PyTypeChecker
        return item

    def clear(self):
        CmsCache.objects().delete()

    def count(self) -> int:
        return CmsCache.objects().count()
```

One minor oddity is the return value is `caching.CacheEntry` whereas that's not the real return value. But the MongoEngine entity does implement every field that is present in `CacheEntry`, so duck typing and all that.

**Finally, register the new caching engine at process startup**.

```python
from markdown_subtemplate import caching

cache = MarkdownSubTemplateMongoDBCache()
caching.set_cache(cache)
```


## Logging

By default, `markdown-subtemplate` will log to standard out using `print()` and log level `INFO` from the builtin `StdOutLogger` class. 

You can change the log level by using the `markdown_subtemplate.logging.LogLevel` class:

```python
# Change logging level from default LogLevel.info to LogLevel.error

log = logging.get_log()
log.log_level == LogLevel.info
```

You can disable logging by setting it's level to `LogLevel.off`.

If you use a logging framework, you likely want to direct log messages through that framework. So you can, like the above two subsystems, implement a class based on an abstract base class.

Let's log through a preconfigured [Logbook](https://logbook.readthedocs.io/en/stable/) setup (which goes to stdout in dev and rotating files in prod).

**First, create a base class**:

```python
import logbook
import markdown_subtemplate
from markdown_subtemplate.logging import LogLevel

class MarkdownLogger(markdown_subtemplate.logging.SubtemplateLogger):
    def __init__(self, log_level: int):
        super().__init__(log_level)
        self.logbook_logger = logbook.Logger("Markdown Templates")

    def verbose(self, text: str):
        if not self.should_log(LogLevel.verbose, text):
            return

        self.logbook_logger.trace(text)

    def trace(self, text: str):
        if not self.should_log(LogLevel.trace, text):
            return

        self.logbook_logger.trace(text)

    def info(self, text: str):
        if not self.should_log(LogLevel.info, text):
            return

        self.logbook_logger.info(text)

    def error(self, text: str):
        if not self.should_log(LogLevel.error, text):
            return

        self.logbook_logger.error(text)
```

That's pretty straightforward. But do be sure to check at each level whether you should log as we do with:

```python
if not self.should_log(LEVEL, text):
    return
```

Finally, register this logging engine at process startup:

```python
From markdown_subtemplate import logging

log = MarkdownLogger(LogLevel.info) # Set the level you want
logging.set_log(log)
```
