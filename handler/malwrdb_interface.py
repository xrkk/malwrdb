# -*- coding: utf-8 -*-


# -------------------------------------------------------------------------


import json


# -------------------------------------------------------------------------


TIME_DURATION_LEVEL_1 = 1
TIME_DURATION_LEVEL_2 = 2
TIME_DURATION_LEVEL_3 = 3
TIME_DURATION_LEVEL_4 = 4
TIME_DURATION_LEVEL_5 = 5


# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)


# -------------------------------------------------------------------------


from proto_def.malwrdb_proto_pb2 import *
from malwrdb_implmentation import *
from bson.objectid import ObjectId
from google.protobuf.json_format import Parse


# -------------------------------------------------------------------------
# 接口 - test


def _test_pe_by_sample_id(params):
    _check_params_id(params, "sample_id")

    test_pe_by_sample_id(ObjectId(params["sample_id"]))


def _test_analyze_win_pe(params):
    _check_params_string(params, "sample_path")

    test_analyze_win_pe(params["sample_path"])


def _test_analyze_pe_sample_id(params):
    _check_params_id(params, "sample_id")

    test_analyze_pe_sample_id(ObjectId(params["sample_id"]))


# -------------------------------------------------------------------------
# 接口 - 行为主机


"""
需求与接口：
    - 添加主机
        - 界面: Form, 内容为空
        - add_host_os(platform, version, sp, arch, desc, author)
    - 克隆主机
        - 界面: Form, 内容为克隆的主机的内容(不显示author)
        - (->add_host_os)
    - (EX)删除主机
        - 界面: 不是当前用户添加的, 不显示删除选项
        - del_host_os(_id)
        - 问题:
            - 引用这条目的行为咋办?
问题:
    1. "用户" 该如何传递??
"""


def _add_host_os_proto(msg):
    add_host_os(msg)


def _add_host_os_json(params):
    _add_host_os_proto(Parse(json.dumps(params), AddHostOsMessage()))


def _clone_host_os_proto(msg):
    clone_host_os(msg)


def _clone_host_os_json(params):
    _clone_host_os_proto(Parse(params, CloneHostOsMessage()))


def _del_host_os_proto(msg):
    del_host_os(msg)


def _del_host_os_json(params):
    _del_host_os_proto(Parse(params, DelHostOsMessage()))


# -------------------------------------------------------------------------
# 接口 - comm_target


"""
结构:
    domain = ""               # 域名字符串
    ip_addr = ""              # IP地址字符串
    port = 0                  # 端口

接口:
    - 添加通信目标
        - 在通信目标列表中添加
            - 界面: Form, 内容空
            - add_comm_target_list([port, ip=None, domain=None])
        - 在样本详情页面添加
            - 界面: Form, 内容空
            - add_comm_target_list_to_sample(sample_id, [port, ip=None, domain=None])
    x 更新通信目标
        - 通信目标一旦添加, 不可修改, 只可删除
    - (EX)删除通信目标
        - 界面: 判断引用此通信目标的样本是否只有此样本
            - 是: 弹窗要求确认
                - del_comm_target_list(comm_target_id_list)
            - 否: 是否所有关联样本都只与当前用户有关
                - 否: 弹窗提示不可删除, 需跟其他用户将样本断开连接后方可删除
                - 是: 弹窗确认是否断开所有与样本的连接, 并删除通信目标
                    - del_comm_target_list_recur(comm_target_id_list)
    - 断开通信目标与此样本的连接
        - (EX)界面: 判断此通信目标是否只与此样本关联
            - 是: 弹窗提示用户是断开连接后是否删除通信目标
                - 是:
                    - (->del_comm_target_list)
                - 否:
                    - disconnect_comm_target_list(sample_id, comm_target_id_list)
            - (OK)否: 弹窗提示是否断开连接
                - 是:
                    - (->disconnect_comm_target_list)
    - (EXX)网络查询通信目标信息
        - ??
    - (EXX)查找相同目标/ip/域名/端口的样本
        - 如果是域名的话, 解析下ip地址, 再用ip地址搜一遍
        - 界面: 按钮
        - search_similar_sample_based_on_comm_target_list(comm_target_id_list)
        - 问题:
            - 谁来做?
            - 结果是否保存数据库?
"""


def _add_comm_target_proto(msg):
    add_comm_target(msg)


def _add_comm_target_json(params):
    _add_comm_target_proto(Parse(json.dumps(params), AddCommTargetMessage()))


def _add_comm_target_to_sample_proto(msg):
    add_comm_target_to_sample(msg)


def _add_comm_target_to_sample_json(params):
    _add_comm_target_to_sample_proto(Parse(json.dumps(params), AddCommTargetToSampleMessage()))


def _connect_comm_target_proto(msg):
    connect_comm_target(msg)


def _connect_comm_target_json(params):
    _connect_comm_target_proto(Parse(json.dumps(params), ConnectCommTargetMessage()))


def _disconnect_comm_target_proto(msg):
    disconnect_comm_target(msg)


def _disconnect_comm_target_json(params):
    _disconnect_comm_target_proto(Parse(json.dumps(params), DisconnectCommTargetMessage()))


# -------------------------------------------------------------------------
# 接口 - 攻击目标


"""
结构:
    continent_list = []            # 大洲
    country_list = []              # 攻击国家
    industry_list = []             # 攻击行业
"""


def _add_attack_target_proto(msg):
    add_attack_target(msg)


def _add_attack_target_json(params):
    _add_attack_target_proto(Parse(json.dumps(params), AddAttackTargetMessage()))


