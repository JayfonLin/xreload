
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
    