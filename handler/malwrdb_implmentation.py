# -*- coding: utf-8 -*-

"""

1. 所有的 key 都用小写
2. 数据转换:
   如果发送的是 json dict:
       会先转为 json string, 再转为 proto message.
       如果功能是直接添加数据库, 会再把 proto message 转为 json string, 再转为 json dict, 再转为 mongoengine.Document
       - 好在这种情况不多???
   如果发送的是 proto message:
       ...
   总之, 要把 proto message 转换为 mongoengine.Document, 貌似就必须得经过 json string/json dict???
   TODO: mongoengine.Document.from_proto_message(msg), 省掉那个过程

"""

# -------------------------------------------------------------------------

import os
import hashlib

# from google.protobuf.json_format import MessageToJson

from malwrdb_util import *
from malwrdb_models import *
from db_util import *

import analyze_magic
import analyze_pe
# import analyze_elf
# import analyze_idb


# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)


def log_ii(interface_name, msg, info=None, is_print=True, level="DEBUG"):
    # log_interface_invoke
    if info is None:
        log("[INTERFACE-Invoke] - interface: %s, msg: %s" % (interface_name, msg), is_print=is_print, level=level)
    else:
        log("[INTERFACE-Invoke] - interface: %s, msg: %s, info: %s" % (interface_name, msg, info), is_print=is_print, level=level)


# -------------------------------------------------------------------------
# db


def sample_check_or_insert(sample_binary):
    """
    检查 sample 的 sha256, 没有则插入, 有则返回数据库中的 Sample
    """
    sha256 = hashlib.sha256(sample_binary).hexdigest()

    q = Sample.objects(sha256=sha256)

    if q.count() == 0:
        sample = Sample()
        sample._binary = sample_binary
        sample.sha256 = sha256
        sample.save()
        return sample

    elif q.count() == 1:
        sample = q[0]
        return sample

    else:
        raise Exception("sample allready in database, and more than 1 items!!!")


# -------------------------------------------------------------------------
# 接口 - 样本无关


# 测试


def request_test(msg_request_test):
    """测试"""

    log_ii("request_test", msg_request_test)


# 主机


def add_host_os(msg_add_host_os):
    """创建主机"""

    log_ii("add_host_os", msg_add_host_os)

    json_dict = proto_msg_to_json_dict(msg_add_host_os)

    # 检查主机是否已存在
    check_host_os_not_exist(json_dict)

    # 添加
    BehvHostOs.from_json(json.dumps(json_dict)).save()


def clone_host_os(msg_clone_host_os):
    """根据主机 ID 克隆主机"""

    log_ii("clone_host_os", msg_clone_host_os)

    # 检查原主机是否存在
    host_os = check_host_os_single_by_id(msg_clone_host_os.src_host_os_id)

    # 检查克隆的新内容是否有重复
    host_os_json = host_os.to_filter()
    host_os_json["desc"] = msg_clone_host_os.new_desc
    check_host_os_not_exist(host_os_json)

    # 添加
    BehvHostOs.from_json(json.dumps(host_os_json)).save()


def del_host_os(msg_del_host_os):
    """删除主机"""

    log_ii("del_host_os", msg_del_host_os)

    # 检查主机是否存在
    check_host_os_exist_by_id(msg_del_host_os.host_os_id)

    # 删除
    BehvHostOs.objects(pk=msg_del_host_os.host_os_id).delete()


# 通信地址


def add_comm_target(msg_add_comm_target):
    """添加通信地址"""

    log_ii("add_comm_target", msg_add_comm_target)

    json_dict = proto_msg_to_json_dict(msg_add_comm_target)

    # 检查是否有重复
    check_comm_target_not_exist(json_dict)

    # 添加
    CommTarget.from_json(json.dumps(json_dict)).save()


def add_comm_target_to_sample(msg_add_comm_target_to_sample):
    """添加通信地址到某个样本"""

    log_ii("add_comm_target_to_sample", msg_add_comm_target_to_sample)

    # 检查样本是否存在
    check_sample_single_by_id(msg_add_comm_target_to_sample.sample_id)

    # 检查是否已经存在通信地址

    # 检查是否已经连接

    # 添加链接
    pass