def _add_attack_target_to_sample_proto(msg):
    add_attack_target_to_sample(msg)


def _add_attack_target_to_sample_json(params):
    _add_attack_target_to_sample_proto(Parse(json.dumps(params), AddAttackTargetToSampleMessage()))


def _connect_attack_target_proto(msg):
    connect_attack_target(msg)


def _connect_attack_target_json(params):
    _connect_attack_target_proto(Parse(json.dumps(params), ConnectAttackTargetMessage()))


def _disconnect_attack_target_proto(msg):
    disconnect_attack_target(msg)


def _disconnect_attack_target_json(params):
    _disconnect_attack_target_proto(Parse(json.dumps(params), DisconnectAttackTargetMessage()))


# -------------------------------------------------------------------------
# 接口 - VT信息


"""
结构:
    _sample_id = ""
    vt_url = ""                     # url
    vt_result = ""                  # 扫描结果, 例如: "23/45"
"""


# -------------------------------------------------------------------------
# 接口 - Hybrid信息


"""
结构:
    _sample_id = ""
    hybrid_url = ""                     # url
"""


# -------------------------------------------------------------------------
# 接口 - 测试


def _request_test_proto(msg):
    request_test(msg)


def _request_test_json(params):
    _request_test_proto(Parse(json.dumps(params), TestMessage()))


# -------------------------------------------------------------------------
# 接口 - 分析


"""
结构:
    _binary = ""
    # 必须
    # "exe" "dll" "elf" "apk"                      # 可执行文件
    # "eml"                                        # 邮件
    # "js" "vbs" "powershell" "bat"                # 脚本
    # "txt" "word" "excel" "ppt" "hta" "html"      # 文档
    # "dat"                                        # 数据文件, 包括样本释放的/资源/...
    # "pcap"                                       # 数据包文件等辅助分析的
    file_type = ""                                 # 样本类型 - 字符串
    hash_md5 = ""                                  # MD5
    hash_sha1 = ""                                 # 多种哈希值
    hash_sha256 = ""                               # SHA256, 验证唯一性(PHP输入)
    ssdeep = ""                                    # fuzzy hashes
    sample_size = 0                                # 样本大小
    file_name = ""                                 # 文件名称(PHP输入)
    # "macOS" "iOS" "Solaris" "Linux" "Windows" "Android" "IoT"
    platform = ""                                  # 平台
    parent__sample_id = ""                         # 父样本
    # 样本释放的:
    # "auto_disk"                                  # 样本释放到磁盘
    # "auto_memory_unpack"                         # 样本带壳, 到OEP之后dump之后用脚本修复的 ??
    # "auto_memory_module_heap"                    # 堆上的内存模块
    # "auto_memory_module_inject"                  # 注入的内存模块
    # "auto_memory_module_replace"                 # 替换自身的内存模块
    # "auto_memory_data_heap"                      # 堆上的数据段(解密之前的/中间的)
    # "auto_memory_data_inject"                    # 堆上的数据段(解密之前的/中间的)
    # "auto_memory_code_heap"                      # 堆上的代码段
    # "auto_memory_code_inject"                    # 注入的代码段
    # "auto_memory_code_replace"                   # 自解密的代码段
    # 用户手动填入的:
    # "manual_normal"                              # "手动"提取出来的，比如office文件中的宏(不包括下面的特殊类型)
    # "manual_module_unpacked_tool"                # 用脱壳工具脱壳
    # "manual_module_unpacked_fixed"               # 样本释放在内存中的内容直接dump出来之后修复的 ??
    # 其他的
    # "misc"                                       # 比如捕获的pcap数据包文件, 或者分析笔记、分析报告、提取的特征等
    parent__sample_to_this_type = ""               # 与父样本的关系
    #
    # entropy - 熵
    # imphash - pefile.py 自带
    #
    #
    # 可选
    # "ransomware" "trojen" "dropper" ...
    malicious_type_overall = ""                    # 总体的恶意类型
    malware_family = ""                            # 恶意代码家族
    # PE/ELF(可执行文件) - 静态 -
    # - pe_elf_attribute_basic_id = ""                 # 基本信息 - [pe_attribute_basic/elf_attribute_basic]
    # - pe_elf_section_ids = []                        # 段列表 - [pe_section/elf_section]
    # - pe_elf_import_api_ids = []                     # 导入表 - [pe_import_item/elf_import_item]
    # - pe_elf_export_api_ids = []                     # 导出表 - [pe_export_item/elf_export_item]
    # - pe_elf_packer_compiler_id = ""                 # 壳/编译器 - pe_packer_compiler/elf_packer_compiler
    # - pe_elf_attribute_id = ""                       # (可选)属性 - pe_attribute/elf_attribute
    # - pe_elf_signature_id = ""                       # (可选)签名 - pe_signature/elf_signature
    # - pe_elf_resolved_struct_ids = []                # (可选)结构 - [resolved_struct]
    # - pe_elf_string_ids = []                       # (可选)字符串(到x_section里) - [base_string]
    # PE  - 静态 -
    # - pe_dos_header_id = ""                          # PE Dos 头 - pe_dos_header
    # - pe_nt_header_id = ""                           # PE NT 头 - pe_nt_header
    # ELF - 静态 -
    # ??
    # 可选 - 动态 - 行为
    # - behv_file_ids = []                             # 文件行为 - [behv_file]
    # - behv_reg_ids = []                              # 注册表行为 - [behv_reg]
    # - behv_net_ids = []                              # 网络行为 - [behv_net]
    # - behv_proc_ids = []                             # 进程行为 - [behv_proc]
    # - behv_sys_ids = []                              # 系统行为 - [behv_sys]
    # - behv_misc_dynamic_api_ids = []                 # 动态获取api的行为 - [behv_misc_dynamic_apis]
    # - behv_feature_ids = []                          # 组合的行为 - [behv_feature]
    # ...
    # 可选 - 网络信息
    # - ext_internet_vt_ids = []                       # [ext_internet_vt]
    # - ext_internet_hybrid_ids = []                   # ext_internet_hybrid
接口:
    -
"""


