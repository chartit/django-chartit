"""
    utility and helper functions.
"""

from functools import reduce


def _getattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value."""
    if isinstance(obj, dict):
        value = obj[attr]
    else:
        value = reduce(getattr, attr.split('__'), obj)

    # b/c we also support model properties
    if callable(value):
        value = value()

    return value


def _convert_to_rdd(obj):
    """Accepts a dict or a list of dicts and converts it to a
    RecursiveDefaultDict."""
    if isinstance(obj, dict):
        rdd = RecursiveDefaultDict()
        for k, v in obj.items():
            rdd[k] = _convert_to_rdd(v)
        return rdd
    elif isinstance(obj, list):
        rddlst = []
        for ob in obj:
            rddlst.append(_convert_to_rdd(ob))
        return rddlst
    else:
        return obj


class RecursiveDefaultDict(dict):
    """
        Behaves exactly the same as a collections.defaultdict
        but works with pickle.loads. Fixes #10.
    """
    def __init__(self, data=None):
        if data is not None:
            self.data = _convert_to_rdd(data)
            self.update(self.data)
            del self.data

    def __getitem__(self, key):
        # create a default object if this key
        # isn't in the dictionary
        if key not in self.keys():
            item = self.__class__()
            self[key] = item
            return item
        else:
            return super(RecursiveDefaultDict, self).__getitem__(key)

    def __setitem__(self, key, item):
        if not isinstance(item, RecursiveDefaultDict):
            super(RecursiveDefaultDict, self).__setitem__(
                key, _convert_to_rdd(item))
        else:
            super(RecursiveDefaultDict, self).__setitem__(key, item)

    def update(self, element):
        super(RecursiveDefaultDict, self).update(_convert_to_rdd(element))
