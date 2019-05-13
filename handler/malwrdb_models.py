# -*- coding: utf-8 -*-

"""
1. 集合的名称会被拆开: CommTarget -> comm_target
2. 纯基类的文档, 类名称以Document结尾, 其他均不以Document结尾
"""


import json

from datetime import datetime
from mongoengine import *

from malwrdb_util import *
from malwrdb_settings import *
from db_connect import db_connect

# -------------------------------------------------------------------------


# 连接数据库
db_connect()


# -------------------------------------------------------------------------
# misc


class LogLine(Document):
    """日志"""

    time = DateTimeField()
    file = StringField()
    level = IntField()
    info = StringField()


# -------------------------------------------------------------------------
# 不属于特定样本的 - N->1


class BehvHostOs(Document):
    """行为目标主机"""

    meta = {'collection': "host_os"}

    platform = StringField()                        # TODO: 检查 platform 是否在某个列表中??
    version = StringField()
    arch = StringField()
    desc = StringField()
    sp = IntField()
    author = StringField()

    update_time = DateTimeField()

    def clean(self):
        self.update_time = datetime.now()

    def to_filter(self):
        json_dict = self.to_json()
        del json_dict["_id"]
        del json_dict["author"]
        del json_dict["update_time"]
        return json_dict


class CommTarget(Document):
    """通信目标"""

    meta = {'collection': "comm_target"}

    domain = StringField()
    ip_addr = StringField()
    port = IntField(min_value=0, max_value=65536)

    update_time = DateTimeField()

    def clean(self):
        self.update_time = datetime.now()

    def to_filter(self):
        json_dict = json.loads(self.to_json())
        del json_dict["_id"]
        del json_dict["update_time"]
        return json.dumps(json_dict)


class AttackTarget(Document):
    """攻击目标"""

    meta = {'collection': "attack_target"}

    continent_list = ListField()                      # 大洲
    country_list = ListField()                      # 攻击国家
    industry_list = ListField()                     # 攻击行业

    update_time = DateTimeField()

    def clean(self):
        self.update_time = datetime.now()

    def to_filter(self):
        json_dict = json.loads(self.to_json())
        del json_dict["_id"]
        del json_dict["update_time"]
        return json.dumps(json_dict)


# -------------------------------------------------------------------------
# 样本


class Sample(Document):
    """样本"""

    _binary = BinaryField()                                            # 二进制数据

    file_name = StringField()                                          # 文件名, 添加时设置. 不是路径
    sample_size = IntField()                                           # 样本大小
    file_type = StringField()                                          # 样本文件类型

    md5 = StringField(max_length=32, min_length=32)                    # 哈希值 - MD5    - 长度32
    sha1 = StringField(max_length=40, min_length=40)                   # 哈希值 - SHA1   - 长度40
    sha256 = StringField(max_length=64, min_length=64)                 # 哈希值 - SHA256 - 长度64
    sha512 = StringField(max_length=128, min_length=128)               # 哈希值 - SHA512 - 长度128
    ssdeep = StringField()                                             # 哈希值 - ssdeep
    imphash = StringField()                                            # 哈希值 - 导入表
    crc32 = StringField()                                              # 哈希值 - CRC32

    platform = StringField()                                           # 平台
    is_malicious = BooleanField()                                      # 是否恶意
    malware_name_list = ListField()                                    # 恶意名称列表(某些恶意代码有多个名称)
    malware_family_list = ListField()                                  # 恶徒家族列表

    parent__sample_id = ObjectIdField()                                # 父样本 id
    parent__sample_to_this_type = StringField()                        # 与父样本的关系(有choices)

    #

    analyze_time = DateTimeField()                                     # 分析时间(手动设置). 为 None 表示没分析过

    update_time = DateTimeField()

    def clean(self):
        pass

    def to_filter(self):
        return {"sha256": self.sha256}


