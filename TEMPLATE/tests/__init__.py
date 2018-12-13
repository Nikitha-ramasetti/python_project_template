import importlib
import unittest
from distutils.version import LooseVersion


def _import_or_skip(modname, minversion=None):
    """Build skip markers for a optional module

    :param str modname:
        Name of the optional module
    :param str minversion:
        Minimum required version
    :return:
        Tuple of

        has_module (bool)
            True if the module is available and >= minversion
        requires_module (decorator)
            Tests decorated with it will only run if the module is available
            and >= minversion
    """
    reason = 'requires %s' % modname
    if minversion:
        reason += '>=%s' % minversion

    try:
        mod = importlib.import_module(modname)
        has = True
    except ImportError:
        has = False
    if (has and minversion
            and LooseVersion(mod.__version__) < LooseVersion(minversion)):
        has = False

    # Do not use pytest.mark.skipif with less than pytest >= 3.6,
    # which fixes pytest#568.
    func = unittest.skipUnless(has, reason=reason)
    return has, func


# TODO: optional dependencies here
has_numpy, requires_numpy = _import_or_skip('numpy')