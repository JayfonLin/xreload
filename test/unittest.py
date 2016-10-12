#coding:utf-8
"""
Created on 2016-09-20
@author:jeff
"""

import xreload


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