class BelongToSampleDocument(Document):
    """属于Sample的文档"""

    meta = {
        'allow_inheritance': True,
        'abstract': True
    }
    # 自己代码里用
    _sample = ReferenceField(Document)
    # 前台PHP访问数据库用
    _sample_id = ObjectIdField()

    update_time = DateTimeField()

    def clean(self):
        # sample
        if self._sample is not None and self._sample_id is not None:
            assert self._sample.id == self._sample_id
        elif self._sample is not None:
            self._sample_id = self._sample.id
        elif self._sample_id is not None:
            q = Sample.objects(id=self._sample_id)
            assert q.count() == 1
            self._sample = q[0]
        else:
            raise ValidationError("at least one of _sample_id or _sample shall be se")

        self.update_time = datetime.now()


class BelongToSampleDynamicDocument(DynamicDocument):
    """属于Sample的文档"""

    meta = {
        'allow_inheritance': True,
        'abstract': True
    }
    # 自己代码里用
    _sample = ReferenceField(Document)
    # 前台PHP访问数据库用
    _sample_id = ObjectIdField()

    update_time = DateTimeField()

    def clean(self):
        if self._sample is not None and self._sample_id is not None:
            assert self._sample.id == self._sample_id
        elif self._sample is not None:
            self._sample_id = self._sample.id
        elif self._sample_id is not None:
            q = Sample.objects(id=self._sample_id)
            assert q.count() == 1
            self._sample = q[0]
        else:
            raise ValidationError("at least one of _sample_id or _sample shall be se")

        self.update_time = datetime.now()


# -------------------------------------------------------------------------
# 样本 - pe/elf - pefile.py 的基本属性


class PeDosHeader(BelongToSampleDynamicDocument):
    """PE Dos 头"""

    meta = {'collection': "pe_dos_header"}


class PeNtHeader(BelongToSampleDynamicDocument):
    """PE Nt 头"""

    meta = {'collection': "pe_nt_header"}

    file_header = DictField()
    optional_header = DictField()


class PeSection(BelongToSampleDynamicDocument):
    """PE 段"""

    meta = {'collection': "pe_section"}


# -------------------------------------------------------------------------
# 样本 - pe/elf -


class PackerCompiler(BelongToSampleDocument):
    """壳/编译器信息"""

    meta = {'collection': "packer_compiler"}

    raw = StringField()

    name = StringField()
    version = StringField()
    lang = StringField()
    compile_time = StringField()


class PeSuspecious(BelongToSampleDocument):
    """PE 可以信息"""

    meta = {'collection': "pe_suspecious"}

    suspecious_type = StringField()
    suspecious_content = StringField()


# -------------------------------------------------------------------------
# 样本 - 行为


class BehvBaseDocument(BelongToSampleDocument):
    """行为基类"""

    meta = {
        'allow_inheritance': True,
        'abstract': True
    }
    _behv_host_os_list = ListField(ReferenceField(BehvHostOs))


class BehvFile(BehvBaseDocument):
    """文件行为"""

    meta = {'collection': "behv_file"}

    file_path = StringField(required=True)

    def is_identical(self, doc):
        return self.file_path == doc.file_path

    def similarity(self, doc):
        return diff_string(self.file_path, doc.file_path)


class BehvReg(BehvBaseDocument):
    """注册表行为"""

    meta = {'collection': "behv_reg"}

    reg_path = StringField(required=True)

    def is_identical(self, doc):
        return self.reg_path == doc.reg_path

    def similarity(self, doc):
        return diff_string(self.reg_path, doc.reg_path)


class BehvNetwork(BehvBaseDocument):
    """网络行为"""

    meta = {'collection': "behv_network"}

    comm_type = StringField()
    comm_target = ReferenceField(CommTarget)

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


class BehvThread(BehvBaseDocument):
    """线程行为"""

    meta = {'collection': "behv_thread"}

    behv_desc = StringField()

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


class BehvProcess(BehvBaseDocument):
    """进程行为"""

    meta = {'collection': "behv_process"}

    behv_type = StringField()
    behv_desc = StringField()

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


