from django.db.models.aggregates import Aggregate
from django.db.models.query import QuerySet


def assertOptionDictsEqual(self, first, second):
    if type(first) != type(second):
        msg = "Types don't match %r --> %r" % (type(first), type(second))
        self.fail(msg)
    if len(first) != len(second):
        msg = "Lengths don't match; %r --> %r" % (first, second)
        self.fail(msg)
    if set(first.keys()) != set(second.keys()):
        msg = "Keys don't match %s, %s" % (first.keys(), second.keys())
        self.fail(msg)
    for k1, v1 in first.items():
        v2 = second[k1]
        if isinstance(v1, Aggregate):
            if isinstance(v2, Aggregate):
                if v1.name == v2.name:
                    return
                else:
                    msg = "Aggregates don't match"
                    self.fail(msg)
            else:
                msg = "Aggregate being compared to a Non-aggregate."
                self.fail(msg)
        elif isinstance(v1, QuerySet):
            if isinstance(v2, QuerySet):
                if str(v1.query) == str(v2.query):
                    return
                else:
                    msg = "Querysets don't match"
                    self.fail(msg)
            else:
                msg = "QuerySet being compared to a Non-QuerySet."
                self.fail(msg)
        elif isinstance(v1, dict):
            if isinstance(v2, dict):
                self.assertOptionDictsEqual(v1, v2)
            else:
                msg = "Dict being compared to a Non-dict."
                self.fail(msg)
        else:
            self.assertEqual(v1, v2)
