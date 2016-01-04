from collections import defaultdict


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


class RecursiveDefaultDict(defaultdict):
    """The name says it all.
    """
    def __init__(self, data=None):
        self.default_factory = type(self)
        if data is not None:
            self.data = _convert_to_rdd(data)
            self.update(self.data)
            del self.data

    def __getitem__(self, key):
        return super(RecursiveDefaultDict, self).__getitem__(key)

    def __setitem__(self, key, item):
        if not isinstance(item, RecursiveDefaultDict):
            super(RecursiveDefaultDict, self).__setitem__(key,
                                                          _convert_to_rdd(item))
        else:
            super(RecursiveDefaultDict, self).__setitem__(key, item)

    def update(self, element):
        super(RecursiveDefaultDict, self).update(_convert_to_rdd(element))
