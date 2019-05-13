# -*- coding: utf-8 -*-

"""
"""

# -------------------------------------------------------------------------


from __future__ import print_function
from __future__ import unicode_literals


import traceback
from datetime import datetime


from malwrdb_models import LogLine
# from malwrdb_settings import


# -------------------------------------------------------------------------


lvel_dict = {
    "INFO": 1,
    "DEBUG": 2,
    "WARN": 3,
    "ERROR": 4,
}


# -------------------------------------------------------------------------


def _log(file, level, info, is_print=True):

    if is_print:
        print("[%s] - %s" % (level, info))

    # try:
    #     l = LogLine()
    #     l.file = file
    #     l.level = lvel_dict[level]
    #     l.info = info
    #     l.time = datetime.now()
    #     l.save()
    # except:
    #     traceback.print_exc()


# -------------------------------------------------------------------------
# END OF FILE
# -------------------------------------------------------------------------
