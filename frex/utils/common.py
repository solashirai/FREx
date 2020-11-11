import functools


def rgetattr(obj, attr, *args):
    """
    Get an attribute of an object, allowing for the target attribute to be an attribute of some sub-object.
    """
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split('.'))