def connect_comm_target(msg_connect_comm_target):
    """连接样本与通信地址"""

    log_ii("connect_comm_target", msg_connect_comm_target)

    # 检查样本/通信地址是否唯一
    check_sample_single_by_id(msg_connect_comm_target.sample_id)
    check_comm_target_single_by_id(msg_connect_comm_target.comm_target_id)

    # 检查是否已连接

    # 连接


def disconnect_comm_target(msg_disconnect_comm_target):
    """断开样本与通信地址的连接"""

    log_ii("disconnect_comm_target", msg_disconnect_comm_target)

    # 检查样本/通信地址是否唯一
    check_sample_single_by_id(msg_connect_comm_target.sample_id)
    check_comm_target_single_by_id(msg_connect_comm_target.comm_target_id)

    # 检查是否已连接

    # 断开连接


# 攻击目标


def add_attack_target(msg_add_attack_target):
    """添加攻击目标"""

    log_ii("add_attack_target", msg_add_attack_target)


def add_attack_target_to_sample(msg_add_attack_target_to_sample):
    """"""

    log_ii("add_attack_target_to_sample", msg_add_attack_target_to_sample)


def connect_attack_target(msg_connect_attack_target):
    """"""

    log_ii("connect_attack_target", msg_connect_attack_target)


def disconnect_attack_target(msg_disconnect_attack_target):
    """"""

    log_ii("disconnect_attack_target", msg_disconnect_attack_target)


# -------------------------------------------------------------------------
# 接口 - 分析


def analyze_sample(sample, is_overwrite=False):
    """
        分析样本，设置其基本信息及相关表

        @param: sample : obj : malwrdb_models.Sample object

        - 基本信息

        - pe相关表
        - elf相关表
        - pcap相关表
    """
    if is_overwrite or sample.analyze_time is None:

        sample_binary = sample._binary

        sample.sample_size = len(sample_binary)
        sample.md5 = hashlib.md5(sample_binary).hexdigest()
        sample.sha1 = hashlib.sha1(sample_binary).hexdigest()
        sample.sha256 = hashlib.sha256(sample_binary).hexdigest()
        sample.ssdeep = ssdeep_hash(sample_binary)
        sample.file_type = analyze_magic.guess_binary_type(sample_binary)

        # 先存一波
        sample.save()

        # PE32 executable for MS Windows (GUI) Intel 80386 32-bit
        # UTF-8 Unicode text, with CRLF line terminators

        file_type = sample.file_type

        if "PE32 executable for MS Windows" in file_type:

            analyze_pe.analyze_pe_basic(sample, sample_binary, is_overwrite=False)
            analyze_pe.analyze_pe_advanced(sample, sample_binary)

        elif file_type in ["elf"]:

            # analyze_elf.analyze_elf_basic(sample_id, sample_bin)
            pass

        elif file_type in ["idb"]:

            # analyze_idb.analyze_idb(sample_id, sample_bin)
            pass

        elif file_type in ["word", "xls", "ppt", "rtf", "xxx"]:
            pass

        elif file_type in ["plm"]:
            pass

        else:
            log("invalid file type: %s" % file_type)


def analyze_sample_list_by_id(msg_analyze_sample_list):
    """依据id分析样本"""
    for sample_id in msg_analyze_sample_list.sample_id_list:
        q = Sample.objects(pk=sample_id)
        if q.count() == 1:
            analyze_sample(q[0], is_overwrite=msg_analyze_sample_list.is_overwrite)
        else:
            raise Exception("duplicate sample. id: %s" % sample_id)


def sample_relationship(msg_sample_relationship):
    """设置样本父子关系"""
    check_sample_single(msg_sample_relationship.parent_sample_id)

    for child_sample_id in msg_sample_relationship.child_sample_id_list:

        child_sample = check_sample_single(child_sample_id)
        child_sample.parent__sample_id = msg_sample_relationship.parent_sample_id
        child_sample.parent__sample_to_this_type = msg_sample_relationship.relationship_type
        child_sample.save()


