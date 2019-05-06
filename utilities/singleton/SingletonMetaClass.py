# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:00:44 2018

@author: Asus
"""
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

##Python2
#class MyClass(BaseClass):
#    __metaclass__ = Singleton

#Python3
#class MyClass(BaseClass, metaclass=Singleton):
#    pass

# Singleton/SingletonMetaClass.py
class SingletonMetaClass(type):

    def __init__(cls,name,bases,dict):

        super(SingletonMetaClass,cls).__init__(name,bases,dict)
        original_new = cls.__new__
        def my_new(cls,*args,**kwds):

            if cls.instance == None:
                cls.instance = original_new(cls,*args,**kwds)
            return cls.instance

        cls.instance = None
        cls.__new__ = staticmethod(my_new)

class bar(object):
    __metaclass__ = SingletonMetaClass
    def __init__(self,val):
        self.val = val
    def __str__(self):
        return repr(self) + self.val

if __name__ == '__main__':

    x=bar('sausage')
    y=bar('eggs')
    z=bar('spam')
    print(x)
    print(y)
    print(z)
    print(x is y is z)
#
#    x = ZSingleton('sausage')
#    print(x.instance)
#    y = ZSingleton('eggs')
#    print(y.instance)
#    z = ZSingleton('spam')
#    print(z.instance)
#    print(x.instance)
#    print(y.instance)
#    print(x.val)
#    print(x)
#    print(y)
#    print(z)

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


