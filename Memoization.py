import collections
import functools


class Memoized(object):
    """
    The decorator function used to cache return values each time it is called.
    eg: If called later with the same arguments, the cached value is returned (not reevaluated).
    TO DO:  Need to add a way to handle generator instances
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            print "this is an unhashable object: %s" % args
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __get__(self, obj, objtype):
        """
        :param obj:
        :param objtype:
        :return:

        NOTE:  This supports instance methods.
        """
        return functools.partial(self.__call__, obj)

