import os
import datetime
from typing import Dict, Optional, Any, List

from markdown_subtemplate import caching as __caching, storage
from markdown_subtemplate.infrastructure import markdown_transformer
from markdown_subtemplate.exceptions import ArgumentExpectedException, TemplateNotFoundException
from markdown_subtemplate import logging as __logging
from markdown_subtemplate.storage import SubtemplateStorage


# noinspection DuplicatedCode
def get_page(template_path: str, data: Dict[str, Any]) -> str:
    if not template_path or not template_path.strip():
        raise ArgumentExpectedException('template_path')

    template_path = template_path.strip().lower()

    cache = __caching.get_cache()
    log = __logging.get_log()

    key = f'html: {template_path}'
    entry = cache.get_html(key)
    if entry:
        log.trace(f"CACHE HIT: Reusing {template_path} from HTML cache.")
        contents = entry.contents

        # Is there data that needs to be folded in? Process it.
        if data:
            contents = process_variables(contents, data)

        # Return the cached data, no need to transform for variables.
        return contents

    t0 = datetime.datetime.now()

    # Get the markdown with imports and substitutions
    markdown = get_markdown(template_path)
    # Convert markdown to HTML
    html = get_html(markdown)

    cache.add_html(key, key, html)
    html = process_variables(html, data)

    dt = datetime.datetime.now() - t0

    msg = f"Created contents for {template_path}:{data} in {int(dt.total_seconds() * 1000):,} ms."
    log.info(f"GENERATING HTML: {msg}")

    return html


def get_html(markdown_text: str, unsafe_data=False) -> str:
    html = markdown_transformer.transform(markdown_text, unsafe_data)
    return html


# noinspection DuplicatedCode
def get_markdown(template_path: str, data: Dict[str, Any] = None) -> str:
    if data is None:
        data = {}

    cache = __caching.get_cache()
    log = __logging.get_log()

    key = f'markdown: {template_path}'
    entry = cache.get_markdown(key)
    if entry:
        log.trace(f"CACHE HIT: Reusing {template_path} from MARKDOWN cache.")
        if not data:
            return entry.contents
        else:
            return process_variables(entry.contents, data)

    t0 = datetime.datetime.now()

    text = load_markdown_contents(template_path)
    cache.add_markdown(key, key, text)
    if data:
        text = process_variables(text, data)

    dt = datetime.datetime.now() - t0

    msg = f"Created contents for {template_path} in {int(dt.total_seconds() * 1000):,} ms."
    log.trace(f"GENERATING MARKDOWN: {msg}")

    return text


def load_markdown_contents(template_path: str) -> Optional[str]:
    if not template_path:
        return ''

    log = __logging.get_log()
    log.verbose(f"Loading markdown template: {template_path}")

    landing_md = get_page_markdown(template_path)
    if not landing_md:
        return ''

    lines = landing_md.split('\n')
    lines = process_imports(lines)

    final_markdown = "\n".join(lines).strip()

    return final_markdown


def get_page_markdown(template_path: str) -> Optional[str]:
    if not template_path or not template_path.strip():
        raise TemplateNotFoundException("No template file specified: template_path=''.")

    store: SubtemplateStorage = storage.get_storage()
    return store.get_markdown_text(template_path)


def get_shared_markdown(import_name: str) -> Optional[str]:
    if not import_name or not import_name.strip():
        raise ArgumentExpectedException('import_name')

    store: SubtemplateStorage = storage.get_storage()
    return store.get_shared_markdown(import_name)


def process_imports(lines: List[str]) -> List[str]:
    log = __logging.get_log()
    line_data = list(lines)

    for idx, line in enumerate(line_data):
        if not line.strip().startswith('[IMPORT '):
            continue

        import_statement = line.strip()
        import_name = import_statement \
            .replace('[IMPORT ', '') \
            .replace(']', '') \
            .strip()

        imported_file = os.path.join('_shared', import_name + '.md')
        log.verbose(f"Loading import: {imported_file}...")

        markdown = get_page_markdown(imported_file)
        markdown_lines = markdown.split('\n')
        line_data = line_data[:idx] + markdown_lines + line_data[idx + 1:]

        return process_imports(line_data)

    return line_data


def process_variables(raw_text: str, data: Dict[str, Any]) -> str:
    if not raw_text:
        return raw_text

    log = __logging.get_log()

    keys = list(data.keys())
    key_placeholders = {
        key: f"${key.strip().upper()}$"
        for key in keys
        if key and isinstance(key, str)
    }

    transformed_text = raw_text
    for key in keys:
        if key_placeholders[key] not in transformed_text:
            continue

        log.verbose(f"Replacing {key_placeholders[key]}...")
        transformed_text = transformed_text.replace(key_placeholders[key], str(data[key]))

    return transformed_text
