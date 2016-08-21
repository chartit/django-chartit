import inspect
import textwrap
from functools import wraps


def add_source_code_and_doc(f):
    """Instrospects the function and adds source code and the doc string to
    the return parameters.
    """
    @wraps(f)
    def f_with_source_and_doc(request, title, sidebar_items):
        doc = f.__doc__
        if doc is None:
            doc = ""
        else:
            doc = textwrap.dedent(f.__doc__)

        src_lines, num_lines = inspect.getsourcelines(f)
        start_line = end_line = None
        for i, line in enumerate(src_lines):
            if start_line is None or end_line is None:
                if '# start_code' in line:
                    start_line = i+1
                if '# end_code' in line:
                    end_line = i
            else:
                break
        if end_line is None:
            end_line = num_lines - 1
        if start_line is None:
            start_line = 1

        code = ''.join(src_lines[start_line: end_line])
        code = textwrap.dedent(code)
        return f(request, code=code, title=title,
                 doc=doc, sidebar_items=sidebar_items)
    return f_with_source_and_doc