def _analyze_sample_list_proto(msg):
    analyze_sample_list_by_id(msg)


def _analyze_sample_list_json(params):
    """分析指定的样本"""
    _analyze_sample_list_proto(Parse(json.dumps(params), AnalyzeSampleListMessage()))


# -------------------------------------------------------------------------
# 接口 - 样本相关


def _sample_relationship_proto(msg):
    sample_relationship(msg)


def _sample_relationship_json(params):
    """设置样本父子关系"""
    _sample_relationship_proto(Parse(json.dumps(params), SampleRelationshipMessage()))


# -------------------------------------------------------------------------
# 接口 - 文件行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    file_path = ""                  # 文件路径 - file_path
    # "enum_disk"
    # "find" "create" "read" "write" "del" "copy" "move"
    # file_behv_type = ""           # 文件行为类型
接口:
    - 添加文件行为:
        - 界面: 弹框, 输入字符串数组, 选择追加还是替换
            - 追加
                - add_behv_file_list(sample_id, host_os_id_list, file_path_list)
            - 替换
                - replace_behv_file_list(sample_id, host_os_id_list, file_path_list)
    x 更新文件行为
        - 文件行为就是字符串, 没什么好更新的, 不需要就删了就行
    - 删除文件行为
        - 界面: 多选框, 选中, 点击删除
        - delete_behv_file_list(sample_id, behv_file_id)
    - 清空文件行为
        - 界面: 提示用户确认
        - clear_behv_file_list(sample_id)
    - (EX)特殊目录替换
        -
    - (EXX)查找相似
        -
问题:
    - 如果某个文件, 正好是某个"Sample", 是否提供接口做关联?
        - 否??
"""


def _append_file_behv_proto(msg):
    append_file_behv(msg)


def _append_file_behv_json(params):
    _append_file_behv_proto(Parse(json.dumps(params), AppendFileBehvMessage()))


def _replace_file_behv_proto(msg):
    replace_file_behv(msg)


def _replace_file_behv_json(params):
    _replace_file_behv_proto(Parse(json.dumps(params), ReplaceFileBehvMessage()))


def _clear_file_behv_proto(msg):
    clear_file_behv(msg)


def _clear_file_behv_json(params):
    _clear_file_behv_proto(Parse(json.dumps(params), ClearFileBehvMessage()))


# -------------------------------------------------------------------------
# 接口 - 注册表行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""        # 行为对应的操作系统 - [behv_host_os]
    reg_path = ""                     # 路径
    # reg_value = ""                  # (可选)设置的值
    # "read" "write" "create" "del"
    # reg_behv_type = ""              # 注册表操作类型
    # reg_root = ""
    # reg_path = ""                   # - [reg_path]
    # reg_key = ""
    # related_sample_ids = []         # - [Sample]
接口:
    - 添加注册表行为
        - 界面: 弹框, 输入字符串数组, 选择追加还是替换
            - 追加
                - add_behv_reg_list(sample_id, host_os_id_list, reg_path_list)
            - 替换
                - replace_behv_reg_list(sample_id, host_os_id_list, reg_path_list)
    x 更新注册表行为
        -
    - 删除注册表行为
        - delete_behv_reg_list(sample_id, behv_reg_id)
    - 清空注册表行为
        - clear_behv_reg_list(sample_id)
    - (EX)用户路径替换
        - 根路径在添加时已经被自动替换
        -
    - (EX)Key分离
        -
    - (EXX)查找相似
        -
问题:
    - 对于将二进制隐藏到注册表中的"无文件", 这里value值是很重要的
"""


def _append_reg_behv_proto(msg):
    append_reg_behv(msg)


def _append_reg_behv_json(params):
    _append_reg_behv_proto(Parse(json.dumps(params), AppendRegBehvMessage()))


def _replace_reg_behv_proto(msg):
    replace_reg_behv(msg)


def _replace_reg_behv_json(params):
    _replace_reg_behv_proto(Parse(json.dumps(params), ReplaceRegBehvMessage()))


def _clear_reg_behv_proto(msg):
    clear_reg_behv(msg)


def _clear_reg_behv_json(params):
    _clear_reg_behv_proto(Parse(json.dumps(params), ClearRegBehvMessage()))


# -------------------------------------------------------------------------
# 接口 - 网络行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    # "CnC" "P2P"
    comm_type = ""                  # 通信类型
    comm_target_id = ""             #
    binary = ""                     # 数据
    protocol = ""                   # 协议
    # related_sample_ids = []         # 涉及到的样本列表, 例如生成的pcap文件 - [Sample]
接口:
    - 添加网络行为
        -