# -------------------------------------------------------------------------
# 接口 - 行为


# 文件


def append_file_behv(msg_append_file_behv):
    """添加文件行为"""

    log_ii("append_file_behv", msg_append_file_behv)

    sample_id = msg_append_file_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_append_file_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 循环添加
    for msg_file_behv in msg_append_file_behv.file_behv_list:

        file_behv_json_dict = proto_msg_to_json_dict(msg_file_behv)
        file_behv_json_dict["_behv_os_id_list"] = msg_append_file_behv.behv_os_id_list
        file_behv_json_dict["_sample_id"] = sample_id

        if BehvFile.objects(file_behv_json_dict).count() == 0:

            # 添加
            BehvFile.from_json(json.dumps(file_behv_json_dict)).save()

        else:
            # 忽略已经存在的
            warn("ignore already-existed file behv: %s" % file_behv_json_dict)


def replace_file_behv(msg_replace_file_behv):
    """替换文件行为"""

    log_ii("replace_file_behv", msg_replace_file_behv)

    sample_id = msg_replace_file_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_replace_file_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 去除之前的
    BehvFile.objects(id=sample_id).delete()

    # 循环添加
    for msg_file_behv in msg_replace_file_behv.file_behv_list:

        file_behv_json_dict = proto_msg_to_json_dict(msg_file_behv)
        file_behv_json_dict["_behv_os_id_list"] = msg_replace_file_behv.behv_os_id_list
        file_behv_json_dict["_sample_id"] = sample_id

        # 添加
        BehvFile.from_json(json.dumps(file_behv_json_dict)).save()


def clear_file_behv(msg_clear_file_behv):
    """清空文件行为"""

    log_ii("clear_file_behv", msg_clear_file_behv)

    # 确保样本唯一
    check_sample_single_by_id(msg_clear_file_behv.sample_id)

    # 清空
    BehvFile.objects(id=msg_clear_file_behv.sample_id).delete()


# 注册表


def append_reg_behv(msg_append_reg_behv):
    """追加注册表行为"""

    log_ii("append_reg_behv", msg_append_reg_behv)

    sample_id = msg_append_reg_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_append_reg_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 循环添加
    for msg_reg_behv in msg_append_reg_behv.reg_behv_list:

        reg_behv_json_dict = proto_msg_to_json_dict(msg_reg_behv)
        reg_behv_json_dict["_behv_os_id_list"] = msg_append_reg_behv.behv_os_id_list
        reg_behv_json_dict["_sample_id"] = sample_id

        if BehvReg.objects(reg_behv_json_dict).count() == 0:

            # 添加
            BehvReg.from_json(json.dumps(reg_behv_json_dict)).save()

        else:
            # 忽略已经存在的
            warn("ignore already-existed reg behv: %s" % reg_behv_json_dict)


def replace_reg_behv(msg_replace_reg_behv):
    """替换注册表行为"""

    log_ii("replace_reg_behv", msg_replace_reg_behv)

    sample_id = msg_replace_reg_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_replace_reg_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 去除之前的
    BehvReg.objects(id=sample_id).delete()

    # 循环添加
    for msg_reg_behv in msg_replace_reg_behv.reg_behv_list:

        reg_behv_json_dict = proto_msg_to_json_dict(msg_reg_behv)
        reg_behv_json_dict["_behv_os_id_list"] = msg_replace_file_behv.behv_os_id_list
        reg_behv_json_dict["_sample_id"] = sample_id

        # 添加
        BehvReg.from_json(json.dumps(reg_behv_json_dict)).save()


def clear_reg_behv(msg_clear_reg_behv):
    """删除注册表行为"""

    log_ii("clear_reg_behv", msg_clear_reg_behv)

    # 确保样本唯一
    check_sample_single_by_id(msg_clear_reg_behv.sample_id)

    # 清空
    BehvReg.objects(id=msg_clear_reg_behv.sample_id).delete()


# 网络


def append_network_behv(msg_append_network_behv):
    """添加网络行为"""

    log_ii("append_network_behv", msg_append_network_behv)

    sample_id = msg_append_network_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_append_network_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # ??


# 进程


