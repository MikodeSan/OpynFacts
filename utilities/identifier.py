# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 12:49:16 2018

@author: Asus
"""



class ZIdentifier(object):


    __ID_BASE = 0
    __N_INSTANCE = 0
    _ID_DEFAULT = -1


    @classmethod
    def init_n_transaction(cls, init_id):

        success = True
        if init_id >= cls.__ID_BASE:
            cls.__N_INSTANCE = init_id
        else:
            success = False

        return success


    def __init__(self, new_id=-1):

        self._label = ''
        self.__id = ZIdentifier._ID_DEFAULT
        self.__id_lst = list()
#        self.__set_id(new_id)

#    def __set_id(self, new_id=-1):
#
#        # Set new instance id.
#        if new_id < self.__ID_BASE:
#
#            self.__id = self.__N_INSTANCE
#            self.__N_INSTANCE += 1
#        else:
#            self.__id = new_id

    @property
    def value(self):
        return self.__id

    @property
    def next_value(self):
        id_cur = self.__id
#        self.__set_id()
        self.__id_lst.append(id_cur)
        self.__inc()
        return id_cur

#    @id_next.setter
#    def id_next(self, value):
    def set_next(self, value):

        if value >= self.__ID_BASE:
            if value not in self.__id_lst:
                if value > self.__id:

                    self.__id = value
                else:
#                    print('error')
                    pass
            else:
#                print('error')
                pass
        else:
#            print('error')
            pass

    def init_id_list(self, object_lst, init_id):

        # find max id. value
        id_lst = self.__id_lst
        n_id = 0
        cur_id = 0
        id_next = init_id

        # Get event id list
        for obj_dict in object_lst:

            if '_id' in obj_dict:
                cur_id = obj_dict['_id']

                if cur_id >= self.__ID_BASE:

                    if cur_id not in id_lst:
                        id_lst.append(cur_id)
                        n_id += 1
                        if cur_id >= id_next:
                            id_next = cur_id + 1

                    else:
                        obj_dict['_id'] *= -10
                        # EXCEPTION
                else:
                    obj_dict['_id'] = -3
            else:
                obj_dict['_id'] = self._ID_DEFAULT

        id_lst.sort()
        if id_next > self.__id:
            self.__id = id_next

        print('\nN id.(s)', n_id, '; id. list:', id_lst, '; db next id.', init_id, '; next id.', id_next, '\n')


        # fix id
        for obj_dict in object_lst:

            cur_id = obj_dict['_id']

#            if cur_id < self.__ID_BASE:
            if cur_id == self._ID_DEFAULT or cur_id == -3:

                obj_dict['_id'] = self.next_value


    def __inc(self):

        # Set new instance id.
        self.__id += 1


class ZIdentifier_0(ZIdentifier):

    __ID_BASE = 1000000
    __N_INSTANCE = 1000000

    def __init__(self, arg=-1):

        super().__init__(arg)


class ZIdentifier_1(ZIdentifier):

    __ID_BASE = 2000000
    __N_INSTANCE = 2000000

    def __init__(self, arg=-1):

        super().__init__(arg)



if __name__ == '__main__':

#    ZIdentifier.init_n_transaction()

    print('Class name:', ZIdentifier.__name__)
    z_id = ZIdentifier(0)
    print(z_id.next_value)
    print(z_id.next_value)
    z_id.set_next(26)
    print(z_id.next_value)
    print(z_id.next_value)
    z_id.set_next(0)
    print(z_id.next_value)
    z_id.set_next(1)
    print(z_id.next_value)
    z_id.set_next(26)
    print(z_id.next_value)
    z_id.set_next(45)
    print(z_id.next_value)
#    print(z_id.next_value)
#    y = ZIdentifier_0()
###    y.val = 'eggs'
#    print(y.next_value)
#    print(y.next_value)
#    print(y.next_value)
#    y = ZIdentifier_0()
#    print(y.next_value)
#    print(y.next_value)
#    print(y.next_value)
#    print(y._argm)
#    z = ZIdentifier_1(0)
##    z.val = 'spam'
#    print(z._argm)
#    print(z_id._argm)
#    print(y._argm)