"""


def _append_network_behv_proto(msg):
    append_network_behv(msg)


def _append_network_behv_json(json):
    _append_network_behv_proto(Parse(json.dumps(params), AppendNetworkBehvMessage()))


# -------------------------------------------------------------------------
# 接口 - 进程行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    # "check_parent_proc"                 # 检查父进程
    # "create_new_proc"                   # 创建新进程
    # "write_proc_mm"                     # 进程写入
    # "read_proc_mm"                      # 进程读取
    # "proc_enum"                         # 遍历进程
    # "check_wow64"                       # 检查是否为64位进程
    proc_behv_type = ""                   # 进程行为类型
    # create_proc_path_id = ""              # 创建进程名称 - [file_path]
    # create_proc_cmd_line_regex = ""       # 创建进程命令行的正则表达式
    # create_proc_params = ""               # 创建进程其他参数
    # read_proc_path_id = ""                # 读取进程名称 - [file_path]
    # read_proc_base = 0                    # 读取基址
    # read_proc_size = 0                    # 读取大小
    # read_proc_data_id = ""                # 读取到的内容id - [Sample]
    # write_proc_path_id = ""               # 写入进程名称 - [file_path]
    # write_proc_base = 0                   # 写入基址
    # write_proc_size = 0                   # 写入大小
    # write_proc_data_id = ""               # 写入到的内容id - [Sample]
    # "api" ...
    # proc_enum_type = ""                   # 进程遍历类型
接口:
    - 添加进程行为
"""


def _append_proc_behv_proto(msg):
    append_proc_behv(msg)


def _append_proc_behv_json(params):
    _append_proc_behv_proto(Parse(json.dumps(params), AppendProcBehvMessage()))


def _replace_proc_behv_proto(msg):
    replace_proc_behv(msg)


def _replace_proc_behv_json(params):
    _replace_proc_behv_proto(Parse(json.dumps(params), ReplaceProcBehvMessage()))


def _clear_proc_behv_proto(msg):
    clear_proc_behv(msg)


def _clear_proc_behv_json(params):
    _clear_proc_behv_proto(Parse(json.dumps(params), ClearProcBehvMessage()))


# -------------------------------------------------------------------------
# 接口 - 系统行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    # "get_computer_name"
    # "get_domain_name"
    # "get_computer_version"
    # "get_system_info"
    # "check_is_64bit"
    # "enum_driver"
    sys_behv_type = ""           # 系统行为类型
接口:
    -
"""


def _append_sys_behv_proto(msg):
    append_sys_behv(msg)


def _append_sys_behv_json(params):
    _append_sys_behv_proto(Parse(json.dumps(params), AppendSysBehvMessage()))


def _replace_sys_behv_proto(msg):
    replace_sys_behv(msg)


def _replace_sys_behv_json(params):
    _replace_sys_behv_proto(Parse(json.dumps(params), ReplaceSysBehvMessage()))


def _clear_sys_behv_proto(msg):
    clear_sys_behv(msg)


def _clear_sys_behv_json(params):
    _clear_sys_behv_proto(Parse(json.dumps(params), ClearSysBehvMessage()))


# -------------------------------------------------------------------------
# 接口 - 窗口行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    # "register" "create" "destroy" "check"
    window_behv_type = ""           # 窗口事件类型
    window_name_string = ""         # 窗口名称的正则表达式
"""


def _append_window_behv_proto(msg):
    append_window_behv(msg)


def _append_window_behv_json(params):
    _append_window_behv_proto(Parse(json.dumps(params), AppendWindowBehvMessage()))


def _replace_window_behv_proto(msg):
    replace_window_behv(msg)


def _replace_window_behv_json(params):
    _replace_window_behv_proto(Parse(json.dumps(params), ReplaceWindowBehvMessage()))


def _clear_window_behv_proto(msg):
    clear_window_behv(msg)


def _clear_window_behv_json(params):
    _clear_window_behv_proto(Parse(json.dumps(params), ClearWindowBehvMessage()))


# -------------------------------------------------------------------------
# 接口 - 服务行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    # _risk = 0                        # 威胁等级
    # "create" "open" "del" "stop"
    service_behv_type = ""           # 服务事件的类型
    service_name_string = ""         # 服务名称的正则表达式
    service_displayname_string = ""  # 服务显示名的正则表达式
    service_binary_path_id = ""      # 服务路径 - [file_path]
    service_other_params = ""        # 其他的服务参数
"""


def _append_service_behv_proto(msg):
    append_service_behv(msg)


def _append_service_behv_json(params):
    _append_service_behv_proto(Parse(json.dumps(params), AppendServiceBehvMessage()))


def _replace_service_behv_proto(msg):
    replace_service_behv(msg)


def _replace_service_behv_json(params):
    _replace_service_behv_proto(Parse(json.dumps(params), ReplaceServiceBehvMessage()))


def _clear_service_behv_proto(msg):
    clear_service_behv(msg)


def _clear_service_behv_json(params):
    _clear_service_behv_proto(Parse(json.dumps(params), ClearServiceBehvMessage()))


# -------------------------------------------------------------------------
# 接口 - 互斥体/事件行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    # "create" "open" "release"
    mutex_behv_type = []            # 互斥体事件类型
    mutex_name_string = ""          # 互斥体名称的正则表达式
"""


def _append_mutex_behv_proto(msg):
    append_mutex_behv(msg)


def _append_mutex_behv_json(params):
    _append_mutex_behv_proto(Parse(json.dumps(params), AppendMutexBehvMessage()))


def _replace_mutex_behv_proto(msg):
    replace_mutex_behv(msg)


def _replace_mutex_behv_json(params):
    _replace_mutex_behv_proto(Parse(json.dumps(params), ReplaceMutexBehvMessage()))


