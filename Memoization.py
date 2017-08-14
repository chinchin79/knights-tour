import collections
import functools
from itertools import tee
from types import GeneratorType


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


Tee = tee([], 1)[0].__class__


def memoized_generator(f):
    cache = {}

    def ret(*args):
        if args not in cache:
            cache[args] = f(*args)
        if isinstance(cache[args], (GeneratorType, Tee)):
            # the original can't be used any more,
            # so we need to change the cache as well
            cache[args], r = tee(cache[args])
            return r
        return cache[args]
    return ret


def generator_memoize(func):
    def inner(arg):
        if isinstance(arg, list):
            # Make arg immutable
            arg = tuple(arg)
        if arg in inner.cache:
            print "Using cache for %s" % repr(arg)
            for i in inner.cache[arg]:
                yield i
        else:
            print "Building new for %s" % repr(arg)
            temp = []
            for i in func(arg):
                temp.append(i)
                yield i
            inner.cache[arg] = temp
    inner.cache = {}
    return inner
