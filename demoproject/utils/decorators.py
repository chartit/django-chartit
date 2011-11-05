import inspect
import os
import textwrap

from functools import wraps

from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe


def rstfy(value):
    try:
        from docutils.core import publish_parts
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Cannot rstfy. The Python " 
            "docutils library isn't installed.")
        return force_unicode(value)
    else:
        parts = publish_parts(source=smart_str(value), writer_name="html4css1")
        return (mark_safe(force_unicode(parts["title"])), 
                mark_safe(force_unicode(parts["fragment"])))

def get_docstring_and_code(func, f_file):
    with open(os.path.abspath( __file__ )) as f:
        all_code = f.readlines()
        for i, line in enumerate(all_code):
            if 'def ' in line and func in line:
                func_start = i
                break
            
        for i, line in enumerate(all_code[func_start:]):
            if '#start_code' in line:
                code_start = func_start+i+1
                break
        
        for i, line in enumerate(all_code[code_start:]):
            if '#end_code' in line:
                code_end = code_start+i
                break
        
        indent = None
        clean_code = []
        after_whitespace = False
        code = all_code[code_start:code_end]
        
        for line in code[:]:
            if not after_whitespace:
                if not line.strip():
                    pass
                else:
                    indent = len(line) - len(line.strip()) - 1
                    clean_code.append(line[indent:])
                    after_whitespace = True
            else:
                if not line.strip():
                    clean_code.append(line)
                else:
                    clean_code.append(line[indent:])
    return ''.join(clean_code)

def add_source_code_and_doc(f):
    @wraps(f)
    def f_with_source_and_doc(request, title, sidebar_items, 
                              *args, **kwargs):
        
        doc = f.__doc__
        if doc is None:
            doc = ""
        else:
            doc = textwrap.dedent(f.__doc__)
        
        src_lines, num_lines = inspect.getsourcelines(f)
        start_line = end_line = None
        for i, line in enumerate(src_lines):
            if start_line is None or end_line is None: 
                if '#start_code' in line:
                    start_line = i+1
                if '#end_code' in line:
                    end_line = i
            else:
                break
        if end_line is None:
            end_line = num_lines - 1
        if start_line is None:
            start_line = 1
            
        code = ''.join(src_lines[start_line: end_line])   
        code = textwrap.dedent(code)
        return f(request, code = code, title = title,
                 doc = doc, sidebar_items = sidebar_items)
    return f_with_source_and_doc
        