def _clear_mutex_behv_proto(msg):
    clear_mutex_behv(msg)


def _clear_mutex_behv_json(params):
    _clear_mutex_behv_proto(Parse(json.dumps(params), ClearMutexBehvMessage()))


# -------------------------------------------------------------------------
# 接口 - 动态获取api行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    # "GetProcAddress"
    # "manual"
    resolve_type = ""                        # 解析类型
    target_export_item_id = ""               # 获取的函数信息 - export_item
"""

# -------------------------------------------------------------------------
# 接口 - 获取DNS行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    invoke_type = ""
"""


# -------------------------------------------------------------------------
# 接口 - 随便什么行为


def _append_whatever_behv_proto(msg):
    append_whatever_behv(msg)


def _append_whatever_behv_json(params):
    _append_whatever_behv_proto(Parse(json.dumps(params), AppendWhateverBehvMessage()))


def _replace_whatever_behv_proto(msg):
    replace_whatever_behv(msg)


def _replace_whatever_behv_json(params):
    _replace_whatever_behv_proto(Parse(json.dumps(params), ReplaceWhateverBehvMessage()))


def _del_whatever_behv_proto(msg):
    del_whatever_behv(msg)


def _del_whatever_behv_json(params):
    _del_whatever_behv_proto(Parse(json.dumps(params), DelWhateverBehvMessage()))


def _clear_whatever_behv_proto(msg):
    clear_whatever_behv(msg)


def _clear_whatever_behv_json(params):
    _clear_whatever_behv_proto(Parse(json.dumps(params), ClearWhateverBehvMessage()))


# -------------------------------------------------------------------------
# 接口 - 组合行为


"""
结构:
    _sample_id = ""
    _behv_host_os_id_list = ""      # 行为对应的操作系统 - [behv_host_os]
    # 保护类型
    # "anti-av"
    # "anti-sandbox"
    # "anti-debug"
    # 加密类型
    # "encrypt_data"
    # "encrypt_file"
    # "encrypt_disk" - encrypt_file + enum_file + ...
    # 设置自启动
    # "set_auto_run"
    #   - 设置注册表Run/...
    #   - 放到磁盘根目录下, 创建autorun.ini等文件
    # 驻留
    # "set_persistence"
    #   - 驻留到注册表
    # 其他
    # "trigger_vul"      # 触发漏洞
    # "spread"           # 传播
    # "memory_module"    # 内存模块
    # "enum_files"       # 枚举文件
    # "enum_disk"        # 枚举磁盘
    # "dll_hijact"       # DLL 劫持
    feature_gole = ""           # 行为目的

    # "dll-hiject" "sleep" "check_proc"
    # feature_type = ""           # 行为类型
    # 可选 - behv_feature的组合 - 比如 "encrypt_disk" = "encrypt_data" + "enum_files"
    # behv_feature_ids = []        # [behv_feature]
    # 可选 - 其他behv的组合
    # behv_file_ids = []            # [behv_file]
    # behv_reg_ids = []             # [behv_reg]
    # behv_net_ids = []             # [behv_net]
    # behv_proc_ids = []            # [behv_proc]
    # behv_sys_ids = []             # [behv_sys]
    # behv_misc_ids = []            # [behv_misc]
    # 可选 - 没涉及到behv
    # function_ids = []             # 函数列表
"""


def _append_behv_feature_proto(msg):
    append_behv_feature(msg)


def _append_behv_feature_json(params):
    _append_behv_feature_proto(Parse(json.dumps(params), AppendBehvFeatureMessage()))


def _replace_behv_feature_proto(msg):
    replace_behv_feature(msg)


def _replace_behv_feature_json(params):
    _replace_behv_feature_proto(Parse(json.dumps(params), ReplaceBehvFeatureMessage()))


def _clear_behv_feature_proto(msg):
    clear_behv_feature(msg)


def _clear_behv_feature_json(params):
    _clear_behv_feature_proto(Parse(json.dumps(params), ClearBehvFeatureMessage()))


# -------------------------------------------------------------------------
# 样本的网络信息


def _update_vt_info_proto(msg):
    update_vt_info(msg)


def _update_vt_info_json(params):
    _update_vt_info_proto(Parse(json.dumps(params), UpdateVtInfoMessage()))


def _update_hybrid_info_proto(msg):
    update_hybrid_info(msg)


def _update_hybrid_info_json(params):
    _update_hybrid_info_proto(Parse(json.dumps(params), UpdateHybridInfoMessage()))


def _update_reverseit_info_proto(msg):
    update_reverseit_info(msg)


def _update_reverseit_info_json(params):
    _update_reverseit_info_proto(Parse(json.dumps(params), UpdateReverseItInfoMessage()))


def _update_malwr_info_proto(msg):
    update_malwr_info(msg)


def _update_malwr_info_json(params):
    _update_malwr_info_proto(Parse(json.dumps(params), UpdateMalwrInfoMessage()))


# -------------------------------------------------------------------------
# 从网络提取样本


# -------------------------------------------------------------------------
# 从网络获取 Yara 规则


# -------------------------------------------------------------------------
# 中英对照


# 文件类型


def _add_file_type_proto(msg):
    add_file_type(msg)


def _add_file_type_json(params):
    _add_file_type_proto(Parse(json.dumps(params), AddFileTypeMessage()))


def _del_file_type_proto(msg):
    del_file_type(msg)


def _del_file_type_json(params):
    _del_file_type_proto(Parse(json.dumps(params), DelFileTypeMessage()))


