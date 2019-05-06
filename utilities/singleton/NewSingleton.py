# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:00:44 2018

@author: Asus
"""

# Singleton/NewSingleton.py

class ZSingleton(object):
    class __ZSingleton:
        def __init__(self):
            self.val = None
        def __str__(self):
            return `self` + self.val
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not ZSingleton.instance:
            ZSingleton.instance = ZSingleton.__ZSingleton()
        return ZSingleton.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)



if __name__ == '__main__':

    x = ZSingleton()
    x.val = 'sausage'
    print(x)
    y = ZSingleton()
    y.val = 'eggs'
    print(y)
    z = ZSingleton()
    z.val = 'spam'
    print(z)
    print(x)
    print(y)