def append_proc_behv(msg_append_proc_behv):
    """追加进程行为"""

    log_ii("append_proc_behv", msg_append_proc_behv)

    sample_id = msg_append_proc_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_append_proc_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 循环添加
    for msg_proc_behv in msg_append_proc_behv.proc_behv_list:

        proc_behv_json_dict = proto_msg_to_json_dict(msg_proc_behv)
        proc_behv_json_dict["_behv_os_id_list"] = msg_append_proc_behv.behv_os_id_list
        proc_behv_json_dict["_sample_id"] = sample_id

        if BehvProcess.objects(proc_behv_json_dict).count() == 0:

            # 添加
            BehvProcess.from_json(json.dumps(proc_behv_json_dict)).save()

        else:
            # 忽略已经存在的
            warn("ignore already-existed proc behv: %s" % proc_behv_json_dict)


def replace_proc_behv(msg_replace_proc_behv):
    """替换进程行为"""

    log_ii("replace_proc_behv", msg_replace_proc_behv)

    sample_id = msg_replace_proc_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_replace_proc_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 去除之前的
    BehvProcess.objects(id=sample_id).delete()

    # 循环添加
    for msg_proc_behv in msg_replace_proc_behv.proc_behv_list:

        proc_behv_json_dict = proto_msg_to_json_dict(msg_proc_behv)
        proc_behv_json_dict["_behv_os_id_list"] = msg_replace_file_behv.behv_os_id_list
        proc_behv_json_dict["_sample_id"] = sample_id

        # 添加
        BehvProcess.from_json(json.dumps(proc_behv_json_dict)).save()


def clear_proc_behv(msg_clear_proc_behv):
    """删除进程行为"""

    log_ii("clear_proc_behv", msg_clear_proc_behv)

    # 确保样本唯一
    check_sample_single_by_id(msg_clear_proc_behv.sample_id)

    # 清空
    BehvProcess.objects(id=msg_clear_proc_behv.sample_id).delete()


# 系统


def append_sys_behv(msg_append_sys_behv):
    """追加系统行为"""

    log_ii("append_sys_behv", msg_append_sys_behv)

    sample_id = msg_append_sys_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_append_sys_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 循环添加
    for msg_sys_behv in msg_append_sys_behv.sys_behv_list:

        sys_behv_json_dict = proto_msg_to_json_dict(msg_sys_behv)
        sys_behv_json_dict["_behv_os_id_list"] = msg_append_sys_behv.behv_os_id_list
        sys_behv_json_dict["_sample_id"] = sample_id

        if BehvSystem.objects(sys_behv_json_dict).count() == 0:

            # 添加
            BehvSystem.from_json(json.dumps(sys_behv_json_dict)).save()

        else:
            # 忽略已经存在的
            warn("ignore already-existed system behv: %s" % sys_behv_json_dict)


def replace_sys_behv(msg_replace_sys_behv):
    """替换系统行为"""

    log_ii("replace_sys_behv", msg_replace_sys_behv)

    sample_id = msg_replace_sys_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_replace_sys_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 去除之前的
    BehvSystem.objects(id=sample_id).delete()

    # 循环添加
    for msg_sys_behv in msg_replace_sys_behv.sys_behv_list:

        sys_behv_json_dict = proto_msg_to_json_dict(msg_sys_behv)
        sys_behv_json_dict["_behv_os_id_list"] = msg_replace_file_behv.behv_os_id_list
        sys_behv_json_dict["_sample_id"] = sample_id

        # 添加
        BehvSystem.from_json(json.dumps(sys_behv_json_dict)).save()


def clear_sys_behv(msg_clear_sys_behv):
    """删除系统行为"""

    log_ii("clear_sys_behv", msg_clear_sys_behv)

    # 确保样本唯一
    check_sample_single_by_id(msg_clear_sys_behv.sample_id)

    # 清空
    BehvSystem.objects(id=msg_clear_sys_behv.sample_id).delete()


# 窗口


