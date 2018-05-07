def flatten(lst):
    return sum(map(flatten, lst), []) if isinstance(lst, list) else [lst]