class BehvSystem(BehvBaseDocument):
    """系统行为"""

    meta = {'collection': "behv_system"}

    behv_type = StringField()

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


class BehvWindow(BehvBaseDocument):
    """窗口行为"""

    meta = {'collection': "behv_window"}

    behv_type = StringField()
    window_name = StringField()
    window_class_name = StringField()

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


class BehvService(BehvBaseDocument):
    """服务行为"""

    meta = {'collection': "behv_service"}

    behv_type = StringField()
    service_name = StringField()
    service_display_name = StringField()
    service_binary_path = StringField()
    service_other_params = StringField()

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


class BehvMutex(BehvBaseDocument):
    """互斥体行为"""

    meta = {'collection': "behv_mutex"}

    mutex_name = StringField()

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


class BehvDynamicApi(BehvBaseDocument):
    """动态API行为"""

    meta = {'collection': "behv_dynamic_api"}

    resolve_type = StringField()

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


class BehvWhatever(BehvBaseDocument):
    """其他行为"""

    meta = {'collection': "behv_whatever"}

    behv_desc = StringField()

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


class BehvFeature(BehvBaseDocument):
    """组合行为"""

    meta = {'collection': "behv_feature"}

    feature_type = StringField()

    def is_identical(self, doc):
        pass

    def similarity(self, doc):
        pass


# -------------------------------------------------------------------------
# 网络信息


class SampleVtInfo(Document):
    """VT信息"""
    meta = {'collection': "sample_vt_info"}

    url = URLField()

    update_time = DateTimeField()

    def clean(self):
        self.update_time = datetime.now()


class SampleHybridInfo(Document):
    """Hybrid信息"""
    meta = {'collection': "sample_hybrid_info"}

    url = URLField()
    update_time = DateTimeField()

    def clean(self):
        self.update_time = datetime.now()


class SampleReverseItInfo(Document):
    """ReverseIt信息"""
    meta = {'collection': "sample_reverseit_info"}

    url = URLField()
    update_time = DateTimeField()

    def clean(self):
        self.update_time = datetime.now()


class SampleMalwrInfo(Document):
    """Malwr信息"""
    meta = {'collection': "sample_malwr_info"}

    url = URLField()
    update_time = DateTimeField()

    def clean(self):
        self.update_time = datetime.now()


# -------------------------------------------------------------------------
# 中英对照


class LocalDocument(Document):
    meta = {
        'allow_inheritance': True,
        'abstract': True,
        'db_alias': mongo_local_db_name,
    }

    name = StringField(required=True)
    desc = StringField(required=True)

    add_time = DateTimeField()

    def clean(self):
        self.add_time = datetime.now()


class FileType(LocalDocument):
    """文件类型"""
    meta = {'collection': "local_file_type"}


class Platform(LocalDocument):
    """平台"""
    meta = {'collection': "local_platform"}


class SampleRelationshipType(LocalDocument):
    """样本关系"""
    meta = {'collection': "local_sample_relationship_type"}


class OverallMaliciousType(LocalDocument):
    """总体的恶意类型"""
    meta = {'collection': "local_overall_malicious_types"}


class MalwareFamily(LocalDocument):
    """恶意代码家族"""
    meta = {'collection': "local_malware_family"}


class ProgramingLang(LocalDocument):
    """编程语言"""
    meta = {'collection': "local_programing_lang"}


class FunctionType(LocalDocument):
    """函数类型"""
    meta = {'collection': "local_function_type"}


class ProcBehvType(LocalDocument):
    """进程行为类型"""
    meta = {'collection': "local_proc_behv_type"}


class SysBehvType(LocalDocument):
    """系统行为类型"""
    meta = {'collection': "local_sys_behv_type"}


class BehvFeatureType(LocalDocument):
    """组合行为"""
    meta = {'collection': "local_behv_feature_type"}


# -------------------------------------------------------------------------
# 其他


class Yara(Document):
    pass


# -------------------------------------------------------------------------
# ENF OF FILE
# -------------------------------------------------------------------------
