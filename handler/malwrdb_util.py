# -*- coding: utf-8 -*-

"""
"""

# -------------------------------------------------------------------------


import json
import string


# -------------------------------------------------------------------------
# util -


# 字符转换


def convert_char(char):
    if char in string.ascii_letters or \
       char in string.digits or \
       char in string.punctuation or \
       char in string.whitespace:
        return char
    else:
        return r'\x%02x' % ord(char)


def convert_to_printable(s):
    return ''.join([convert_char(c) for c in s])


# 字符串相似性比较


def diff_string(str1, str2):
    pass


# -------------------------------------------------------------------------
# util -

def ssdeep_hash(binary):
    pass


# -------------------------------------------------------------------------
# util - proto


def proto_msg_to_json_dict(msg):
    """
        将定义的 proto message 转换为 json, 用于创建 mongoengine.Document
    """
    from google.protobuf.json_format import MessageToJson
    json_str = MessageToJson(msg, including_default_value_fields=True, preserving_proto_field_name=True)
    json_dict = json.loads(json_str)
    return json_dict


# -------------------------------------------------------------------------
# ENF OF FILE
# -------------------------------------------------------------------------
