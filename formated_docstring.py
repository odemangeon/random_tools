""" Decorator for Formating doctstrings.
"""


def _formatDostring(*args, **kwargs):
    """ Decorator to put before a function to be able to format it on import.

    >>> from formated_docstring import _formatDostring
    >>> @_formatDostring(__file__=__file__)
    >>> def run_tests(args):
    >>>     '''run tests on methods in {__file__}
    >>>
    >>>     usage: {__file__} --tests
    >>>     '''
    >>>     pass
    """
    def decorator(o):
        o.__doc__ = o.__doc__.format(*args, **kwargs)
        return o

    return decorator

# from
# @_formatDostring(__file__=__file__)
# def run_tests(args):
#     """run tests on methods in {__file__}
#
#     usage: {__file__} --tests
#     """
#     pass
