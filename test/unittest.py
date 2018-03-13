#coding:utf-8
"""
Created on 2016-09-20
@author:jeff
"""

import xreload
import pytest
import types


def setup_module(module):
    import os
    make_dir_cmd = "mkdir scripts"
    os.system(make_dir_cmd)

    touch_initpy_cmd = "touch scripts/__init__.py"
    os.system(touch_initpy_cmd)

def teardown_module(module):
    import os
    cmd = "rm -rf scripts"
    os.system(cmd)

def ReplaceScripts(file_name, content):
    f = open(file_name, "w")

    try:
        f.write(content)
    finally:
        f.close()

def test_function():

    origin_file = \
    """
def Foo():
    return 13579
    """

    new_file = \
    """
def Foo():
    return 97531
    """

    file_name = "scripts/functions.py"
    ReplaceScripts(file_name, origin_file)
    import scripts.functions
    module = scripts.functions

    assert module.Foo() == 13579

    ReplaceScripts(file_name, new_file)
    xreload.xreload(module.__name__)
    assert module.Foo() == 97531

def test_new_style_class():

    origin_file = \
    """
class Operate(object):
    def __init__(self, x, y):
        self.m_x = x
        self.m_y = y

    def add(self):
        return self.m_x + self.m_y + 1

    @classmethod
    def minus(cls, x, y):
        return x - y

    @staticmethod
    def multiply(x, y):
        return x * y

    def to_bo_delete_method(self):
        pass
    """

    new_file = \
    """
class Operate(object):
    def __init__(self, x, y):
        self.m_x = x
        self.m_y = y

    def add(self):
        return self.m_x + self.m_y

    @classmethod
    def minus(cls, x, y):
        return y - x

    @staticmethod
    def multiply(x, y):
        return x * y * 2

    def divide(self):
        return self.m_x / self.m_y
    """

    file_name = "scripts/new_style_class.py"
    ReplaceScripts(file_name, origin_file)
    import scripts.new_style_class
    module = scripts.new_style_class

    x = 17
    y = 3

    op = module.Operate(x, y)
    assert op.add() == 21
    assert module.Operate.minus(x, y) == 14
    assert module.Operate.multiply(x, y) == 51
    assert hasattr(module.Operate, "to_bo_delete_method")

    Operate_instance_add = op.add
    Operate_minus = module.Operate.minus
    Operate_multiply = module.Operate.multiply

    ReplaceScripts(file_name, new_file)
    xreload.xreload(module.__name__)

    new_op = module.Operate(x, y)

    assert Operate_instance_add == op.add

    assert op.add() == 20
    assert Operate_minus(x, y) == -14
    assert Operate_multiply(x, y) == 102
    assert op.divide() == 5
    assert not hasattr(module.Operate, "to_bo_delete_method")


def test_classic_class():

    origin_file = \
    """
class Operate:
    def __init__(self, x, y):
        self.m_x = x
        self.m_y = y

    def add(self):
        return self.m_x + self.m_y + 1

    @classmethod
    def minus(cls, x, y):
        return x - y

    @staticmethod
    def multiply(x, y):
        return x * y
    """

    new_file = \
    """
class Operate:
    def __init__(self, x, y):
        self.m_x = x
        self.m_y = y

    def add(self):
        return self.m_x + self.m_y

    @classmethod
    def minus(cls, x, y):
        return y - x

    @staticmethod
    def multiply(x, y):
        return x * y * 2

    def divide(self):
        return self.m_x / self.m_y
    """

    file_name = "scripts/classic_class.py"
    ReplaceScripts(file_name, origin_file)
    import scripts.classic_class
    module = scripts.classic_class

    x = 17
    y = 3

    op = module.Operate(x, y)
    assert op.add() == 21
    assert module.Operate.minus(x, y) == 14
    assert module.Operate.multiply(x, y) == 51

    Operate_instance_add = op.add
    Operate_minus = module.Operate.minus
    Operate_multiply = module.Operate.multiply

    ReplaceScripts(file_name, new_file)
    xreload.xreload(module.__name__)

    new_op = module.Operate(x, y)

    assert Operate_instance_add == op.add

    assert op.add() == 20
    assert Operate_minus(x, y) == -14
    assert Operate_multiply(x, y) == 102
    assert op.divide() == 5

def test_global_values():

    origin_file = \
    """
g_user_table = {}
def LoadUsers():
    global g_user_table
    g_user_table[1234] = 'Alice'
    g_user_table[5678] = 'Bob'

manager = None
def GetManagerInstance():
    global manager
    if not manager:
        manager = "God"
    return manager

CONSTANT_VALUE = "I don't know"
    """

    new_file = \
    """
g_user_table = {}
def LoadUsers():
    global g_user_table
    g_user_table[1234] = 'Alice'
    g_user_table[5678] = 'Bob'

manager = None
def GetManagerInstance():
    global manager
    if not manager:
        manager = "God"
    return manager

CONSTANT_VALUE = 31415926  # compare to its origin value which is a different type, string
    """

    file_name = "scripts/global_values.py"
    ReplaceScripts(file_name, origin_file)
    import scripts.global_values
    module = scripts.global_values

    module.LoadUsers()
    module.GetManagerInstance()

    assert module.g_user_table != {}
    assert module.manager is not None
    assert module.CONSTANT_VALUE == "I don't know"

    ReplaceScripts(file_name, new_file)
    xreload.xreload(module.__name__)

    assert module.g_user_table != {}
    assert module.manager is not None
    assert module.CONSTANT_VALUE == 31415926

