# -*- coding: utf-8 -*-

"""
1. 删除重复的 -> 获取 -> 添加数据库

"""

# -------------------------------------------------------------------------

import pefile
import peutils


from malwrdb_models import *


import malwrdb_util
import malwrdb_settings
import analyze_magic


# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)


# -------------------------------------------------------------------------


def _analyze_pe_headers(sample_id, pe, is_overwrite=False):
    """
        分析 PE 各种头/基本结构

        - Dos Header
        - Nt Header
            - File Header
            - Optional Header
                - Data Directories
    """
    if is_overwrite or PeDosHeader.objects(_sample_id=sample_id).count() == 0:

        # 删除重复的

        q = PeDosHeader.objects(_sample_id=sample_id)
        if q.count() != 0:
            log("delete existing PeDosHeader item")
            q.delete()

        # 获取

        dos_header = pe.DOS_HEADER.dump_dict()
        dos_header.pop("Structure")

        # 添加数据库

        db_dos_header = PeDosHeader(**dos_header)
        db_dos_header._sample_id = sample_id
        db_dos_header.save()

    if is_overwrite or PeNtHeader.objects(_sample_id=sample_id).count() == 0:

        # 删除重复的

        q = PeNtHeader.objects(_sample_id=sample_id)
        if q.count() != 0:
            log("delete existing PeNtHeader item")
            q.delete()

        # 获取

        file_header = pe.FILE_HEADER.dump_dict()
        file_header.pop("Structure")
        optional_header = pe.OPTIONAL_HEADER.dump_dict()
        optional_header.pop("Structure")
        optional_header["_data_directories"] = {}  # 为下面的 DataDirectories 准备
        nt_header = pe.NT_HEADERS.dump_dict()
        nt_header.pop("Structure")

        # 添加数据库

        db_nt_header = PeNtHeader(**nt_header)
        db_nt_header._sample_id = sample_id
        db_nt_header.file_header = file_header
        db_nt_header.optional_header = optional_header
        for data_dir in pe.OPTIONAL_HEADER.DATA_DIRECTORY:
            dict_ = data_dir.dump_dict()
            db_nt_header.optional_header["_data_directories"][dict_.pop("Structure")] = dict_
        db_nt_header.save()


def _analyze_pe_packer_compiler(sample_id, pe, is_overwrite=False):
    """
        编译器和壳信息
    """
    if is_overwrite or PackerCompiler.objects(_sample_id=sample_id).count() == 0:

        sig = peutils.SignatureDatabase(malwrdb_settings.win_peid_signature_path)
        packer_compiler = sig.match(pe, ep_only=True)
        if packer_compiler is not None:

            # 删除重复的

            q = PackerCompiler.objects(_sample_id=sample_id)
            if q.count() != 0:
                log("delete existing PackerCompiler item")
                q.delete()

            # 获取 - 添加数据库

            db_packer_compiler = PackerCompiler()
            db_packer_compiler._sample_id = sample_id
            db_packer_compiler.raw = packer_compiler[0]
            db_packer_compiler.save()

        else:
            log("identifing pe file packer/compiler failed")


def _analyze_pe_sections(sample_id, pe, is_overwrite=False):
    """
        段
    """
    if is_overwrite or PeSection.objects(_sample_id=sample_id).count() == 0:

        # 删除重复的

        q = PeSection.objects(_sample_id=sample_id)
        if q.count() != 0:
            log("delete existing PeSection item")
            q.delete()

        for section in pe.sections:

            # 获取

            pe_section = section.dump_dict()
            pe_section.pop("Structure")
            pe_section_ = {}
            for (k, v) in pe_section.items():
                pe_section_[k] = v["Value"]

            # 添加数据库

            db_pe_section = PeSection(**pe_section_)
            db_pe_section._sample_id = sample_id
            db_pe_section.save()


def _analyze_pe_import_items(sample_id, pe, is_overwrite=False):
    """
        PE 文件导入表信息
        参照 pefil.py 的 dump 过程
    """
    pass


def _analyze_pe_export_items(sample_id, pe, is_overwrite=False):

    # export items
    pass


def _analyze_pe_version_attr(sample_id, pe, is_overwrite=False):
    """
        数据库中存储 PE 文件版本信息

        # TODO: 这里把值都改为字符串了, 不能这样...
    """
    version_dict = {}
    if hasattr(pe, 'VS_VERSIONINFO'):
        if hasattr(pe, 'FileInfo'):
            for entry in pe.FileInfo:

                if hasattr(entry, 'StringTable'):
                    for st_entry in entry.StringTable:
                        for str_entry in st_entry.entries.items():

                            # yes... it annoyed me that much .. ocd whatttt
                            if 'OriginalFilename' in str_entry:
                                version_dict[malwrdb_util.convert_to_printable(str_entry[0])] = malwrdb_util.convert_to_printable(str_entry[1])
                            else:
                                version_dict[malwrdb_util.convert_to_printable(str_entry[0])] = malwrdb_util.convert_to_printable(str_entry[1])

                elif hasattr(entry, 'Var'):
                    for var_entry in entry.Var:
                        if hasattr(var_entry, 'entry'):
                            version_dict[malwrdb_util.convert_to_printable(var_entry.entry.keys()[0])] = var_entry.entry.values()[0]

    if len(version_dict) != 0:

        version_dict["_sample_id"] = sample_id
        # col_pe_version.insert_one(version_dict)


def _analyze_pe_ca_certificate(sample_id, pe, is_overwrite=False):

    # signature
    pass