def append_window_behv(msg_append_window_behv):
    """追加窗口行为"""

    log_ii("append_window_behv", msg_append_window_behv)

    sample_id = msg_append_window_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_append_window_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 循环添加
    for msg_window_behv in msg_append_window_behv.window_behv_list:

        window_behv_json_dict = proto_msg_to_json_dict(msg_window_behv)
        window_behv_json_dict["_behv_os_id_list"] = msg_append_window_behv.behv_os_id_list
        window_behv_json_dict["_sample_id"] = sample_id

        if BehvWindow.objects(window_behv_json_dict).count() == 0:

            # 添加
            BehvWindow.from_json(json.dumps(window_behv_json_dict)).save()

        else:
            # 忽略已经存在的
            warn("ignore already-existed window behv: %s" % window_behv_json_dict)


def replace_window_behv(msg_replace_window_behv):
    """替换窗口行为"""

    log_ii("replace_window_behv", msg_replace_window_behv)

    sample_id = msg_replace_window_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_replace_window_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 去除之前的
    BehvWindow.objects(id=sample_id).delete()

    # 循环添加
    for msg_window_behv in msg_replace_window_behv.window_behv_list:

        window_behv_json_dict = proto_msg_to_json_dict(msg_window_behv)
        window_behv_json_dict["_behv_os_id_list"] = msg_replace_file_behv.behv_os_id_list
        window_behv_json_dict["_sample_id"] = sample_id

        # 添加
        BehvWindow.from_json(json.dumps(window_behv_json_dict)).save()


def clear_window_behv(msg_clear_window_behv):
    """删除窗口行为"""

    log_ii("clear_window_behv", msg_clear_window_behv)

    # 确保样本唯一
    check_sample_single_by_id(msg_clear_window_behv.sample_id)

    # 清空
    BehvWindow.objects(id=msg_clear_window_behv.sample_id).delete()


# 服务


def append_service_behv(msg_append_service_behv):
    """追加服务行为"""

    log_ii("append_service_behv", msg_append_service_behv)

    sample_id = msg_append_service_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_append_service_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 循环添加
    for msg_service_behv in msg_append_service_behv.service_behv_list:

        service_behv_json_dict = proto_msg_to_json_dict(msg_service_behv)
        service_behv_json_dict["_behv_os_id_list"] = msg_append_service_behv.behv_os_id_list
        service_behv_json_dict["_sample_id"] = sample_id

        if BehvService.objects(service_behv_json_dict).count() == 0:

            # 添加
            BehvService.from_json(json.dumps(service_behv_json_dict)).save()

        else:
            # 忽略已经存在的
            warn("ignore already-existed service behv: %s" % service_behv_json_dict)


def replace_service_behv(msg_replace_service_behv):
    """替换服务行为"""

    log_ii("replace_service_behv", msg_replace_service_behv)

    sample_id = msg_replace_service_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_replace_service_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 去除之前的
    BehvService.objects(id=sample_id).delete()

    # 循环添加
    for msg_service_behv in msg_replace_service_behv.service_behv_list:

        service_behv_json_dict = proto_msg_to_json_dict(msg_service_behv)
        service_behv_json_dict["_behv_os_id_list"] = msg_replace_file_behv.behv_os_id_list
        service_behv_json_dict["_sample_id"] = sample_id

        # 添加
        BehvService.from_json(json.dumps(service_behv_json_dict)).save()


def clear_service_behv(msg_clear_service_behv):
    """删除服务行为"""

    log_ii("clear_service_behv", msg_clear_service_behv)

    # 确保样本唯一
    check_sample_single_by_id(msg_clear_service_behv.sample_id)

    # 清空
    BehvService.objects(id=msg_clear_service_behv.sample_id).delete()


# 互斥体/事件


def append_mutex_behv(msg_append_mutex_behv):
    """添加互斥体/事件行为"""

    log_ii("append_mutex_behv", msg_append_mutex_behv)

    sample_id = msg_append_mutex_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_append_mutex_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 循环添加
    for msg_mutex_behv in msg_append_mutex_behv.mutex_behv_list:

        mutex_behv_json_dict = proto_msg_to_json_dict(msg_mutex_behv)
        mutex_behv_json_dict["_behv_os_id_list"] = msg_append_mutex_behv.behv_os_id_list
        mutex_behv_json_dict["_sample_id"] = sample_id

        if BehvMutex.objects(mutex_behv_json_dict).count() == 0:

            # 添加
            BehvMutex.from_json(json.dumps(mutex_behv_json_dict)).save()

        else:
            # 忽略已经存在的
            warn("ignore already-existed mutex behv: %s" % mutex_behv_json_dict)


