# -*- coding: utf-8 -*-

"""
"""

# -------------------------------------------------------------------------

import magic

import malwrdb_settings


# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)

# -------------------------------------------------------------------------


def guess_binary_type(sample_binary):
    m = magic.Magic(magic_file=malwrdb_settings.win_magic_path)
    return m.from_buffer(sample_binary)


# -------------------------------------------------------------------------
# ENF OF FILE
# -------------------------------------------------------------------------
