import sys


def fail(message):
    print("FATAL:%s" % message)
    sys.exit(-1)


def is_true(something):
    if isinstance(something, str):
        return something.lower() in ("true", "1", "yes", "on")
    elif isinstance(something, int):
        return something != 0
    else:
        return bool(something)
