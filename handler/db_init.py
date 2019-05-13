# -*- coding: utf-8 -*-

"""

1. 初始化MongoDB的某些表, 以及设置一些值:
    - 从 db_schema.txt 中加载
    - 以 "覆盖添加" 的方式 - col.find_one_and_

2. 具体内容:
    - col_host_os                     : {"platform": xx, "version": xx, "sp": xx, "arch": xx}
    - col_file_type                   : {"name": xx, "desc": xx}
    - col_platform                    : {"name": xx, "desc": xx}
    - col_sample_relationship         : {"name": xx, "desc": xx}
    - col_overall_malicious_type      : {"name": xx, "desc": xx}
    - col_malware_family              : {"name": xx, "desc": xx}

    - col_programing_lang             : {"name": xx, "desc": xx}
    - col_function_type               : {"name": xx, "desc": xx}
    - col_sys_behv_type               : {"name": xx, "desc": xx}
    - col_feature_behv_type           : {"name": xx, "desc": xx}
"""


import os
import json
from mongoengine import *
from malwrdb_models import *
from malwrdb_settings import *
from db_util import *
from db_connect import db_connect


# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)


# -------------------------------------------------------------------------


default_stuff = {

    # -------------------------------------------------------------------------
    # 数据

    "host_os": [
        {"platform": "windows", "version": "xp", "sp": 3, "arch": "x86", "desc": "WinXP Sp3 x86"},
        {"platform": "windows", "version": "7", "sp": 1, "arch": "x86", "desc": "Win7 Sp1 x86"},
        {"platform": "windows", "version": "7", "sp": 1, "arch": "x64", "desc": "Win7 Sp1 x64"},
    ],

    # -------------------------------------------------------------------------
    # 中英对照

    "file_types": [
        {"name": "exe", "desc": "PE 可执行文件"},
        {"name": "dll", "desc": "PE 动态链接库文件"},
    ],
    "platforms": [
        {"name": "windows", "desc": ""},
        {"name": "linux", "desc": ""},
    ],
    "sample_relationships": [
        {"name": "unpack", "desc": "脱壳"},
        {"name": "dump", "desc": "内存转储"},
        {"name": "report", "desc": "分析报告"},
        {"name": "note", "desc": "分析笔记"},
    ],
    "overall_malicious_types": [
        {"name": "trojan", "desc": "木马"},
        {"name": "downloader", "desc": "下载者"},
    ],
    "malware_families": [
        {"name": "wannacry", "desc": "勒索软件Wannacry"},
    ],
    "programing_lang": [
        {"name": "C#", "desc": ""},
    ],
    "function_types": [
        {"name": "library", "desc": "库函数"},
        {"name": "standard", "desc": "标准"},
    ],
    "proc_behv_types": [
        {"name": "create", "desc": "创建进程"},
    ],
    "sys_behv_types": [
        {"name": "detect_os_version", "desc": "检查系统版本"},
    ],
    "feature_behv_types": [
        {"name": "anti_vm", "desc": "反虚拟机"},
    ],
}


if __name__ == "__main__":

    # -------------------------------------------------------------------------
    # 从文件加载配置，并补全

    file = r"db_default.json"
    is_replace_file = False
    if os.path.exists(file) and os.path.getsize(file) != 0:

        log("loading from file: %s ..." % file)

        # 从配置文件加载
        with open(file) as f:
            stuff = json.load(f)
        # 用默认补全
        for (k, v) in default_stuff.items():
            if k not in stuff:

                log("adding key %s to stuff, item count: %d" % (k, len(v)))

                stuff[k] = v
                is_replace_file = True
    else:
        # 设置为默认
        log("setting default as stuff ...")
        stuff = default_stuff
        is_replace_file = True

    # 替换配置文件
    if is_replace_file:

        log("replacing config file %s ..." % file)

        if os.path.exists(file):
            os.remove(file)
        # 写入文件
        with open(file, "w") as f:
            f.write(json.dumps(stuff, ensure_ascii=False, indent=4))

    # -------------------------------------------------------------------------

    # 连接数据库
    db_connect()

    log("init database start ...")

    # -------------------------------------------------------------------------
    # 数据

    # 主机类型
    host_os = stuff["host_os"]
    for os_ in host_os:
        check_insert_host_os(os_)

    # -------------------------------------------------------------------------
    # 中英对照

    # 文件类型
    file_types = stuff["file_types"]
    for file_type in file_types:
        check_insert_file_type(file_type)

    # 平台
    platforms = stuff["platforms"]
    for platform in platforms:
        check_insert_platform(platform)

    # 样本父子关系
    sample_relationships = stuff["sample_relationships"]
    for relationship in sample_relationships:
        check_insert_sample_relationship_type(relationship)

    # 总体的恶意类型
    overall_malicious_types = stuff["overall_malicious_types"]
    for type_ in overall_malicious_types:
        check_insert_overall_malicious_type(type_)

    # 恶意代码家族
    malware_families = stuff["malware_families"]
    for family in malware_families:
        check_insert_malware_family(family)

    # 编程语言
    programing_lang = stuff["programing_lang"]
    for lang in programing_lang:
        check_insert_programing_lang(lang)

    # 函数类型
    function_types = stuff["function_types"]
    for type_ in function_types:
        check_insert_function_type(type_)

    # 进程行为
    proc_behv_types = stuff["proc_behv_types"]
    for type_ in proc_behv_types:
        check_insert_proc_behv_type(type_)

    # 系统行为
    sys_behv_types = stuff["sys_behv_types"]
    for type_ in sys_behv_types:
        check_insert_sys_behv_type(type_)

    # 综合行为
    feature_behv_types = stuff["feature_behv_types"]
    for type_ in feature_behv_types:
        check_insert_behv_feature_type(type_)

    # -------------------------------------------------------------------------

    log("init database finish...")


# -------------------------------------------------------------------------
# ENF OF FILE
# -------------------------------------------------------------------------
