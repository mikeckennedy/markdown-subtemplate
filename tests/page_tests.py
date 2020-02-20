import os

import pytest

from markdown_subtemplate import exceptions
from markdown_subtemplate import engine
# noinspection PyProtectedMember
from markdown_subtemplate._impl import page

template_folder = os.path.join(os.path.dirname(__file__), 'templates')
engine.set_template_folder(template_folder)


def test_missing_template_by_file():
    with pytest.raises(exceptions.TemplateNotFoundException):
        engine.get_page(os.path.join('home', 'hiding.md'), {})


def test_missing_template_by_folder():
    with pytest.raises(exceptions.TemplateNotFoundException):
        engine.get_page(os.path.join('hiding', 'index.md'), {})


def test_empty_template():
    html = engine.get_page(os.path.join('home', 'empty_markdown.md'), {})
    assert html == ''


def test_basic_markdown_template():
    template = os.path.join('home', 'basic_markdown.md')
    md = page.get_markdown(template, {'a': 1, 'b': 2})

    text = '''
# This is the basic title

We have a paragraph with [a link](https://talkpython.fm).

* Bullet 1
* Bullet 2
* Bullet 3

'''.strip()
    assert text == md.strip()


def test_basic_markdown_html():
    template = os.path.join('home', 'basic_markdown.md')
    html = engine.get_page(template, {'a': 1, 'b': 2})

    text = '''
<h1>This is the basic title</h1>

<p>We have a paragraph with <a href="https://talkpython.fm">a link</a>.</p>

<ul>
<li>Bullet 1</li>
<li>Bullet 2</li>
<li>Bullet 3</li>
</ul>
'''.strip()
    assert text == html.strip()


def test_import_markdown():
    template = os.path.join('home', 'import1.md')
    md = page.get_markdown(template, {'a': 1, 'b': 2})

    text = '''
# This page imports one thing.

We have a paragraph with [a link](https://talkpython.fm).

## This is a basic import.

You'll see imported things.


And more inline **content**.
'''.strip()
    assert text == md.strip()


def test_nested_import_markdown():
    template = os.path.join('home', 'import_nested.md')
    md = page.get_markdown(template, {'a': 1, 'b': 2})

    text = '''
# This page imports nested things.

We have a paragraph with [a link](https://talkpython.fm).

### This page imports stuff and is imported.

## This is a basic import.

You'll see imported things.


And more nested import content.

And more inline **content**.
'''.strip()
    assert text == md.strip()


def test_missing_import_markdown():
    template = os.path.join('home', 'import_missing.md')
    with pytest.raises(exceptions.TemplateNotFoundException):
        page.get_markdown(template, {'a': 1, 'b': 2})
