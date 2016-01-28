"""
This Django application can be used to create charts and pivot charts
directly from models.
"""
from .chartdata import PivotDataPool, DataPool
from .charts import PivotChart, Chart

__version__ = '0.2.2'
