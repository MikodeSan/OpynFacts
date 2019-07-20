# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 12:33:47 2017

@author: Asus
"""


import sys
import json
import datetime


def load_db(filename):

    db = {}

#    print("\n[json-db] 'load_db' call \n");

    try:
        with open(filename, "r") as myfile:

#            print(myfile)

            try:
                db = json.load(myfile)
                if not db:      # is_empty(db):
                    raise Exception('Database is empty')        #DatabaseEmptyWarning('Database is empty')

            except json.JSONDecodeError as err:
                print("\n# <Exception> ", err.args[0], "\n")
            except Exception as wrn:
                print(wrn)
            except:
                print("\n# <Exception> ", "Unexpected error:", sys.exc_info(), "\n#")
            finally:
#                print("\n[json-db] 'json_load_db' exit \nDataBase: ", db);
                pass

    except FileNotFoundError as err:
        print("\n# <Exception> ", err, "\n")

    return db



def save_db(json_file, db):

#    print("\n[json-db] 'save_db' call \n");

    with open(json_file,"w") as myfile:
#        print(myfile, "my file open w")

        # Convert json to string
        f = json.dumps(db, indent=4, sort_keys=True, cls=ObjectEncoder)
#        f = json.dumps(db, indent=4, sort_keys=True, default=ObjectEncoder().default)
#        print(f)
#        print("json dump")

        # save into file
        myfile.write(f)



class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif hasattr(obj, "to_dict"):
            return obj.to_dict()


        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":

    load_db("conso_data.json")
    load_db("ffhb.json")
