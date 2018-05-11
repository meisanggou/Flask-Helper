# !/usr/bin/env python
# coding: utf-8

__author__ = 'meisa'


class UrlRule(object):

    def __init__(self, rule, endpoint=None, view_func=None, **options):
        self.rule = rule
        self.endpoint = endpoint
        self.view_func = view_func
        self.options = options


class UrlRules(object):

    def __init__(self):
        self._rules = []
        self._i = -1
        self.add_url = self.add

    def add(self, url_rule):
        assert isinstance(url_rule, UrlRule)
        self._rules.append(url_rule)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        ur_item = UrlRule(rule, endpoint, view_func, **options)
        self.add(ur_item)

    def __iter__(self):
        return self

    def next(self):
        self._i += 1
        if self._i >= len(self._rules):
            raise StopIteration
        return self._rules[self._i]

    def __getitem__(self, i):
        if i >= len(self._rules):
            raise IndexError("out of index")
        value = self._rules[i]
        return value

    def __len__(self):
        return len(self._rules)


if __name__ == "__main__":
    a1 = UrlRule("/a1")
    a2 = UrlRule("/a2")
    a = UrlRules()
    a.add(a1)
    a.add(a2)
    for item in a:
        print(item.rule)
    print(len(a))