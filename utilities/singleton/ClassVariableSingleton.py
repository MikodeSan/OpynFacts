# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:00:44 2018

@author: Asus
"""

# Singleton/ClassVariableSingleton.py
class SingleTone(object):
    __instance = None
    def __new__(cls, val):
        if SingleTone.__instance is None:
            SingleTone.__instance = object.__new__(cls)
        SingleTone.__instance.val = val
        return SingleTone.__instance


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

#    x = OnlyOne()
#    x.val = 'sausage'
#    print(x)
#    y = OnlyOne()
#    y.val = 'eggs'
#    print(y)
#    z = OnlyOne()
#    z.val = 'spam'
#    print(z)
#    print(x)
#    print(y)


