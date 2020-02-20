# Talk Python Training Example

This project was extracted from an internal CMS built to power [Talk Python Training](https://training.talkpython.fm/)'s landing pages, for example, [this one](https://training.talkpython.fm/courses/explore_100days_web/100-days-of-web-in-python).

We have lots of sections on our landing pages that are repeated. Hence the ability to import them into the landing page is very helpful. If you visit the page:

[https://training.talkpython.fm/courses/explore_100days_web/100-days-of-web-in-python](https://training.talkpython.fm/courses/explore_100days_web/100-days-of-web-in-python)

The sections from **What's this course about and how is it different?** to **The time to act is now** are generated with content similar to below.

## 100-web.md (top level page)

```markdown
## What's this course about and how is it different?

100 days of code isn’t just about the time commitment. 
**The true power is in utilising that time effectively 
with a tailored set of projects**. That’s why we have 24 
practical projects, each paired with 20-60 minute video 
lessons at the beginning of the project.

Just a small sampling of the projects you’ll work on include:

* Create your very own Static Site
* ...
* Web Scraping with BeautifulSoup4 and newspaper3k
* And 17 more projects!

View the full [course outline](#course_outline).
...

## Who is this course for?

This course is for **anyone who knows the basics of Python and 
wants to push themselves into the world of Python Web Development 
for 100 days with hands-on projects**.
...

[IMPORT TRANSCRIPTS]
## Who we are and why should you take our course?

**Meet Michael Kennedy:**

[IMPORT MICHAEL]

**Meet Bob Belderbos:**

[IMPORT BOB_B]

**Meet Julian Sequeira:**

[IMPORT JULIAN_S]

[IMPORT OFFICE_HOURS]

[IMPORT PYTHON_3_STATEMENT]

## The time to act is now

The **#100DaysOfCode** challenge is an epic adventure. 
Don't got it alone. Take our course and we'll
 be your guide with both lessons and projects. 
```


## transcripts.md (imported section)

```markdown
## Follow along with subtitles and transcripts

Each course comes with subtitles and full transcripts.
The transcripts are available as a separate searchable page for
each lecture. They also are available in course-wide search results
to help you find just the right lecture.

<p>
<img src="/static/img/landing/subtitles.jpg"
     class="img img-responsive"
     style="padding-left: 25px;"
     alt="Each course has subtitles available in the video player.">
</p>
```

## Explore course Chameleon template

The template contents are show in the larger context of the site via:

```html
... explore_course.pt:[]() main contents, nav, etc. ...
<div>
    ${structure:contents}
</div>
```

These templates are rendered with `markdown_subtemplate` using this code:

```python
# contents returned as part of the model/dictionary from Pyramid.
contents = markdown_subtemplate.engine.get_page('100-web.md', {})
```

## Other details

This site is using two custom extensibility points. First, we are using a wrapper around the logging to integrate with [logbook](https://logbook.readthedocs.io/en/stable/). Secondly, we have a custom cache provider that is backed by MongoDB rather than in-memory. This allows us to reset the cache and have effects across our scaled out web worker processes.