# 平台


def _add_platform_proto(msg):
    add_platform(msg)


def _add_platform_json(params):
    _add_platform_proto(Parse(json.dumps(params), AddPlatformMessage()))


def _del_platform_proto(msg):
    del_platform(msg)


def _del_platform_json(params):
    _del_platform_proto(Parse(json.dumps(params), DelPlatformMessage()))


# 样本关系


def _add_sample_relationship_type_proto(msg):
    add_sample_relationship_type(msg)


def _add_sample_relationship_type_json(params):
    _add_sample_relationship_type_proto(Parse(json.dumps(params), AddSampleRelationshipTypeMessage()))


def _del_sample_relationship_type_proto(msg):
    del_sample_relationship_type(msg)


def _del_sample_relationship_type_json(params):
    _del_sample_relationship_type_proto(Parse(json.dumps(params), DelSampleRelationshipTypeMessage()))


# 总体的恶意类型


def _add_overall_malicious_type_proto(msg):
    add_overall_malicious_type(msg)


def _add_overall_malicious_type_json(params):
    _add_overall_malicious_type_proto(Parse(json.dumps(params), AddOverallMaliciousTypeMessage()))


def _del_overall_malicious_type_proto(msg):
    del_overall_malicious_type(msg)


def _del_overall_malicious_type_json(params):
    _del_overall_malicious_type_proto(Parse(json.dumps(params), DelOverallMaliciousTypeMessage()))


# 恶意代码家族


def _add_malware_family_proto(msg):
    add_malware_family(msg)


def _add_malware_family_json(params):
    _add_malware_family_proto(Parse(json.dumps(params), AddMalwareFamilyMessage()))


def _del_malware_family_proto(msg):
    del_malware_family(msg)


def _del_malware_family_json(params):
    _del_malware_family_proto(Parse(json.dumps(params), DelMalwareFamilyMessage()))


# 编程语言


def _add_programing_lang_proto(msg):
    add_programing_lang(msg)


def _add_programing_lang_json(params):
    _add_programing_lang_proto(Parse(json.dumps(params), AddProgramingLangMessage()))


def _del_programing_lang_proto(msg):
    del_programing_lang(msg)


def _del_programing_lang_json(params):
    _del_programing_lang_proto(Parse(json.dumps(params), DelProgramingLangMessage()))


# 函数类型


def _add_function_type_proto(msg):
    add_function_type(msg)


def _add_function_type_json(params):
    _add_function_type_proto(Parse(json.dumps(params), AddFunctionTypeMessage()))


def _del_function_type_proto(msg):
    del_function_type(msg)


def _del_function_type_json(params):
    _del_function_type_proto(Parse(json.dumps(params), DelFunctionTypeMessage()))


# 进程行为类型


def _add_proc_behv_type_proto(msg):
    add_proc_behv_type(msg)


def _add_proc_behv_type_json(params):
    _add_proc_behv_type_proto(Parse(json.dumps(params), AddProcBehvTypeMessage()))


def _del_proc_behv_type_proto(msg):
    del_proc_behv_type(msg)


def _del_proc_behv_type_json(params):
    _del_proc_behv_type_proto(Parse(json.dumps(params), DelProcBehvTypeMessage()))


# 系统行为类型


def _add_sys_behv_type_proto(msg):
    add_sys_behv_type(msg)


def _add_sys_behv_type_json(params):
    _add_sys_behv_type_proto(Parse(json.dumps(params), AddSysBehvTypeMessage()))


def _del_sys_behv_type_proto(msg):
    del_sys_behv_type(msg)


def _del_sys_behv_type_json(params):
    _del_sys_behv_type_proto(Parse(json.dumps(params), DelSysBehvTypeMessage()))


# 组合行为类型


def _add_behv_feature_type_proto(msg):
    add_behv_feature_type(msg)


def _add_behv_feature_type_json(params):
    _add_behv_feature_type_proto(Parse(json.dumps(params), AddBehvFeatureTypeMessage()))


def _del_behv_feature_type_proto(msg):
    del_behv_feature_type(msg)


def _del_behv_feature_type_json(params):
    _del_behv_feature_type_proto(Parse(json.dumps(params), DelBehvFeatureTypeMessage()))


# -------------------------------------------------------------------------
# 主表格


