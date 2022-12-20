import argparse
import copy
from argparse import Namespace


def dict2ns(dict_obj):
    """
    Convert recursively dict to Namespace object.
    """
    dict_obj = copy.deepcopy(dict_obj)
    temp = Namespace(**dict_obj)
    for k, v in dict_obj.items():
        if isinstance(v, dict):
            temp.__setattr__(k, dict2ns(v))
    return temp


def ns2dict(namespace):
    """
    Convert recursively Namespace object to dict.
    """
    namespace = copy.deepcopy(namespace)
    temp = vars(namespace)
    for k, v in temp.items():
        if isinstance(v, Namespace):
            temp[k] = ns2dict(v)
    return temp


class NestedParser:
    def __init__(self, parser, names, prefixes):
        self.parser = parser
        self.names = names
        self.prefixes = prefixes

    def add_argument(self, name, **kwargs):
        if name.startswith('--'):
            name, dashes = name[2:], '--'
        elif name.startswith('-'):
            name, dashes = name[1:], '-'
        else:
            dashes = ''
        return self.parser.add_argument(dashes + '.'.join(list(self.prefixes) + [name]),
                                        dest='.'.join(list(self.names) + [name]), **kwargs)

    def parse_args(self):
        def recursive(dt, names, val):
            name0 = names[0]
            if len(names) == 1:
                dt[name0] = val
                return
            else:
                if name0 not in dt:
                    dt[name0] = {}
                recursive(dt[name0], names[1:], val)

        dict_in = vars(self.parser.parse_args())
        # print(dict_in)
        dict_out = {}
        for k, v in dict_in.items():
            name_list = k.split('.')
            recursive(dict_out, name_list, v)

        return dict2ns(dict_out)

    def get_child(self, name, prefix):
        return NestedParser(self.parser, list(self.names) + [name], list(self.prefixes) + [prefix])

    @staticmethod
    def new():
        return NestedParser(argparse.ArgumentParser(), (), ())
