__author__ = 'gkisel'

import pprint as _pprint
import os

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

_vars = None
_builtin = BuiltIn()


def pprint(data, level='INFO', html=False, console=False, repr=False):
    if not isinstance(data, basestring):
        data = _pprint.pformat(data)
    _builtin.log(data, level, html, console, repr)


def format_string(string, *args, **kwargs):
    logger.debug('Format string {} with {} and {}'.format(string, args, kwargs))
    try:
        result = string.format(*args, **kwargs)
    except KeyError:
        args_copy = list(args)
        kwargs_copy = dict(kwargs)
        for arg in args:
            arg = str(arg)
            if '=' in arg:
                args_copy.remove(arg)
            key, value = arg.split('=', 1)
            kwargs_copy[key.strip()] = value.strip()
        result = format_string(string, *args_copy, **kwargs_copy)
    return result


def find_first_match_in_dict(dictionary, key_name, exact=False, case_sensitive=False):
    return find_matches_in_dict(dictionary, key_name, exact, case_sensitive)[0]


def find_matches_in_dict(dictionary, key_name, exact=False, case_sensitive=False):
    """Return all matches of key_name in the provided dictionary """
    return list(_find_matches_in_dict(dictionary, key_name, exact, case_sensitive))


def find_set_in_dict(dictionary, key_name, exact=False, case_sensitive=False):
    return set(find_matches_in_dict(dictionary, key_name, exact, case_sensitive))


def _find_matches_in_dict(dictionary, key_name, exact=False, case_sensitive=False):
    """Generator that returns all matches of key_name in the provided dictionary """
    if dictionary and not isinstance(dictionary, (basestring, int, long, float, complex)):
        if isinstance(dictionary, list):
            for item in dictionary:
                for result in _find_matches_in_dict(item, key_name, exact):
                    yield result
        else:
            if exact:
                if key_name in dictionary:
                    yield dictionary[key_name]
            else:
                for key in dictionary:
                    if str(key_name).lower().strip() in str(key).lower().strip():
                        yield dictionary[key]
            for key, value in dictionary.items():
                for result in _find_matches_in_dict(value, key_name, exact):
                    yield result


def set_nulls_to_none(dictionary):
    for key, value in dict(dictionary):
        if str(value).lower().strip() == 'null':
            dictionary[key] = None
    return dictionary


def unicode_to_ascii(unicode_data):
    if isinstance(unicode_data, basestring):
        return _unicode_string_to_ascii(unicode_data)
    elif isinstance(unicode_data, dict):
        return _unicode_dictionary_to_ascii(unicode_data)
    elif isinstance(unicode_data, list):
        return _unicode_list_to_ascii(unicode_data)
    return unicode_data


def _unicode_list_to_ascii(unicode_list):
    return [unicode_to_ascii(x) for x in unicode_list]


def _unicode_string_to_ascii(unicode_string):
    return unicode_string.encode('ascii', 'ignore')


def _unicode_dictionary_to_ascii(unicode_dictionary):
    ascii_dictionary = dict()
    for key, value in unicode_dictionary.items():
        key = unicode_to_ascii(key)
        value = unicode_to_ascii(value)
        ascii_dictionary[key] = value
    return ascii_dictionary


def remove_empty_from_dict(dictionary):
    return dict((k, v) for k, v in dictionary.items() if v)


def pformat_nonspecial(dictionary):
    d = {key: value for key, value in dictionary.items() if
         (str(key)[0] != '_' and str(key) != __name__)}
    return _pprint.pformat(d, depth=2)


def reload_vars():
    global _builtin
    global _vars
    try:
        _builtin = BuiltIn()
        _vars = _builtin.get_variables()
    except AttributeError:
        if not _vars:
            _vars = dict()
            _builtin = None
            for key, value in os.environ.items():
                _vars[key] = value
    return _vars


def set_var(var_name, var_value):
    global _vars
    _vars = reload_vars()
    var_name = var_name.strip('${}')
    try:
        _var_name = '${' + str(var_name) + '}'
        _builtin.set_suite_variable(_var_name, var_value)
    except AttributeError:
        _vars[var_name] = var_value


def get_var(var_name, default=None):
    global _vars
    value = None
    _vars = reload_vars()
    var_name = var_name.strip('${}')
    try:
        _var_name = '${' + str(var_name) + '}'
        value = _builtin.get_variable_value(_var_name)
    except AttributeError:
        value = _vars.get(var_name, None)
    return value or default


def clear_suite_vars(exclude=None):
    _vars = reload_vars()
    for var_name in _vars:
        if exclude and any([var_name in _var_name for _var_name in exclude]):
            continue
        set_var(var_name, None)


_vars = reload_vars()