def _analyze_pe_resources(sample_id, pe, is_overwrite=False):
    # 资源
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:

            if resource_type.name is not None:
                name = "%s" % resource_type.name
            else:
                name = "%s" % pefile.RESOURCE_TYPE.get(resource_type.struct.Id)
            if name is not None:
                name = "%d" % resource_type.struct.Id

            if hasattr(resource_type, 'directory'):
                for resource_id in resource_type.directory.entries:
                    if hasattr(resource_id, 'directory'):
                        for resource_lang in resource_id.directory.entries:

                            data = pe.get_data(resource_lang.data.struct.OffsetToData, resource_lang.data.struct.Size)
                            filetype = analyze_magic.guess_binary_type(data),
                            # col_pe_resource.insert_one({
                            #     "_sample_id": sample_id,
                            #     "_binary": data,
                            #     "name": name,
                            #     "offset": resource_lang.data.struct.OffsetToData,
                            #     "size": resource_lang.data.struct.Size,
                            #     "filetype": analyze_magic.guess_binary_type(data),
                            #     "lang": pefile.LANG.get(resource_lang.data.lang, '*unknown*'),
                            #     "sublang": pefile.get_sublang_name_for_lang(resource_lang.data.lang, resource_lang.data.sublang),
                            #     "file_ratio": 0,
                            # })


# -------------------------------------------------------------------------


def _analyze_pe_tls_callbacks(sample_id, pe, is_overwrite=False):
    """
        TLS 回调函数在程序入口点之前就能获得程序控制权，先于 main 函数执行
    """
    if is_overwrite or PeSuspecious.objects(_sample_id=sample_id, suspecious_type="tls_callback").count() == 0:

        # 删除重复的

        q = PeSuspecious.objects(_sample_id=sample_id, suspecious_type="tls_callback")
        if q.count() != 0:
            log("delete existing PeSuspecious-tls_callback item")
            q.delete()

        # 获取

        callbacks = []
        if (hasattr(pe, 'DIRECTORY_ENTRY_TLS') and
                pe.DIRECTORY_ENTRY_TLS and
                pe.DIRECTORY_ENTRY_TLS.struct and
                pe.DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks):
            callback_array_rva = pe.DIRECTORY_ENTRY_TLS.struct.AddressOfCallBacks - pe.OPTIONAL_HEADER.ImageBase
            idx = 0
            while True:
                func = pe.get_dword_from_data(pe.get_data(callback_array_rva + 4 * idx, 4), 0)
                if func == 0:
                    break
                callbacks.append(func)
                idx += 1

        # 获取 - 添加数据库

        pe_suspecious = PeSuspecious()
        pe_suspecious._sample_id = sample_id
        pe_suspecious.suspecious_type = "tls_callback",
        pe_suspecious.suspecious_content = ["0x%X, " % c for c in callbacks]


def _analyze_pe_ep(sample_id, pe, is_overwrite=False):
    """
        检查 PE 入口是否可疑
    """
    if is_overwrite or PeSuspecious.objects(_sample_id=sample_id, suspecious_type="entry_point").count() == 0:

        # 删除重复的

        q = PeSuspecious.objects(_sample_id=sample_id, suspecious_type="entry_point")
        if q.count() != 0:
            log("delete existing PeSuspecious-entry_point item")
            q.delete()

        # 获取

        suspecious_content = ""
        ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
        for sec in pe.sections:
            if (ep >= sec.VirtualAddress) and ep < (sec.VirtualAddress + sec.Misc_VirtualSize):

                name = sec.Name.replace('\x00', '')
                if name not in ['.text', '.code', 'CODE', 'INIT', 'PAGE']:
                    suspecious_content = "in bad named section: %s" % name
                    break

        # 添加数据库

        pe_suspecious = PeSuspecious()
        pe_suspecious._sample_id = sample_id
        pe_suspecious.suspecious_type = "entry_point"
        pe_suspecious.suspecious_content = suspecious_content
        pe_suspecious.save()


def _analyze_pe_yara(sample_id, pe):
    """
        匹配 yara
    """
    pass


def _analyze_pe_pdb_path(sample_id, pe):
    pass


def _analyze_pe_extra_bytes(sample_id, pe):
    # 检查 PE 的 ExtraBytes
    pass


def _analyze_pe_function(sample_id, pe):
    """
        - 长时间Sleep
    """
    pass


# -------------------------------------------------------------------------


def analyze_pe_basic(sample, sample_binary, is_overwrite=False):
    """
        分析 PE 基本内容
    """
    is_overwrite = True

    pe = pefile.PE(data=sample_binary)

    # sample.file_type = ""

    _analyze_pe_headers(sample.id, pe, is_overwrite=is_overwrite)
    _analyze_pe_packer_compiler(sample.id, pe, is_overwrite=is_overwrite)
    _analyze_pe_sections(sample.id, pe, is_overwrite=is_overwrite)
    _analyze_pe_import_items(sample.id, pe, is_overwrite=is_overwrite)
    _analyze_pe_export_items(sample.id, pe, is_overwrite=is_overwrite)
    _analyze_pe_version_attr(sample.id, pe, is_overwrite=is_overwrite)
    _analyze_pe_ca_certificate(sample.id, pe, is_overwrite=is_overwrite)
    _analyze_pe_resources(sample.id, pe, is_overwrite=is_overwrite)


def analyze_pe_advanced(sample, sample_binary):
    # 分析 PE 高端内容
    pe = pefile.PE(data=sample_binary)
    _analyze_pe_yara(sample.id, pe)


# -------------------------------------------------------------------------
# ENF OF FILE
# -------------------------------------------------------------------------