cmd_to_handler_json = {
    # test
    "request_test": (_request_test_json, TIME_DURATION_LEVEL_1),

    "analyze_sample_list": (_analyze_sample_list_json, TIME_DURATION_LEVEL_1),

    "add_host_os": (_add_host_os_json, TIME_DURATION_LEVEL_1),
    "clone_host_os": (_clone_host_os_json, TIME_DURATION_LEVEL_1),
    "del_host_os": (_del_host_os_json, TIME_DURATION_LEVEL_1),

    "add_comm_target": (_add_comm_target_json, TIME_DURATION_LEVEL_1),
    "add_comm_target_to_sample": (_add_comm_target_to_sample_json, TIME_DURATION_LEVEL_1),
    "connect_comm_target": (_connect_comm_target_json, TIME_DURATION_LEVEL_1),
    "disconnect_comm_target": (_disconnect_comm_target_json, TIME_DURATION_LEVEL_1),

    "add_attack_target": (_add_attack_target_json, TIME_DURATION_LEVEL_1),
    "add_attack_target_to_sample": (_add_attack_target_to_sample_json, TIME_DURATION_LEVEL_1),
    "connect_attack_target": (_connect_attack_target_json, TIME_DURATION_LEVEL_1),
    "disconnect_attack_target": (_disconnect_attack_target_json, TIME_DURATION_LEVEL_1),

    "sample_relationship": (_sample_relationship_json, TIME_DURATION_LEVEL_1),

    #

    "append_file_behv": (_append_file_behv_json, TIME_DURATION_LEVEL_1),
    "replace_file_behv": (_replace_file_behv_json, TIME_DURATION_LEVEL_1),
    "clear_file_behv": (_clear_file_behv_json, TIME_DURATION_LEVEL_1),

    "append_reg_behv": (_append_reg_behv_json, TIME_DURATION_LEVEL_1),
    "replace_reg_behv": (_replace_reg_behv_json, TIME_DURATION_LEVEL_1),
    "clear_reg_behv": (_clear_reg_behv_json, TIME_DURATION_LEVEL_1),

    "append_network_behv": (_append_network_behv_json, TIME_DURATION_LEVEL_1),

    "append_proc_behv": (_append_proc_behv_json, TIME_DURATION_LEVEL_1),
    "replace_proc_behv": (_replace_proc_behv_json, TIME_DURATION_LEVEL_1),
    "clear_proc_behv": (_clear_proc_behv_json, TIME_DURATION_LEVEL_1),

    "append_sys_behv": (_append_sys_behv_json, TIME_DURATION_LEVEL_1),
    "replace_sys_behv": (_replace_sys_behv_json, TIME_DURATION_LEVEL_1),
    "clear_sys_behv": (_clear_sys_behv_json, TIME_DURATION_LEVEL_1),

    "append_window_behv": (_append_window_behv_json, TIME_DURATION_LEVEL_1),
    "replace_window_behv": (_replace_window_behv_json, TIME_DURATION_LEVEL_1),
    "clear_window_behv": (_clear_window_behv_json, TIME_DURATION_LEVEL_1),

    "append_service_behv": (_append_service_behv_json, TIME_DURATION_LEVEL_1),
    "replace_service_behv": (_replace_service_behv_json, TIME_DURATION_LEVEL_1),
    "clear_service_behv": (_clear_service_behv_json, TIME_DURATION_LEVEL_1),

    "append_mutex_behv": (_append_mutex_behv_json, TIME_DURATION_LEVEL_1),
    "replace_mutex_behv": (_replace_mutex_behv_json, TIME_DURATION_LEVEL_1),
    "clear_mutex_behv": (_clear_mutex_behv_json, TIME_DURATION_LEVEL_1),

    "append_whatever_behv": (_append_whatever_behv_json, TIME_DURATION_LEVEL_1),
    "replace_whatever_behv": (_replace_whatever_behv_json, TIME_DURATION_LEVEL_1),
    "del_whatever_behv": (_del_whatever_behv_json, TIME_DURATION_LEVEL_1),
    "clear_whatever_behv": (_clear_whatever_behv_json, TIME_DURATION_LEVEL_1),

    "append_behv_feature": (_append_behv_feature_json, TIME_DURATION_LEVEL_1),
    "replace_behv_feature": (_replace_behv_feature_json, TIME_DURATION_LEVEL_1),
    "clear_behv_feature": (_clear_behv_feature_json, TIME_DURATION_LEVEL_1),

    #

    "update_vt_info": (_update_vt_info_json, TIME_DURATION_LEVEL_1),
    "update_hybrid_info": (_update_hybrid_info_json, TIME_DURATION_LEVEL_1),
    "update_reverseit_info": (_update_reverseit_info_json, TIME_DURATION_LEVEL_1),
    "update_malwr_info": (_update_malwr_info_json, TIME_DURATION_LEVEL_1),

    #
    #

    # 中英对照

    "add_file_type": (_add_file_type_json, TIME_DURATION_LEVEL_1),
    "del_file_type": (_del_file_type_json, TIME_DURATION_LEVEL_1),
    "add_platform": (_add_platform_json, TIME_DURATION_LEVEL_1),
    "del_platform": (_del_platform_json, TIME_DURATION_LEVEL_1),
    "add_sample_relationship_type": (_add_sample_relationship_type_json, TIME_DURATION_LEVEL_1),
    "del_sample_relationship_type": (_del_sample_relationship_type_json, TIME_DURATION_LEVEL_1),
    "add_overall_malicious_type": (_add_overall_malicious_type_json, TIME_DURATION_LEVEL_1),
    "del_overall_malicious_type": (_del_overall_malicious_type_json, TIME_DURATION_LEVEL_1),
    "add_malware_family": (_add_malware_family_json, TIME_DURATION_LEVEL_1),
    "del_malware_family": (_del_malware_family_json, TIME_DURATION_LEVEL_1),
    "add_programing_lang": (_add_programing_lang_json, TIME_DURATION_LEVEL_1),
    "del_programing_lang": (_del_programing_lang_json, TIME_DURATION_LEVEL_1),
    "add_function_type": (_add_function_type_json, TIME_DURATION_LEVEL_1),
    "del_function_type": (_del_function_type_json, TIME_DURATION_LEVEL_1),
    "add_proc_behv_type": (_add_proc_behv_type_json, TIME_DURATION_LEVEL_1),
    "del_proc_behv_type": (_del_proc_behv_type_json, TIME_DURATION_LEVEL_1),
    "add_sys_behv_type": (_add_sys_behv_type_json, TIME_DURATION_LEVEL_1),
    "del_sys_behv_type": (_del_sys_behv_type_json, TIME_DURATION_LEVEL_1),
    "add_behv_feature_type": (_add_behv_feature_type_json, TIME_DURATION_LEVEL_1),
    "del_behv_feature_type": (_del_behv_feature_type_json, TIME_DURATION_LEVEL_1),

    #
}


