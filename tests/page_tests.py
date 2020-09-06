import os

import pytest

from markdown_subtemplate import engine
from markdown_subtemplate import exceptions
from markdown_subtemplate.infrastructure import page
from markdown_subtemplate.storage.file_storage import FileStore

FileStore.set_template_folder(
    os.path.join(os.path.dirname(__file__), 'templates'))


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


def test_variable_replacement_markdown():
    template = os.path.join('home', 'replacements_import.md')
    md = page.get_markdown(template, {'Title': 'Best Title Ever!', 'link': 'https://training.talkpython.fm'})

    text = '''
# This page imports things with data.

We have a paragraph with [a link](https://training.talkpython.fm).

### This page had a title set: Best Title Ever!

And more content with the word TITLE.


And more inline **content**.
'''.strip()
    assert text == md.strip()


def test_two_imports_markdown():
    template = os.path.join('home', 'two_imports.md')
    md = page.get_markdown(template, {})

    text = '''
# This page imports nested things.

We have a paragraph with [a link](https://talkpython.fm).

## This is a basic import.

You'll see imported things.


## This is the second import.

You'll see imported things.


And more inline **content**.
'''.strip()
    assert text == md.strip()


def test_variable_definition_markdown():
    template = os.path.join('home', 'variables.md')
    html = page.get_page(template, {})

    text = '''
<h1>This page defines a variable.</h1>

<p>We have a paragraph with <a href="https://talkpython.fm">a link</a>.</p>

<h3>This page had a title set: Variables rule!</h3>

<p>And more content with the word TITLE.</p>
'''.strip()

    assert text == html.strip()


def test_no_lowercase_replacements_markdown():
    template = os.path.join('home', 'replacements_case_error.md')
    md = page.get_markdown(template, {'title': 'the title', 'link': 'The link'})

    text = '''
# This page imports things with data.

We have a paragraph with [a link]($Link$).

And this was a title: $title$

And more inline **content**.
'''.strip()
    assert text == md.strip()


def test_html_with_replacement():
    template = os.path.join('home', 'replacements_import.md')
    html = engine.get_page(template, {'Title': 'Best Title Ever!', 'link': 'https://training.talkpython.fm'})

    text = '''
<h1>This page imports things with data.</h1>

<p>We have a paragraph with <a href="https://training.talkpython.fm">a link</a>.</p>

<h3>This page had a title set: Best Title Ever!</h3>

<p>And more content with the word TITLE.</p>

<p>And more inline <strong>content</strong>.</p>
'''.strip()
    assert text == html.strip()


def test_html_with_embedded_html():
    template = os.path.join('home', 'markdown_with_html.md')
    html = engine.get_page(template, {})

    text = '''
<h1>This is the basic title</h1>

<p>We have a paragraph with <a href="https://talkpython.fm">a link</a>.</p>

<ul>
<li>Bullet 1</li>
<li>Bullet 2</li>
<li>Bullet 3</li>
</ul>

<p>We also have an image with some details:</p>

<p><a href="http://www.lolcats.com" target="_blank"><img 
class="img img-responsive"
src="http://www.lolcats.com/images/u/11/45/lolcatsdotcom3gp6wm7dw3jihq9t.jpg"></a></p>

<p>End of the message.</p>
'''.strip()
    assert text == html.strip()


def test_missing_import_markdown():
    template = os.path.join('home', 'import_missing.md')
    with pytest.raises(exceptions.TemplateNotFoundException):
        page.get_markdown(template, {'a': 1, 'b': 2})