def test_pyc():
    import os
    import py_compile

    import scripts.new_style_class
    path = "scripts/new_style_class.py"
    py_compile.compile(path)
    os.remove(path)
    assert not os.path.exists(path)
    pyc_path = path+'c'
    assert os.path.exists(pyc_path)

    xreload.xreload("scripts.new_style_class")
    op = scripts.new_style_class.Operate(1, 1)


def skip_test_derived_class():

    origin_file = """
class A(object):
    def __init__(self):
        pass

class B(A):
    def __init__(self):
        super(B, self).__init__()


    """

    new_file = """
class A(object):
    def __init__(self):
        pass

class B(A):
    def __init__(self):
        super(B, self).__init__()

class C(B):
    def __init__(self):
        super(C, self).__init__()


def Foo():
    a = A()
    b = B()
    c = C()

    """

    other_file = """

class E(object):
    def __init__(self):
        super(E, self).__init__()

    """

    other_new_file = """
import base_derived_classes

class E(object):

    def __init__(self):
        super(E, self).__init__()

class D(base_derived_classes.B, E):
    def __init__(self):
        super(D, self).__init__()

def Foo():
    b = base_derived_classes.B()
    d = D()
    """


    file_name = "scripts/base_derived_classes.py"
    ReplaceScripts(file_name, origin_file)
    import scripts.base_derived_classes

    other_name = "scripts/other.py"
    ReplaceScripts(other_name, other_file)
    import scripts.other

    module = scripts.base_derived_classes
    ReplaceScripts(file_name, new_file)
    ReplaceScripts(other_name, other_new_file)

    xreload.xreload(module.__name__)
    xreload.xreload(scripts.other.__name__)

    module.Foo()
    scripts.other.Foo()

def test_after_slot_class():
    origin_file = """
class A(object):
    def __init__(self, member):
        self.m_member = member

    def Foo(self):
        pass
    """

    new_file = """
class A(object):
    __slots__ = ["m_member", "Foo"]
    def __init__(self, member):
        self.m_member = member

    def Foo(self):
        pass
    """

    file_name = "scripts/after_slot_class.py"
    ReplaceScripts(file_name, origin_file)
    import scripts.after_slot_class

    ReplaceScripts(file_name, new_file)

    with pytest.raises(Exception, match=r'__slots__.*before.*after modified'):
        xreload.xreload(scripts.after_slot_class.__name__)

def test_before_slot_class():
    origin_file = """
class A(object):
    __slots__ = ["m_member", "Foo"]
    def __init__(self, member):
        self.m_member = member

    def Foo(self):
        pass
    """

    new_file = """
class A(object):
    def __init__(self, member):
        self.m_member = member

    def Foo(self):
        pass
    """
    

    file_name = "scripts/before_slot_class.py"
    ReplaceScripts(file_name, origin_file)
    import scripts.before_slot_class

    ReplaceScripts(file_name, new_file)

    with pytest.raises(Exception, match=r'__slots__.*before.*after modified'):
        xreload.xreload(scripts.before_slot_class.__name__)


def test_slots_update_class():
    origin_file = """
class A(object):
    __slots__ = ["m_member", "Foo", "DeleteMethod"]

    def __init__(self):
        self.m_member = 1

    def Foo(self):
        return 'before'

    def DeleteMethod(self):
        pass
    """

    new_file = """
class A(object):
    __slots__ = ["m_member", "Foo", "Bar"]

    def __init__(self):
        self.m_member = 2

    def Foo(self):
        return 'after'

    @classmethod
    def Bar(cls):
        pass
    """

    file_name = "scripts/slots_update_class.py"
    ReplaceScripts(file_name, origin_file)
    import scripts.slots_update_class
    module = scripts.slots_update_class

    assert hasattr(module.A, 'DeleteMethod')
    assert isinstance(module.A.DeleteMethod, types.MethodType)
    assert hasattr(module.A, 'Foo')
    assert hasattr(module.A, 'm_member')

    ReplaceScripts(file_name, new_file)
    xreload.xreload(module.__name__)

    assert hasattr(module.A, 'Foo')
    assert isinstance(module.A.Foo, types.MethodType)
    a = module.A()
    assert a.m_member == 2
    assert a.Foo() == 'after'

    assert hasattr(module.A, 'Bar') 
    assert isinstance(module.A.__dict__['Bar'], classmethod)
    assert not hasattr(module.A, 'DeleteMethod')
    assert hasattr(module.A, 'm_member')







