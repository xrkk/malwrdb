# -*- coding: utf-8 -*-

"""
"""

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# 1. .NET
# 2. Andorid等
# 3. 内容输入是个比较大的问题

# section 是静态的, segment 是动态的

# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# util - 不属于sample


class export_item:  # 导出函数信息，包括 API
    _id = ""

    name = ""
    module_name = ""
    offset = ""

    pass


# -------------------------------------------------------------------------
# PE


class pe_data_directory:
    _id = ""
    _pe_optional_header_id = ""
    _binary = ""

    name = ""
    address = 0
    size = 0
    pe_section_id = 0                    # - pe_section
    # ...

    pass


class pe_optional_header:
    _id = ""
    _pe_nt_header_id = ""
    _binary = ""

    magic = ""
    # ...
    pe_data_directory_ids = []           # [pe_data_directory]

    pass


class pe_file_header:
    _id = ""
    _pe_nt_header_id = ""
    _binary = ""

    machine = ""
    # ...

    pass


class pe_nt_header:
    _id = ""
    _sample_id = ""
    _binary = ""

    pe_file_header_id = ""                # pe_file_header
    pe_optional_header_id = ""            # pe_optional_header

    pass


class pe_dos_header:
    _id = ""
    _sample_id = ""
    _binary = ""

    e_magic = ""
    # ...

    pass


# -


class pe_debug_info:
    _id = ""
    _sample_id = ""

    pass


class pe_dos_stub:
    _id = ""
    _sample_id = ""
    _binary = ""

    size = ""
    entropy = ""
    stub_msg = ""                         # This file can't be run in ....

    pass


class pe_attribute_basic:  # 基础属性
    _id = ""
    _sample_id = ""

    # "x86" "x64" "armx86" "armx64"
    cpu = ""                         # cpu结构
    # ...

    extra_start = 0                  # ffi 提示的 extra data
    extra_size = 0                   # ffi 提示的 extra data

    entry_point = 0                  # 入口

    subsystem = ""                   # 子系统

    pass


class pe_packer_compiler:  # 壳和编译器
    _id = ""
    _sample_id = ""

    name = ""     # vs/gcc/... or upx/vmp/...
    version = 0
    # ...

    # ".NET" "C#" "VB" "C/C++" "C" "C++" "Delphi" "Go" "Python"
    lang = ""                    # 开发语言
    compile_time = ""

    raw = ""                     # raw

    pass


class pe_section:  # PE样本的段
    _id = ""
    _sample_id = ""
    _binary = ""

    name = ""
    base = 0
    # ...

    hash_md5 = ""
    hash_shax = ""

    file_ratio = 0                      # 占比重

    # ? function_ids = []                               # (可选)函数列表 - [function]

    # 可选

    string_ids = []                                 # (可选)字符串 - [base_string]

    pass


class pe_import_item:  # PE样本的导入表
    _id = ""
    _sample_id = ""

    # 必须

    name = ""
    # ...

    pass


class pe_export_item:  # PE样本的导出表
    _id = ""
    _sample_id = ""

    name = ""
    # ...

    pass


class pe_version:  # PE样本的属性
    _id = ""
    _sample_id = ""                                 # 所属样本

    comments = ""                                  # 备注
    company_name = ""                              #
    file_description = ""                          #
    file_version = ""                              #
    legal_copyright = ""                           #
    product_name = ""                              #

    pass


class pe_signature:  # PE样本签名的属性
    _id = ""
    _sample_id = ""

    date_start = ""                  # 起始日期
    date_end = ""                    # 终止日期
    serial_number = ""               # 序列号
    user = ""                        # 使用者
    licensor = ""                    # 颁发者

    check_result_when_analyze = ""                # 分析时验证是否有效

    pass


class pe_resource:  # PE样本的资源
    _id = ""
    _sample_id = ""
    _binary = ""

    # ...

    file_ratio = 0                   # 占比例

    pass


class pe_suspecious:
    """
        接口:
            -
    """
    _id = ""
    _sample_id = ""

    # "extra_bytes" ""
    suspecious_type = ""                       # 类型
    suspecious_content = ""                    # 内容
    suspecious_comment = ""                    # 用户评论

    pass

# -------------------------------------------------------------------------
# ELF


class elf_attribute_basic:
    _id = ""
    _sample_id = ""

    # "x86" "x64" "armx86" "armx64"
    arch = ""                        # cpu结构
    # ...

    pass


class elf_packer_compiler:
    _id = ""
    _sample_id = ""

    name = ""     # vs/gcc/... or upx/vmp/...
    version = 0
    # ...

    compile_time = ""

    pass


class elf_section:
    _id = ""
    _sample_id = ""

    # ...

    pass


class elf_import_item:
    _id = ""
    _sample_id = ""

    # ...

    pass


class elf_export_item:
    _id = ""
    _sample_id = ""

    # ...

    pass


class elf_attibute:
    pass


class elf_signature:
    pass


# -------------------------------------------------------------------------


class function:  # 段包含的函数, 不管能不能 F5
    _id = ""
    _segement_id = ""          # 所属段 - [pe_section/elf_section]
    _binary = ""

    # 必须

    function_size = 0
    function_offset = 0

    # "library" "regular" "shellcode"
    function_type = ""                # 函数类型

    bin_diff_map = ""                 # 用于函数相似性判断的内容

    pass


class resolved_struct:  # 分析出的数据结构
    _id = ""
    _sample_id = ""

    struct_size = 0
    struct_details = ""

    pass


class loaded_module:  # 运行时实际加载的磁盘模块
    # [保留]
    _id = ""
    _sample_id = ""

    file_path_id = ""             # 模块在磁盘的路径 - file_path
    module_base = 0               # 模块基址
    module_size = 0               # 模块大小

    pass


# -------------------------------------------------------------------------
# ENF OF FILE
# -------------------------------------------------------------------------
