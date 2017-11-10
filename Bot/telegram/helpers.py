import inspect


def func_args(frame):
    args, _, _, values = inspect.getargvalues(frame)
    format_values = {}
    for arg in args:
        if arg != 'self':
            format_values[arg] = values[arg]
    return format_values
