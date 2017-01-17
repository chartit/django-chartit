"""
This Django application can be used to create charts and pivot charts
directly from models.
"""
from .chartdata import PivotDataPool, DataPool # noqa
from .charts import PivotChart, Chart # noqa

__version__ = '0.2.9'
