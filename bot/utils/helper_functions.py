def try_get_value(_dict, key, default_val):
    return _dict[key] if key in _dict else default_val