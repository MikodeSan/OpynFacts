# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:00:44 2018

@author: Asus
"""

# Singleton/BorgSingleton.py
# Alex Martelli's 'Borg'

class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class Singleton(Borg):
    def __init__(self, arg):
        Borg.__init__(self)
        self.val = arg
    def __str__(self): return self.val


if __name__ == '__main__':

    x = Singleton('sausage')
    print(x)
    y = Singleton('eggs')
    print(y)
    z = Singleton('spam')
    print(z)
    print(x)
    print(y)
    print(`x`)
    print(`y`)
    print(`z`)