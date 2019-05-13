# -*- coding: utf-8 -*-

"""
"""

# -------------------------------------------------------------------------

_host = "192.168.0.114"

mongo_db_name_base = "malwrdb"

# mongo_host = "192.168.99.100"
mongo_host = _host
mongo_port = 27017
mongo_db_name = mongo_db_name_base                                  # 主要数据库
mongo_local_db_name = mongo_db_name_base + "_local"                 # 存储本地化信息数据库

# mongo_test_host = "192.168.99.100"
mongo_test_host = _host
mongo_test_port = 27017
mongo_test_db_name = mongo_db_name_base + "_test"                   # 测试数据库


# redis_host = "192.168.99.100"
redis_host = _host
redis_port = 6378

win_magic_path = r"D:\_path\magic_misc\magic"
win_peid_signature_path = r"F:\abc\__malware_db\userdb.txt"


# win_magic_path =

# this_host = "tcp://192.168.0.106:6677"
this_host = "tcp://127.0.0.1:6677"  # 只能用本地测试


# -------------------------------------------------------------------------
# END OF FILE -------------------------------------------------------------
# -------------------------------------------------------------------------