def replace_mutex_behv(msg_replace_mutex_behv):
    """替换互斥体/事件行为"""

    log_ii("replace_mutex_behv", msg_replace_mutex_behv)

    sample_id = msg_replace_mutex_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_replace_mutex_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 去除之前的
    BehvMutex.objects(id=sample_id).delete()

    # 循环添加
    for msg_mutex_behv in msg_replace_mutex_behv.mutex_behv_list:

        mutex_behv_json_dict = proto_msg_to_json_dict(msg_mutex_behv)
        mutex_behv_json_dict["_behv_os_id_list"] = msg_replace_file_behv.behv_os_id_list
        mutex_behv_json_dict["_sample_id"] = sample_id

        # 添加
        BehvMutex.from_json(json.dumps(mutex_behv_json_dict)).save()


def clear_mutex_behv(msg_clear_mutex_behv):
    """清空互斥体/事件行为"""

    log_ii("clear_mutex_behv", msg_clear_mutex_behv)

    # 确保样本唯一
    check_sample_single_by_id(msg_clear_mutex_behv.sample_id)

    # 清空
    BehvMutex.objects(id=msg_clear_mutex_behv.sample_id).delete()


# 随便什么行为


def append_whatever_behv(msg_append_whatever_behv):
    """追加随便什么行为"""

    log_ii("append_whatever_behv", msg_append_whatever_behv)

    sample_id = msg_append_whatever_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_append_whatever_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 循环添加
    for msg_whatever_behv in msg_append_whatever_behv.whatever_behv_list:

        whatever_behv_json_dict = proto_msg_to_json_dict(msg_whatever_behv)
        whatever_behv_json_dict["_behv_os_id_list"] = msg_append_whatever_behv.behv_os_id_list
        whatever_behv_json_dict["_sample_id"] = sample_id

        if BehvWhatever.objects(whatever_behv_json_dict).count() == 0:

            # 添加
            BehvWhatever.from_json(json.dumps(whatever_behv_json_dict)).save()

        else:
            # 忽略已经存在的
            warn("ignore already-existed whatever behv: %s" % whatever_behv_json_dict)


def replace_whatever_behv(msg_replace_whatever_behv):
    """替换随便什么行为"""

    log_ii("replace_whatever_behv", msg_replace_whatever_behv)

    sample_id = msg_replace_whatever_behv.sample_id

    # 确保样本/行为主机唯一
    check_sample_single_by_id(sample_id)
    for host_os_id in msg_replace_whatever_behv.behv_os_id_list:
        check_host_os_single_by_id(host_os_id)

    # 去除之前的
    BehvWhatever.objects(id=sample_id).delete()

    # 循环添加
    for msg_whatever_behv in msg_replace_whatever_behv.whatever_behv_list:

        whatever_behv_json_dict = proto_msg_to_json_dict(msg_whatever_behv)
        whatever_behv_json_dict["_behv_os_id_list"] = msg_replace_file_behv.behv_os_id_list
        whatever_behv_json_dict["_sample_id"] = sample_id

        # 添加
        BehvWhatever.from_json(json.dumps(whatever_behv_json_dict)).save()


def del_whatever_behv(msg_del_whatever_behv):
    """删除随便什么行为"""

    # 确保样本唯一
    #


def clear_whatever_behv(msg_clear_whatever_behv):
    """清空随便什么行为"""

    log_ii("clear_whatever_behv", msg_clear_whatever_behv)

    # 确保样本唯一
    check_sample_single_by_id(msg_clear_whatever_behv.sample_id)

    # 清空
    BehvWhatever.objects(id=msg_clear_whatever_behv.sample_id).delete()


# 组合行为


def append_behv_feature(msg_append_behv_feature):
    """追加组合行为"""

    log_ii("append_behv_feature", msg_append_behv_feature)


