import posixpath

from django import template
from django.utils.safestring import mark_safe
from django.utils import six
from django.conf import settings
import simplejson

from ..charts import Chart, PivotChart

try:
    CHARTIT_JS_REL_PATH = settings.CHARTIT_JS_REL_PATH
    if CHARTIT_JS_REL_PATH[0] == '/':
        CHARTIT_JS_REL_PATH = CHARTIT_JS_REL_PATH[1:]
except AttributeError:
    CHARTIT_JS_REL_PATH = 'chartit/js/'

CHART_LOADER_URL = posixpath.join(settings.STATIC_URL,
                                  CHARTIT_JS_REL_PATH,
                                  'chartloader.js')


def date_format(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


register = template.Library()


@register.filter
def load_charts(chart_list=None, render_to=''):
    """Loads the ``Chart``/``PivotChart`` objects in the ``chart_list`` to the
    HTML elements with id's specified in ``render_to``.

    :Arguments:

    - **chart_list** - a list of Chart/PivotChart objects. If there is just a
      single element, the Chart/PivotChart object can be passed directly
      instead of a list with a single element.

    - **render_to** - a comma separated string of HTML element id's where the
      charts needs to be rendered to. If the element id of a specific chart
      is already defined during the chart creation, the ``render_to`` for that
      specific chart can be an empty string or a space.

      For example, ``render_to = 'container1, , container3'`` renders three
      charts to three locations in the HTML page. The first one will be
      rendered in the HTML element with id ``container1``, the second
      one to it's default location that was specified in ``chart_options``
      when the Chart/PivotChart object was created, and the third one in the
      element with id ``container3``.

    :returns:

    - a JSON array of the HighCharts Chart options. Also returns a link
      to the ``chartloader.js`` javascript file to be embedded in the webpage.
      The ``chartloader.js`` has a jQuery script that renders a HighChart for
      each of the options in the JSON array"""

    embed_script = (
        '<script type="text/javascript">\n'
        'var _chartit_hco_array = %s;\n</script>\n'
        '<script src="%s" type="text/javascript">\n</script>')

    if chart_list is not None:
        if isinstance(chart_list, (Chart, PivotChart)):
            chart_list = [chart_list]
        chart_list = [c.hcoptions for c in chart_list]
        render_to_list = [s.strip() for s in render_to.split(',')]
        for hco, render_to in six.moves.zip_longest(chart_list, render_to_list):
            if render_to:
                hco['chart']['renderTo'] = render_to
        embed_script = (embed_script % (simplejson.dumps(chart_list,
                                                         use_decimal=True,
                                                         default=date_format),
                                        CHART_LOADER_URL))
    else:
        embed_script = embed_script % ((), CHART_LOADER_URL)
    return mark_safe(embed_script)
