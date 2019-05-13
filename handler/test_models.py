# -*- coding: utf-8 -*-

"""
"""

import os
import traceback
from mongoengine import *

from malwrdb_models import *
from malwrdb_settings import *


# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)


# -------------------------------------------------------------------------
# mongoengine


def test_json():

    # # to_json
    # tar = CommTarget()
    # tar.domain = "12g"
    # tar.port = 123
    # tar.save()
    # # {"_id": {"$oid": "59b9f2aaa9ddb539fccb66eb"}, "domain": "12g", "port": 123, "update_time": {"$date": 1505387306592}}
    # log(tar.to_json()
    # # {"domain": "12g", "port": 123}
    # log(tar.to_filter()

    # # from_json
    # import json
    # j = {"domain": "12g", "port": 123}
    # tar = CommTarget.from_json(json.dumps(j))  # OK
    # tar.save()
    # log(tar.to_json()

    # # 用 json 做搜索条件
    # j = {"domain": "12g", "port": 123}
    # q = CommTarget.objects(**j)
    # log(q.count()

    pass


def test_meta():
    # {'abstract': False,
    #  'allow_inheritance': None,
    #  'collection': 'comm_target',
    #  'delete_rules': None,
    #  'id_field': 'id',
    #  'index_background': False,
    #  'index_drop_dups': False,
    #  'index_opts': None,
    #  'index_specs': [],
    #  'indexes': [],
    #  'max_documents': None,
    #  'max_size': None,
    #  'ordering': []}
    log(CommTarget._meta)

    pass


# -------------------------------------------------------------------------
# 样本


def add_sample(file_path):
    with open(file_path, 'rb') as f:  # 对于txt文档, 有可能会因为文档的编码导致: Permission denied: u'...\\\u884d\u751f\u7269'
        pe = f.read()
        if len(pe) != 0:
            log("adding sample: %s" % file_path)
            sample = Sample()
            sample._binary = pe
            sample.file_name = os.path.basename(file_path)
            sample.save()
            return sample.pk
    return None


def test_add_sample():
    add_sample(r"F:\abc\Sample Analysis\_self_collect\Acronym_ M is for Malware\a199e9d00123fefe69f2863b08f211a2\_sample.bin")


def test_add_sample_list():
    # 清空集合
    Sample.drop_collection()

    def cbk(arg, dirname, names):
        for filespath in names:
            try:
                path_ = os.path.join(dirname, filespath)
                add_sample(path_)
            except:
                traceback.print_exc()

    dir_ = os.path.abspath(u"test_resources")  # 这里要有 u 前缀
    os.path.walk(dir_, cbk, {})


# -------------------------------------------------------------------------


if __name__ == "__main__":
    connect(mongo_test_db_name, host=mongo_test_host, port=mongo_test_port)
    connect(mongo_local_db_name, alias=mongo_local_db_name, host=mongo_test_host, port=mongo_test_port)

    # -------------------------------------------------------------------------
    # x

    # CommTarget.drop_collection()

    # dos_header = PeDosHeader(**{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
    # dos_header.save()

    # sample = Sample()
    # sample.hash_md5 = "abc"
    # sample.save()
    # file_behv = BehvFile()
    # file_behv._sample = sample
    # file_behv.file_path = "xxx"
    # file_behv.save()

    # -------------------------------------------------------------------------
    # 根据ID查找

    # from bson.objectid import ObjectId
    # log(BehvFile.objects.get(id="59acd72fa9ddb50138db7a2f").pk
    # log(BehvFile.objects.get(pk="59acd72fa9ddb50138db7a2f").pk
    # log(BehvFile.objects.get(id=ObjectId("59acd72fa9ddb50138db7a2f")).pk
    # log(BehvFile.objects.get(pk=ObjectId("59acd72fa9ddb50138db7a2f")).pk

    # -------------------------------------------------------------------------
    # 引用

    # ReferenceField: 可以直接引用
    # log(BehvFile.objects.get(pk="59acdf3ca9ddb51facd99ebb", file_path="xxx")._sample.pk

    # -------------------------------------------------------------------------

    # test_json()
    # test_meta()

    # test_add_sample()
    # test_add_sample_list()

    # -------------------------------------------------------------------------

    # ret = BehvHostOs.from_json(json.dumps({"platform": "windows"})).save()
    # log(ret.to_json()

    FileType.from_json(json.dumps({"name": "x", "desc": "xx"})).save()

    # -------------------------------------------------------------------------

    log("finish ...")


# -------------------------------------------------------------------------
# ENF OF FILE
# -------------------------------------------------------------------------