def replace_behv_feature(msg_replace_behv_feature):
    """替换组合行为"""

    log_ii("replace_behv_feature", msg_replace_behv_feature)


def clear_behv_feature(msg_clear_behv_feature):
    """清空组合行为"""

    log_ii("clear_behv_feature", msg_clear_behv_feature)


# -------------------------------------------------------------------------
# 样本的网络信息


def update_vt_info(msg_update_vt_info):
    """"""

    log_ii("update_vt_info", msg_update_vt_info)


def update_hybrid_info(msg_update_hybrid_info):
    """"""

    log_ii("update_hybrid_info", msg_update_hybrid_info)


def update_reverseit_info(msg_update_reverseit_info):
    """"""

    log_ii("update_reverseit_info", msg_update_reverseit_info)


def update_malwr_info(msg_update_malwr_info):
    """"""

    log_ii("update_malwr_info", msg_update_malwr_info)


# -------------------------------------------------------------------------
# 从网络提取样本


# -------------------------------------------------------------------------
# 从网络获取 Yara 规则


# -------------------------------------------------------------------------
# 中英对照


# 文件类型


def add_file_type(msg_add_file_type):
    """添加文件类型"""

    log_ii("add_file_type", msg_add_file_type)

    # 循环添加
    for msg_file_type in msg_add_file_type.file_type_list:
        check_insert_file_type(proto_msg_to_json_dict(msg_file_type))


def del_file_type(msg_del_file_type):
    """删除文件类型"""

    log_ii("del_file_type", msg_del_file_type)

    # 删除
    FileType.objects(pk=msg_del_file_type.file_type_id).delete()


# 平台


def add_platform(msg_add_platform):
    """添加平台"""

    log_ii("add_platform_proto", msg_add_platform)

    # 循环添加
    for msg_platform in msg_add_platform.platform_list:
        check_insert_platform(proto_msg_to_json_dict(msg_platform))


def del_platform(msg_del_platform):
    """删除平台"""

    log_ii("del_platform", msg_del_platform)

    # 删除
    FileType.objects(pk=msg_del_platform.platform_id).delete()


# 样本关系


def add_sample_relationship_type(msg_add_sample_relationship_type):
    """添加样本关系"""

    log_ii("add_sample_relationship_type", msg_add_sample_relationship_type)

    # 循环添加
    for msg_sample_relationship_type in msg_add_sample_relationship_type.sample_relationship_list:
        check_insert_sample_relationship_type(proto_msg_to_json_dict(msg_sample_relationship_type))


def del_sample_relationship_type(msg_del_sample_relationship_type):
    """删除样本关系"""

    log_ii("del_sample_relationship_type", msg_del_sample_relationship_type)

    # 删除
    SampleRelationshipType.objects(pk=msg_del_sample_relationship_type.sample_realtionship_type_id).delete()


# 总体的恶意类型


def add_overall_malicious_type(msg_add_overall_malicious_type):
    """添加总体的恶意类型"""

    log_ii("add_overall_malicious_type", msg_add_overall_malicious_type)

    # 循环添加
    for msg_overall_malicious_type in msg_add_overall_malicious_type.malicious_type_list:
        check_insert_overall_malicious_type(proto_msg_to_json_dict(msg_overall_malicious_type))


def del_overall_malicious_type(msg_del_overall_malicious_type):
    """删除总体的恶意类型"""

    log_ii("del_overall_malicious_type", msg_del_overall_malicious_type)

    # 删除
    OverallMaliciousType.objects(pk=msg_del_overall_malicious_type.overall_malicious_type_id).delete()


# 恶意代码家族


def add_malware_family(msg_add_malware_family):
    """添加恶意代码家族"""

    log_ii("add_malware_family", msg_add_malware_family)

    # 循环添加
    for msg_malware_family in msg_add_malware_family.malware_family_list:
        check_insert_malware_family(proto_msg_to_json_dict(msg_malware_family))


def del_malware_family(msg_del_malware_family):
    """删除恶意代码家族"""

    log_ii("del_malware_family", msg_del_malware_family)

    # 删除
    MalwareFamily.objects(pk=msg_del_malware_family.malware_family_id).delete()


