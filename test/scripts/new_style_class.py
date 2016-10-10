
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
    