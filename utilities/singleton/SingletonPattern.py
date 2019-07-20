# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:00:44 2018

@author: Asus
"""

# Singleton/SingletonPattern.py

class ZSingleton:
    class __ZSingleton:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if not ZSingleton.instance:
            ZSingleton.instance = ZSingleton.__ZSingleton(arg)
        else:
            ZSingleton.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)



if __name__ == '__main__':

    x = ZSingleton('sausage')
    print(x.instance)
    y = ZSingleton('eggs')
    print(y.instance)
    z = ZSingleton('spam')
    print(z.instance)
    print(x.instance)
    print(y.instance)
    print(x.val)
    print(x)
    print(y)
    print(z)

#    x = ZSingleton()
#    x.val = 'sausage'
#    print(x)
#    y = ZSingleton()
#    y.val = 'eggs'
#    print(y)
#    z = ZSingleton()
#    z.val = 'spam'
#    print(z)
#    print(x)
#    print(y)


