# -*- coding: utf-8 -*-

"""
"""

# -------------------------------------------------------------------------


from mongoengine import *
from malwrdb_settings import *


# -------------------------------------------------------------------------


def db_connect():
    """可以重复调用, 木有关系"""
    connect(mongo_db_name, host=mongo_host, port=mongo_port)
    connect(mongo_local_db_name, alias=mongo_local_db_name, host=mongo_host, port=mongo_port)


# -------------------------------------------------------------------------
# ENF OF FILE
# -------------------------------------------------------------------------
