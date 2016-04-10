"""Doctests for module reloading.

>>> import xreload
>>> import test_xreload
>>>
>>> test_xreload.make_mod_x()
>>> import x
>>> C = x.C
>>> C_foo = C.foo
>>> C_bar = C.bar
>>> C_stomp = C.stomp
>>> C_instance = C()
>>> C_instance_foo = C_instance.foo
>>>
>>> C_foo(C_instance)
42
>>> C_bar()
42 42
>>> C_stomp()
42 42 42
>>> C_instance.foo()
42
>>> C_instance_foo()
42
>>>
>>> test_xreload.make_mod_x(repl="42", subst="24")
>>> xreload.xreload(x)
<module 'x' (built-in)>
>>>
>>> C_foo(C_instance)
24
>>> C_bar()
24 24
>>> C_stomp()
24 24 24
>>> C_instance.foo()
24
>>> C_instance_foo()
24
>>>
>>>
>>> test_xreload.make_mod_y()
>>> import y
>>> D = y.D
>>> D_foo = D.foo
>>> D_bar = D.bar
>>> D_stomp = D.stomp
>>> D_instance = D()
>>> D_instance_foo = D_instance.foo
>>>
>>> D_foo(D_instance)
42
>>> D_bar()
42 42
>>> D_stomp()
42 42 42
>>> D_instance.foo()
42
>>> D_instance_foo()
42
>>>
>>> test_xreload.make_mod_y(repl="42", subst="24")
>>> xreload.xreload(y)
<module 'y' (built-in)>
>>>
>>> D_foo(D_instance)
24
>>> D_bar()
24 24
>>> D_stomp()
24 24 24
>>> D_instance.foo()
24
>>> D_instance_foo()
24
>>> print y.g_except
1
>>>
>>> make_mod_y_except()
>>> xreload.xreload(y)
<module 'y' (built-in)>
>>> print y.g_except
1

"""

SAMPLE_CODE_X = """
class C:
    def foo(self):
        print 42
    @classmethod
    def bar(cls):
        print 42, 42
    @staticmethod
    def stomp():
        print 42, 42, 42
"""

SAMPLE_CODE_Y = """
class D(object):
    def foo(self):
        print 42
    @classmethod
    def bar(cls):
        print 42, 42
    @staticmethod
    def stomp():
        print 42, 42, 42

g_except = 1


"""

SAMPLE_CODE_Y_EXCEPTION = """
class D(object):
    def foo(self):
        print 42
    @classmethod
    def bar(cls):
        print 42, 42
    @staticmethod
    def stomp():
        print 42, 42, 42

g_except = e


"""

import os
import sys
import shutil
import doctest
import xreload
import tempfile
from test.test_support import run_unittest

tempdir = None
save_path = None


def setUp(unused=None):
    global tempdir, save_path
    tempdir = tempfile.mkdtemp()
    save_path = list(sys.path)
    sys.path.append(tempdir)


def tearDown(unused=None):
    global tempdir, save_path
    if save_path is not None:
        sys.path = save_path
        save_path = None
    if tempdir is not None:
        shutil.rmtree(tempdir)
        tempdir = None
        

def make_mod_x(name="x", repl=None, subst=None):
    if not tempdir:
        setUp()
        assert tempdir
    fn = os.path.join(tempdir, name + ".py")
    f = open(fn, "w")
    sample = SAMPLE_CODE_X
    if repl is not None and subst is not None:
        sample = sample.replace(repl, subst)
    try:
        f.write(sample)
    finally:
        f.close()


def make_mod_y(name="y", repl=None, subst=None):
    if not tempdir:
        setUp()
        assert tempdir
    fn = os.path.join(tempdir, name + ".py")
    f = open(fn, "w")
    sample = SAMPLE_CODE_Y
    if repl is not None and subst is not None:
        sample = sample.replace(repl, subst)
    try:
        f.write(sample)
    finally:
        f.close()


def make_mod_y_except(name="y", repl=None, subst=None):
    if not tempdir:
        setUp()
        assert tempdir
    fn = os.path.join(tempdir, name + ".py")
    f = open(fn, "w")
    sample = SAMPLE_CODE_Y_EXCEPTION
    if repl is not None and subst is not None:
        sample = sample.replace(repl, subst)
    try:
        f.write(sample)
    finally:
        f.close()


def test_suite():
    return doctest.DocTestSuite(setUp=setUp, tearDown=tearDown)


def test_main():
    run_unittest(test_suite())

if __name__ == "__main__":
    test_main()
