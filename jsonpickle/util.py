# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 John Paulett (john -at- paulett.org)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Helper functions for pickling and unpickling.  Most functions assist in
determining the type of an object.
"""
import time
import types

from jsonpickle import tags
from jsonpickle.compat import set
from jsonpickle.compat import unicode, long


SEQUENCES = (list, set, tuple)
SEQUENCES_SET = set(SEQUENCES)
PRIMITIVES = set((str, unicode, bool, float, int, long))


def is_type(obj):
    """Returns True is obj is a reference to a type.

    >>> is_type(1)
    False

    >>> is_type(object)
    True

    >>> class Klass: pass
    >>> is_type(Klass)
    True
    """
    return type(obj) is type or type(obj) is types.ClassType


def is_object(obj):
    """Returns True is obj is a reference to an object instance.

    >>> is_object(1)
    True

    >>> is_object(object())
    True

    >>> is_object(lambda x: 1)
    False
    """
    return (isinstance(obj, object) and
            type(obj) is not type and
            type(obj) is not types.FunctionType)


def is_primitive(obj):
    """Helper method to see if the object is a basic data type. Strings,
    integers, longs, floats, booleans, and None are considered primitive
    and will return True when passed into *is_primitive()*

    >>> is_primitive(3)
    True
    >>> is_primitive([4,4])
    False
    """
    if obj is None:
        return True
    elif type(obj) in PRIMITIVES:
        return True
    return False

def is_dictionary(obj):
    """Helper method for testing if the object is a dictionary.

    >>> is_dictionary({'key':'value'})
    True

    """
    return type(obj) is dict

def is_sequence(obj):
    """Helper method to see if the object is a sequence (list, set, or tuple).

    >>> is_sequence([4])
    True

    """
    return type(obj) in SEQUENCES_SET


def is_list(obj):
    """Helper method to see if the object is a Python list.

    >>> is_list([4])
    True
    """
    return type(obj) is list


def is_set(obj):
    """Helper method to see if the object is a Python set.

    >>> is_set(set())
    True
    """
    return type(obj) is set


def is_tuple(obj):
    """Helper method to see if the object is a Python tuple.

    >>> is_tuple((1,))
    True
    """
    return type(obj) is tuple


def is_dictionary_subclass(obj):
    """Returns True if *obj* is a subclass of the dict type. *obj* must be
    a subclass and not the actual builtin dict.

    >>> class Temp(dict): pass
    >>> is_dictionary_subclass(Temp())
    True
    """
    #TODO add UserDict
    return (hasattr(obj, '__class__') and
            issubclass(obj.__class__, dict) and not is_dictionary(obj))


def is_sequence_subclass(obj):
    """Returns True if *obj* is a subclass of list, set or tuple.

    *obj* must be a subclass and not the actual builtin, such
    as list, set, tuple, etc..

    >>> class Temp(list): pass
    >>> is_sequence_subclass(Temp())
    True
    """
    return ((issubclass(obj.__class__, SEQUENCES) or
                is_list_like(obj)) and
            not is_sequence(obj))


def is_noncomplex(obj):
    """Returns True if *obj* is a special (weird) class, that is more complex
    than primitive data types, but is not a full object. Including:

        * :class:`~time.struct_time`
    """
    if type(obj) is time.struct_time:
        return True
    return False


def is_function(obj):
    """Returns true if passed a function

    >>> is_function(lambda x: 1)
    True

    >>> is_function(locals)
    True

    >>> def method(): pass
    >>> is_function(method)
    True

    >>> is_function(1)
    False
    """
    if type(obj) is types.FunctionType:
        return True
    if not is_object(obj):
        return False
    if not hasattr(obj, '__class__'):
        return False
    module = obj.__class__.__module__
    name = obj.__class__.__name__
    return (module == '__builtin__' and
            name in ('function',
                     'builtin_function_or_method',
                     'instancemethod',
                     'method-wrapper'))


def is_module(obj):
    """Returns True if passed a module

    >>> import os
    >>> is_module(os)
    True

    """
    return type(obj) is types.ModuleType


def is_picklable(name, value):
    """Return True if an object cannot be pickled

    >>> import os
    >>> is_picklable('os', os)
    True

    >>> def foo(): pass
    >>> is_picklable('foo', foo)
    False

    """
    if name in tags.RESERVED:
        return False
    return not is_function(value)


def is_installed(module):
    """Tests to see if ``module`` is available on the sys.path

    >>> is_installed('sys')
    True
    >>> is_installed('hopefullythisisnotarealmodule')
    False

    """
    try:
        __import__(module)
        return True
    except ImportError as e:
        return False


def is_list_like(obj):
    return hasattr(obj, '__getitem__') and hasattr(obj, 'append')
