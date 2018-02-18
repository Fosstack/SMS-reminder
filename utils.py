def log_it(function):
    def wrapper(*args, **kwargs):
        # [ass]
        return function(*args, **kwargs)

    return wrapper
