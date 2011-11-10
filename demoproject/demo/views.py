from django.shortcuts import render_to_response, redirect
from demoproject.utils.decorators import add_source_code_and_doc

@add_source_code_and_doc
def demohome(request, title, code, doc, sidebar_items):
    """
    Welcome to the Django-Chartit Demo. This demo has a lot of sample charts 
    along with the code to help you get familiarized with the Chartit API. 
    
    The examples start with simple ones and get more and  more complicated. 
    The latter examples use concepts explained in the examples earlier. So if 
    the source code of a particular chart looks confusing, check to see if any 
    details have already been explained in a previous example. 
    
    The models that the examples are based on are explained in Model Details.
    
    The raw data for all the models is available as a ``SQLite3`` database 
    file `here <../../static/db/chartitdemodb>`_. You can download the file 
    and use `SQLiteBrowser <http://sqlitebrowser.sourceforge.net/>`_ 
    to look at the raw data.
    
    Thank you and have fun exploring! 
    """
    return render_to_response('demohome.html', 
                              {'chart_list': None,
                               'code': None,
                               'title': title,
                               'doc': doc,
                               'sidebar_items': sidebar_items})