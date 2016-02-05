
def add_decorator(*targets, **kwargs):
    decorator = kwargs.pop('decorator', None)
    if decorator is None:
        raise ValueError('The decorator must be defined')
    args = tuple(map(decorator, targets))
    if len(args) == 1:
        return args[0]
    return args