# 编程语言


def add_programing_lang(msg_add_programing_lang):
    """添加编程语言"""

    log_ii("add_programing_lang", msg_add_programing_lang)

    # 循环添加
    for msg_programing_lang in msg_add_programing_lang.programing_lang_list:
        check_insert_programing_lang(proto_msg_to_json_dict(msg_programing_lang))


def del_programing_lang(msg_del_programing_lang):
    """删除编程语言"""

    log_ii("del_programing_lang", msg_del_programing_lang)

    # 删除
    ProgramingLang.objects(pk=msg_del_programing_lang.programing_lang_id).delete()


# 函数类型


def add_function_type(msg_add_function_type):
    """添加函数类型"""

    log_ii("add_function_type", msg_add_function_type)

    # 循环添加
    for msg_function_type in msg_add_function_type.func_type_list:
        check_insert_function_type(proto_msg_to_json_dict(msg_function_type))


def del_function_type(msg_del_function_type):
    """删除函数类型"""

    log_ii("del_function_type", msg_del_function_type)

    # 删除
    FunctionType.objects(pk=msg_del_function_type.function_type_id).delete()


# 进程行为类型


def add_proc_behv_type(msg_add_proc_behv_type):
    """添加进程行为类型"""

    log_ii("add_proc_behv_type", msg_add_proc_behv_type)

    # 循环添加
    for msg_proc_behv_type in msg_add_proc_behv_type.proc_behv_type_list:
        check_insert_proc_behv_type(proto_msg_to_json_dict(msg_proc_behv_type))


def del_proc_behv_type(msg_del_proc_behv_type):
    """删除进程行为类型"""

    log_ii("del_proc_behv_type", msg_del_proc_behv_type)

    # 删除
    ProcBehvType.objects(pk=msg_del_proc_behv_type.proc_behv_type_id).delete()


# 系统行为类型


def add_sys_behv_type(msg_add_sys_behv_type):
    """添加系统行为类型"""

    log_ii("add_sys_behv_type", msg_add_sys_behv_type)

    # 循环添加
    for msg_sys_behv_type in msg_add_sys_behv_type.sys_behv_type_list:
        check_insert_sys_behv_type(proto_msg_to_json_dict(msg_sys_behv_type))


def del_sys_behv_type(msg_del_sys_behv_type):
    """删除系统行为类型"""

    log_ii("del_sys_behv_type", msg_del_sys_behv_type)

    # 删除
    SysBehvType.objects(pk=msg_del_sys_behv_type.sys_behv_type_id).delete()


# 组合行为


def add_behv_feature_type(msg_add_behv_feature_type):
    """添加组合行为"""

    log_ii("add_behv_feature_type", msg_add_behv_feature_type)

    # 循环添加
    for msg_behv_feature in msg_add_behv_feature_type.behv_feature_type_list:
        check_insert_behv_feature_type(proto_msg_to_json_dict(msg_behv_feature))


def del_behv_feature_type(msg_del_behv_feature):
    """删除组合行为"""

    log_ii("del_behv_feature_type", msg_del_behv_feature)

    # 删除
    BehvFeatureType.objects(pk=msg_del_behv_feature.behv_feature_type_id).delete()


# -------------------------------------------------------------------------
# test


def test_analyze_pe_sample(sample):
    log("test start...\n")
    analyze_sample(sample, is_overwrite=True)
    log("\ntest finish...\n")


def test_analyze_win_pe_binary(pe_binary):
    sample = sample_check_or_insert(pe_binary)
    test_analyze_pe_sample(sample)


def test_analyze_win_pe(pe_path):
    if not os.path.exists(pe_path):
        log("invalid win pe path: %s" % pe_path)
        return

    with open(pe_path, 'rb') as f:
        pe = f.read()
        if len(pe) != 0:
            test_analyze_win_pe_binary(pe)
        else:
            log("pe len 0. path: %s" % pe_path)


# -------------------------------------------------------------------------
# END OF FILE
# -------------------------------------------------------------------------
