from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer, ClassNotFound

register = template.Library()


def generate_pygments_css(path=None):
    if path is None:
        import os
        path = os.path.join(os.getcwd(), 'pygments.css')
    f = open(path, 'w')
    f.write(HtmlFormatter().get_style_defs('.highlight'))
    f.close()


def get_lexer(value, arg):
    if arg is None:
        return guess_lexer(value)
    return get_lexer_by_name(arg)


@register.filter(name='colorize')
@stringfilter
def colorize(value, arg=None):
    try:
        return mark_safe(highlight(value, get_lexer(value, arg),
                                   HtmlFormatter()))
    except ClassNotFound:
        return value


@register.filter(name='colorize_table')
@stringfilter
def colorize_table(value, arg=None):
    try:
        return mark_safe(highlight(value, get_lexer(value, arg),
                                   HtmlFormatter(linenos='table')))
    except ClassNotFound:
        return value