cmd_to_handler_proto = {
    # test
    "request_test": (_request_test_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_request_test),

    "analyze_sample_list": (_analyze_sample_list_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_analyze_sample_list),

    "add_host_os": (_add_host_os_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_host_os),
    "clone_host_os": (_clone_host_os_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clone_host_os),
    "del_host_os": (_del_host_os_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_host_os),

    "add_comm_target": (_add_comm_target_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_comm_target),
    "add_comm_target_to_sample": (_add_comm_target_to_sample_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_comm_target_to_sample),
    "connect_comm_target": (_connect_comm_target_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_connect_comm_target),
    "disconnect_comm_target": (_disconnect_comm_target_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_disconnect_comm_target),

    "add_attack_target": (_add_attack_target_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_attack_target),
    "add_attack_target_to_sample": (_add_attack_target_to_sample_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_attack_target_to_sample),
    "connect_attack_target": (_connect_attack_target_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_connect_attack_target),
    "disconnect_attack_target": (_disconnect_attack_target_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_disconnect_attack_target),

    "sample_relationship": (_sample_relationship_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_sample_relationship),

    #

    "append_file_behv": (_append_file_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_file_behv),
    "replace_file_behv": (_replace_file_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_replace_file_behv),
    "clear_file_behv": (_clear_file_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clear_file_behv),

    "append_reg_behv": (_append_reg_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_reg_behv),
    "replace_reg_behv": (_replace_reg_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_replace_reg_behv),
    "clear_reg_behv": (_clear_reg_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clear_reg_behv),

    "append_network_behv": (_append_network_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_network_behv),

    "append_proc_behv": (_append_proc_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_proc_behv),
    "replace_proc_behv": (_replace_proc_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_replace_proc_behv),
    "clear_proc_behv": (_clear_proc_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clear_proc_behv),

    "append_sys_behv": (_append_sys_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_sys_behv),
    "replace_sys_behv": (_replace_sys_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_replace_sys_behv),
    "clear_sys_behv": (_clear_sys_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clear_sys_behv),

    "append_window_behv": (_append_window_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_window_behv),
    "replace_window_behv": (_replace_window_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_replace_window_behv),
    "clear_window_behv": (_clear_window_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clear_window_behv),

    "append_service_behv": (_append_service_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_service_behv),
    "replace_service_behv": (_replace_service_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_replace_service_behv),
    "clear_service_behv": (_clear_service_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clear_service_behv),

    "append_mutex_behv": (_append_mutex_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_mutex_behv),
    "replace_mutex_behv": (_replace_mutex_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_replace_mutex_behv),
    "clear_mutex_behv": (_clear_mutex_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clear_mutex_behv),

    "append_whatever_behv": (_append_whatever_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_whatever_behv),
    "replace_whatever_behv": (_replace_whatever_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_replace_whatever_behv),
    "del_whatever_behv": (_del_whatever_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_whatever_behv),
    "clear_whatever_behv": (_clear_whatever_behv_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clear_whatever_behv),

    "append_behv_feature": (_append_behv_feature_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_append_behv_feature),
    "replace_behv_feature": (_replace_behv_feature_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_replace_behv_feature),
    "clear_behv_feature": (_clear_behv_feature_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_clear_behv_feature),

    "update_vt_info": (_update_vt_info_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_update_vt_info),
    "update_hybrid_info": (_update_hybrid_info_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_update_hybrid_info),
    "update_reverseit_info": (_update_reverseit_info_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_update_reverseit_info),
    "update_malwr_info": (_update_malwr_info_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_update_malwr_info),

    # 中英对照

    "add_file_type": (_add_file_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_file_type),
    "del_file_type": (_del_file_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_file_type),
    "add_platform": (_add_platform_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_platform),
    "del_platform": (_del_platform_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_platform),
    "add_sample_relationship_type": (_add_sample_relationship_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_sample_relationship_type),
    "del_sample_relationship_type": (_del_sample_relationship_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_sample_relationship_type),
    "add_overall_malicious_type": (_add_overall_malicious_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_overall_malicious_type),
    "del_overall_malicious_type": (_del_overall_malicious_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_overall_malicious_type),
    "add_malware_family": (_add_malware_family_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_malware_family),
    "del_malware_family": (_del_malware_family_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_malware_family),
    "add_programing_lang": (_add_programing_lang_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_programing_lang),
    "del_programing_lang": (_del_programing_lang_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_programing_lang),
    "add_function_type": (_add_function_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_function_type),
    "del_function_type": (_del_function_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_function_type),
    "add_proc_behv_type": (_add_proc_behv_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_proc_behv_type),
    "del_proc_behv_type": (_del_proc_behv_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_proc_behv_type),
    "add_sys_behv_type": (_add_sys_behv_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_sys_behv_type),
    "del_sys_behv_type": (_del_sys_behv_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_sys_behv_type),
    "add_behv_feature_type": (_add_behv_feature_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_add_behv_feature_type),
    "del_behv_feature_type": (_del_behv_feature_type_proto, TIME_DURATION_LEVEL_1, lambda msg: msg.msg_del_behv_feature_type),

    #
}


# -------------------------------------------------------------------------
# END OF FILE -------------------------------------------------------------
# -------------------------------------------------------------------------
