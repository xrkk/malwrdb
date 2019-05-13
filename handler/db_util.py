# -*- coding: utf-8 -*-

"""
"""

# -------------------------------------------------------------------------


from mongoengine import *

from malwrdb_models import *


# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)


# -------------------------------------------------------------------------
# 验证/获取
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# base


def check_object_single(model, filter):
    """
        确保 filter 有效且 doc 唯一

        @param: model  : class  : mongoengine.Document 类
        @param: filter : dict   : filter dict

        @return: doc  :
                 None :
    """
    q = model.objects(**filter)
    if q.count() != 1:
        raise Exception("doc not exist or not single. collection: %s, doc count: %d, filter: %s" %
                        (model._meta["collection"], q.count(), filter))
    return q[0]


def check_object_exist(model, filter):
    """
        确保 filter 有效且 doc 存在. 如果不存在, 则抛出异常

        @param: model  : class  : mongoengine.Document 类
        @param: filter : dict   : filter dict
    """
    cnt = model.objects(**filter).count()
    if cnt == 0:
        raise Exception("doc does not exists in collection. collection: %s, doc count: %d, filter: %s" %
                        (model._meta["collection"], cnt, filter))


def check_object_not_exist(model, filter):
    """
        确保 filter 有效且 doc 不存在. 如果存在, 则抛出异常

        @param: model  : class  : mongoengine.Document 类
        @param: filter : dict   : filter dict
    """
    cnt = model.objects(**filter).count()
    if cnt != 0:
        raise Exception("doc exists in collection. collection: %s, doc count: %d, filter: %s" %
                        (model._meta["collection"], cnt, filter))


# -------------------------------------------------------------------------
# 具体的集合


# 样本


def check_sample_single(filter, is_ret=True):
    doc = check_object_single(Sample, filter)
    if is_ret:
        return doc


def check_sample_exist(filter):
    check_object_exist(Sample, filter)


def check_sample_not_exist(filter):
    check_object_not_exist(Sample, filter)


def check_sample_single_by_id(sample_id, is_ret=True):
    doc = check_object_single(Sample, {"id": sample_id})
    if is_ret:
        return doc


def check_sample_exist_by_id(sample_id):
    check_object_exist(Sample, {"id": sample_id})


def check_sample_not_exist_by_id(sample_id):
    check_object_not_exist(Sample, {"id": sample_id})


# 主机


def check_host_os_single(filter, is_ret=True):
    doc = check_object_single(BehvHostOs, filter)
    if is_ret:
        return doc


def check_host_os_exist(filter):
    check_object_exist(BehvHostOs, filter)


def check_host_os_not_exist(filter):
    check_object_not_exist(BehvHostOs, filter)


def check_host_os_single_by_id(host_os_id, is_ret=True):
    doc = check_object_single(BehvHostOs, {"id": host_os_id})
    if is_ret:
        return doc


def check_host_os_exist_by_id(host_os_id):
    check_object_exist(BehvHostOs, {"id": host_os_id})


def check_host_os_not_exist_by_id(host_os_id):
    check_object_not_exist(BehvHostOs, {"id": host_os_id})


# 通信目标


def check_comm_target_single(filter, is_ret=True):
    doc = check_object_single(CommTarget, filter)
    if is_ret:
        return doc


def check_comm_target_exist(filter):
    check_object_exist(CommTarget, filter)


def check_comm_target_not_exist(filter):
    check_object_not_exist(CommTarget, filter)


def check_comm_target_single_by_id(comm_target_id, is_ret=True):
    doc = check_object_single(CommTarget, {"id": comm_target_id})
    if is_ret:
        return doc


def check_comm_target_exist_by_id(comm_target_id):
    check_object_exist(CommTarget, {"id": comm_target_id})


def check_comm_target_not_exist_by_id(comm_target_id):
    check_object_not_exist(CommTarget, {"id": comm_target_id})


# 攻击目标


#


# -------------------------------------------------------------------------
# 验证/插入
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# base


def check_insert(model, filter):
    """检查是否有重复, 没有则插入"""
    q = model.objects(**filter)
    if q.count() != 0:
        log("doc already-existed, not inserting. collection: %s, filter: %s" %
            (model._meta["collection"], filter))
        return None

    doc = model.from_json(json.dumps(filter)).save()
    return doc


# -------------------------------------------------------------------------
# 数据集合


# 主机


def check_insert_host_os(filter):
    return check_insert(BehvHostOs, filter)


# -------------------------------------------------------------------------
# 中英对照集合


# 文件类型


def check_insert_file_type(filter):
    return check_insert(FileType, filter)


# 平台


def check_insert_platform(filter):
    return check_insert(Platform, filter)


# 样本关系


def check_insert_sample_relationship_type(filter):
    return check_insert(SampleRelationshipType, filter)


# 总体的恶意类型


def check_insert_overall_malicious_type(filter):
    return check_insert(OverallMaliciousType, filter)


# 恶意代码家族


def check_insert_malware_family(filter):
    return check_insert(MalwareFamily, filter)


# 编程语言


def check_insert_programing_lang(filter):
    return check_insert(ProgramingLang, filter)


# 函数类型


def check_insert_function_type(filter):
    return check_insert(FunctionType, filter)


# 进程行为类型


def check_insert_proc_behv_type(filter):
    return check_insert(ProcBehvType, filter)


# 系统行为类型


def check_insert_sys_behv_type(filter):
    return check_insert(SysBehvType, filter)


# 组合行为


def check_insert_behv_feature_type(filter):
    return check_insert(BehvFeatureType, filter)


# -------------------------------------------------------------------------


if __name__ == "__main__":

    def validate_database():
        """
            验证数据库:
                - PE/ELF 结构的对应关系
                -
        """
        pass
    pass


# -------------------------------------------------------------------------
# ENF OF FILE
# -------------------------------------------------------------------------
