# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 13:00:44 2018

@author: Asus
"""

class ZSingleton(object):

#    class __ZSingleton:
#
#        def __init__(self, arg):
#            self.val = arg
#
#        def __str__(self):
#            return 'methode str' +  repr(self) + self.val
#
##        def __repr__(self):
##
##            return 'methode repr' + repr(self) + self.val



    __instance = None

    def __new__(cls, val):

        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        cls.__instance.val = val
        return cls.__instance


#    def __init__(self, arg=0):
    #
    #        if not ZSingleton.__instance:
    #            ZSingleton.__instance = ZSingleton.__ZSingleton(arg)
    #        else:
    #            ZSingleton.__instance.val = arg

#    def __new__(cls): # __new__ always a classmethod
#            if not ZSingleton.__instance:
#                ZSingleton.__instance = ZSingleton.__ZSingleton()
#            return ZSingleton.__instance

        def __str__(self):
            return 'methode str' +  repr(self) + self.val

#        def __repr__(self):
#
#            return 'methode repr' + repr(self) + self.val

#    def __getattr__(self, name):
#        return getattr(self.__instance, name)

#    def __setattr__(self, name):
#        return setattr(self.__instance, name)


if __name__ == '__main__':

    x = ZSingleton('sausage')
    print(x)
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


