# -*- coding: utf-8 -*-


# -------------------------------------------------------------------------


# from google.protobuf.json_format import Parse
from google.protobuf.json_format import MessageToJson
from proto_def.malwrdb_proto_pb2 import *
# import json


# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)


# -------------------------------------------------------------------------

"""

咱自己组合消息:

    这是错的:
    sub_msg = SubMessage()
    sub_msg.xxx = xxx
    base_msg.msg_detail = sub_msg

    这是对的:
    sub_msg = base_msg.msg_detail
    sub_msg.xxx = xxx

解析别人的信息:

    x

"""

# -------------------------------------------------------------------------
# 具体消息 - 请求


# 与样本无关


v_tmp_sample_id = "59b77f12a9ddb5057c1288be"
v_tmp_comm_target_id = "59b9e5eaa9ddb515249037e5"
v_tmp_behv_os_id = "59b7667aa9ddb533787bc557"
v_tmp_attack_target_id = "xx"


# 测试

msg_request_test = RequestMessageWrapper()
msg_request_test.msg_type = "request_test"
msg_detail = msg_request_test.msg_request_test
msg_detail.test = "hello"


# 主机


# 追加主机
msg_add_host_os = RequestMessageWrapper()
msg_add_host_os.msg_type = "add_host_os"
msg_detail = msg_add_host_os.msg_add_host_os
msg_detail.platform = "windows"
msg_detail.version = "xp"
msg_detail.arch = "x86"
msg_detail.desc = "xpsp1x86"
msg_detail.sp = 1
msg_detail.author = "admin"

# 克隆主机
msg_clone_host_os = RequestMessageWrapper()
msg_clone_host_os.msg_type = "del_host_os"
msg_detail = msg_clone_host_os.msg_clone_host_os
msg_detail.src_host_os_id = "xxx"
msg_detail.new_desc = "new_desc"

# 删除主机
msg_del_host_os = RequestMessageWrapper()
msg_del_host_os.msg_type = "del_host_os"
msg_detail = msg_del_host_os.msg_del_host_os
msg_detail.host_os_id = "xxx"


# 通信地址


# 追加
msg_add_comm_target = RequestMessageWrapper()
msg_add_comm_target.msg_type = "add_comm_target"
msg_detail = msg_add_comm_target.msg_add_comm_target
msg_detail.domain = "www.baidu.com"
msg_detail.port = 1234

# 追加到样本
msg_add_comm_target_to_sample = RequestMessageWrapper()
msg_add_comm_target_to_sample.msg_type = "add_comm_target_to_sample"
msg_detail = msg_add_comm_target_to_sample.msg_add_comm_target_to_sample
msg_detail.sample_id = v_tmp_sample_id
msg_detail.comm_target.ip_addr = "1.1.1.1"
msg_detail.comm_target.port = 2345

# 连接
msg_connect_comm_target = RequestMessageWrapper()
msg_connect_comm_target.msg_type = "connect_comm_target"
msg_detail = msg_connect_comm_target.msg_connect_comm_target
msg_detail.sample_id = v_tmp_sample_id
msg_detail.comm_target_id = v_tmp_comm_target_id

# 断开连接
msg_disconnect_comm_target = RequestMessageWrapper()
msg_disconnect_comm_target.msg_type = "disconnect_comm_target"
msg_detail = msg_disconnect_comm_target.msg_disconnect_comm_target
msg_detail.sample_id = v_tmp_sample_id
msg_detail.comm_target_id = v_tmp_comm_target_id


# 攻击目标


# 追加
msg_add_attack_target = RequestMessageWrapper()
msg_add_attack_target.msg_type = "add_attack_target"
msg_detail = msg_add_attack_target.msg_add_attack_target
msg_detail.continent_list.append("欧洲")
msg_detail.country_list.append("英国")
msg_detail.industry_list.append("银行")

# 追加到样本
msg_add_attack_target_to_sample = RequestMessageWrapper()
msg_add_attack_target_to_sample.msg_type = "add_attack_target_to_sample"
msg_detail = msg_add_attack_target_to_sample.msg_add_attack_target_to_sample
msg_detail.sample_id = v_tmp_sample_id
msg_detail.attack_target.continent_list.append("欧洲")
msg_detail.attack_target.country_list.append("英国")
msg_detail.attack_target.industry_list.append("银行")

# 连接
msg_connect_attack_target = RequestMessageWrapper()
msg_connect_attack_target.msg_type = "connect_attack_target"
msg_detail = msg_connect_attack_target.msg_connect_attack_target
msg_detail.sample_id = v_tmp_sample_id
msg_detail.attack_target_id = v_tmp_attack_target_id

# 断开连接
msg_disconnect_attack_target = RequestMessageWrapper()
msg_disconnect_attack_target.msg_type = "connect_attack_target"
msg_detail = msg_disconnect_attack_target.msg_disconnect_attack_target
msg_detail.sample_id = v_tmp_sample_id
msg_detail.attack_target_id = v_tmp_attack_target_id


# -------------------------------------------------------------------------
# 分析


msg_analyze_sample_list = RequestMessageWrapper()
msg_analyze_sample_list.msg_type = "analyze_sample_list"
msg_detail = msg_analyze_sample_list.msg_analyze_sample_list
msg_detail.sample_id_list.append(v_tmp_sample_id)
# msg_detail.sample_id_list.append("2")
# msg_detail.sample_id_list.append("3")


# -------------------------------------------------------------------------
# 样本相关


msg_sample_relationship = RequestMessageWrapper()
msg_sample_relationship.msg_type = "sample_relationship"
msg_detail = msg_sample_relationship.msg_sample_relationship
msg_detail.parent_sample_id = "59b77f12a9ddb5057c1288be"
msg_detail.child_sample_id_list.append(v_tmp_sample_id)
msg_detail.relationship_type = "normal"


# -------------------------------------------------------------------------
# 行为


# 文件行为

msg_file_behv = FileBehvMessage()
msg_file_behv.file_path = r"C:\path"

# 追加
msg_append_file_behv = RequestMessageWrapper()
msg_append_file_behv.msg_type = "append_file_behv"
msg_detail = msg_append_file_behv.msg_append_file_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.file_behv_list.extend([msg_file_behv, msg_file_behv])

# 替换
msg_replace_file_behv = RequestMessageWrapper()
msg_replace_file_behv.msg_type = "replace_file_behv"
msg_detail = msg_replace_file_behv.msg_replace_file_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.file_behv_list.extend([msg_file_behv, msg_file_behv])

# 清空
msg_clear_file_behv = RequestMessageWrapper()
msg_clear_file_behv.msg_type = "clear_file_behv"
msg_detail = msg_clear_file_behv.msg_clear_file_behv
msg_detail.sample_id = v_tmp_sample_id


# 注册表行为

msg_reg_behv = RegBehvMessage()
msg_reg_behv.reg_path = r"HKLM\Software"

# 追加
msg_append_reg_behv = RequestMessageWrapper()
msg_append_reg_behv.msg_type = "append_reg_behv"
msg_detail = msg_append_reg_behv.msg_append_reg_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.reg_behv_list.extend([msg_reg_behv, msg_reg_behv])

# 替换
msg_replace_reg_behv = RequestMessageWrapper()
msg_replace_reg_behv.msg_type = "replace_reg_behv"
msg_detail = msg_replace_reg_behv.msg_replace_reg_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.reg_behv_list.extend([msg_reg_behv, msg_reg_behv])

# 清空
msg_clear_reg_behv = RequestMessageWrapper()
msg_clear_reg_behv.msg_type = "clear_reg_behv"
msg_detail = msg_clear_reg_behv.msg_clear_reg_behv
msg_detail.sample_id = v_tmp_sample_id


# 网络行为


# 追加
msg_append_network_behv = RequestMessageWrapper()
msg_append_network_behv.msg_type = "append_network_behv"
msg_detail = msg_append_network_behv.msg_append_network_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.comm_target_id = v_tmp_comm_target_id
msg_detail.protocol = "http"
msg_detail.related_pcap_sample_id_list.append("xxx")


# 进程行为

msg_proc_behv = ProcBehvMessage()
msg_proc_behv.behv_type = "create"
msg_proc_behv.proc_path = r"c:\windows\system32\calc.exe"

# 追加
msg_append_proc_behv = RequestMessageWrapper()
msg_append_proc_behv.msg_type = "append_proc_behv"
msg_detail = msg_append_proc_behv.msg_append_proc_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.proc_behv_list.extend([msg_proc_behv, msg_proc_behv])

# 替换
msg_replace_proc_behv = RequestMessageWrapper()
msg_replace_proc_behv.msg_type = "replace_proc_behv"
msg_detail = msg_replace_proc_behv.msg_replace_proc_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.proc_behv_list.extend([msg_proc_behv, msg_proc_behv])

# 清空
msg_clear_proc_behv = RequestMessageWrapper()
msg_clear_proc_behv.msg_type = "clear_proc_behv"
msg_detail = msg_clear_proc_behv.msg_clear_proc_behv
msg_detail.sample_id = v_tmp_sample_id


# 系统行为

msg_sys_behv = SysBehvMessage()
msg_sys_behv.behv_type = r"check system version"

# 追加
msg_append_sys_behv = RequestMessageWrapper()
msg_append_sys_behv.msg_type = "append_sys_behv"
msg_detail = msg_append_sys_behv.msg_append_sys_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.sys_behv_list.extend([msg_sys_behv, msg_sys_behv])


# 替换
msg_replace_sys_behv = RequestMessageWrapper()
msg_replace_sys_behv.msg_type = "replace_sys_behv"
msg_detail = msg_replace_sys_behv.msg_replace_sys_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.sys_behv_list.extend([msg_sys_behv, msg_sys_behv])

# 清空
msg_clear_sys_behv = RequestMessageWrapper()
msg_clear_sys_behv.msg_type = "clear_sys_behv"
msg_detail = msg_clear_sys_behv.msg_clear_sys_behv
msg_detail.sample_id = v_tmp_sample_id


# 窗口行为

msg_window_behv = WindowBehvMessage()
msg_window_behv.behv_type_list.append("create")
msg_window_behv.window_class_name = "x"
msg_window_behv.window_title_name = "x"
msg_window_behv.window_content = "x"

# 追加
msg_append_window_behv = RequestMessageWrapper()
msg_append_window_behv.msg_type = "append_window_behv"
msg_detail = msg_append_window_behv.msg_append_window_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.window_behv_list.extend([msg_window_behv, msg_window_behv])

# 替换
msg_replace_window_behv = RequestMessageWrapper()
msg_replace_window_behv.msg_type = "replace_window_behv"
msg_detail = msg_replace_window_behv.msg_replace_window_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.window_behv_list.extend([msg_window_behv, msg_window_behv])

# 清空
msg_clear_window_behv = RequestMessageWrapper()
msg_clear_window_behv.msg_type = "clear_window_behv"
msg_detail = msg_clear_window_behv.msg_clear_window_behv
msg_detail.sample_id = v_tmp_sample_id


# 服务行为

msg_service_behv = ServiceBehvMessage()
msg_service_behv.behv_type_list.append("create")
msg_service_behv.service_name = "x"
msg_service_behv.service_display_name = "x"
msg_service_behv.service_binary_path = r"c:\path.exe"
msg_service_behv.service_start_type = 1

# 追加
msg_append_service_behv = RequestMessageWrapper()
msg_append_service_behv.msg_type = "append_service_behv"
msg_detail = msg_append_service_behv.msg_append_service_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.service_behv_list.extend([msg_service_behv, msg_service_behv])

# 替换
msg_replace_service_behv = RequestMessageWrapper()
msg_replace_service_behv.msg_type = "replace_service_behv"
msg_detail = msg_replace_service_behv.msg_replace_service_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.service_behv_list.extend([msg_service_behv, msg_service_behv])

# 清空
msg_clear_service_behv = RequestMessageWrapper()
msg_clear_service_behv.msg_type = "msg_clear_service_behv"
msg_detail = msg_clear_service_behv.msg_clear_service_behv
msg_detail.sample_id = v_tmp_sample_id


# 互斥体/事件行为

msg_mutex_behv = MutexBehvMessage()
msg_mutex_behv.behv_type_list.append("create")
msg_mutex_behv.mutex_string = "hello"

# 追加
msg_append_mutex_behv = RequestMessageWrapper()
msg_append_mutex_behv.msg_type = "append_mutex_behv"
msg_detail = msg_append_mutex_behv.msg_append_mutex_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.mutex_behv_list.extend([msg_mutex_behv, msg_mutex_behv])

# 替换
msg_replace_mutex_behv = RequestMessageWrapper()
msg_replace_mutex_behv.msg_type = "replace_mutex_behv"
msg_detail = msg_replace_mutex_behv.msg_replace_mutex_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.mutex_behv_list.extend([msg_mutex_behv, msg_mutex_behv])

# 清空
msg_clear_mutex_behv = RequestMessageWrapper()
msg_clear_mutex_behv.msg_type = "clear_mutex_behv"
msg_detail = msg_clear_mutex_behv.msg_clear_mutex_behv
msg_detail.sample_id = v_tmp_sample_id


# 随便什么行为

msg_whatever_behv = WhateverBehvMessage()
msg_whatever_behv.behv_desc = "xxxxxxxxx"

# 追加
msg_append_whatever_behv = RequestMessageWrapper()
msg_append_whatever_behv.msg_type = "append_whatever_behv"
msg_detail = msg_append_whatever_behv.msg_append_whatever_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.whatever_behv_list.extend([msg_whatever_behv])

# 替换
msg_replace_whatever_behv = RequestMessageWrapper()
msg_replace_whatever_behv.msg_type = "replace_whatever_behv"
msg_detail = msg_replace_whatever_behv.msg_replace_whatever_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.whatever_behv_list.extend([msg_whatever_behv])

# 删除
msg_del_whatever_behv = RequestMessageWrapper()
msg_del_whatever_behv.msg_type = "del_whatever_behv"
msg_detail = msg_del_whatever_behv.msg_del_whatever_behv
msg_detail.sample_id = v_tmp_sample_id
msg_detail.whatever_behv_id = "xxx"

# 清空
msg_clear_whatever_behv = RequestMessageWrapper()
msg_clear_whatever_behv.msg_type = "clear_whatever_behv"
msg_detail = msg_clear_whatever_behv.msg_clear_whatever_behv
msg_detail.sample_id = v_tmp_sample_id


# 组合行为

msg_behv_feature = BehvFeatureMessage()
msg_behv_feature.behv_feature = "anti-virus"

# 追加
msg_append_behv_feature = RequestMessageWrapper()
msg_append_behv_feature.msg_type = "append_behv_feature"
msg_detail = msg_append_behv_feature.msg_append_behv_feature
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.behv_feature_list.extend([msg_behv_feature, msg_behv_feature])

# 替换
msg_replace_behv_feature = RequestMessageWrapper()
msg_replace_behv_feature.msg_type = "replace_behv_feature"
msg_detail = msg_replace_behv_feature.msg_replace_behv_feature
msg_detail.sample_id = v_tmp_sample_id
msg_detail.behv_os_id_list.append(v_tmp_behv_os_id)
msg_detail.behv_feature_list.extend([msg_behv_feature, msg_behv_feature])

# 清空
msg_clear_behv_feature = RequestMessageWrapper()
msg_clear_behv_feature.msg_type = "clear_behv_feature"
msg_detail = msg_clear_behv_feature.msg_clear_behv_feature
msg_detail.sample_id = v_tmp_sample_id


# -------------------------------------------------------------------------
# 网络信息


# vt
msg_update_vt_info = RequestMessageWrapper()
msg_update_vt_info.msg_type = "update_vt_info"
msg_detail = msg_update_vt_info.msg_update_vt_info
msg_detail.sample_id_list.append(v_tmp_sample_id)

# hybrid
msg_update_hybrid_info = RequestMessageWrapper()
msg_update_hybrid_info.msg_type = "update_hybrid_info"
msg_detail = msg_update_hybrid_info.msg_update_hybrid_info
msg_detail.sample_id_list.append(v_tmp_sample_id)

# reverseit
msg_update_reverseit_info = RequestMessageWrapper()
msg_update_reverseit_info.msg_type = "update_reverseit_info"
msg_detail = msg_update_reverseit_info.msg_update_reverseit_info
msg_detail.sample_id_list.append(v_tmp_sample_id)

# malwr
msg_update_malwr_info = RequestMessageWrapper()
msg_update_malwr_info.msg_type = "update_malwr_info"
msg_detail = msg_update_malwr_info.msg_update_malwr_info
msg_detail.sample_id_list.append(v_tmp_sample_id)


# -------------------------------------------------------------------------
# 网络样本收集


# -------------------------------------------------------------------------
# 网络yara规则收集


# -------------------------------------------------------------------------
# 中英对照


# 文件类型

msg_file_type = FileTypeMessage()
msg_file_type.name = "word"
msg_file_type.desc = "Office Word 文档"

msg_add_file_type = RequestMessageWrapper()
msg_add_file_type.msg_type = "add_file_type"
msg_detail = msg_add_file_type.msg_add_file_type
msg_detail.file_type_list.extend([msg_file_type])

msg_del_file_type = RequestMessageWrapper()
msg_del_file_type.msg_type = "del_file_type"
msg_detail = msg_del_file_type.msg_del_file_type
msg_detail.file_type_id = "59bb5506a9ddb5296ccb7103"

# 平台

msg_platform = PlatformMessage()
msg_platform.name = "Ubuntu"
msg_platform.desc = "Ubuntu"

msg_add_platform = RequestMessageWrapper()
msg_add_platform.msg_type = "add_platform"
msg_detail = msg_add_platform.msg_add_platform
msg_detail.platform_list.extend([msg_platform])

msg_del_platform = RequestMessageWrapper()
msg_del_platform.msg_type = "del_platform"
msg_detail = msg_del_platform.msg_del_platform
msg_detail.platform_id = "xx"

# 样本关系

msg_sample_relationship_type = SampleRelationshipTypeMessage()
msg_sample_relationship_type.name = "unpack"
msg_sample_relationship_type.desc = "脱壳"

msg_add_sample_relationship_type = RequestMessageWrapper()
msg_add_sample_relationship_type.msg_type = "add_sample_relationship_type"
msg_detail = msg_add_sample_relationship_type.msg_add_sample_relationship_type
msg_detail.sample_relationship_list.extend([msg_sample_relationship_type])

msg_del_sample_relationship_type = RequestMessageWrapper()
msg_del_sample_relationship_type.msg_type = "del_sample_relationship_type"
msg_detail = msg_del_sample_relationship_type.msg_del_sample_relationship_type
msg_detail.sample_realtionship_type_id = "xx"

# 总体的恶意类型

msg_overall_malicious_type = OverallMaliciousTypeMessage()
msg_overall_malicious_type.name = "ransomware"
msg_overall_malicious_type.desc = "勒索软件"

msg_add_overall_malicious_type = RequestMessageWrapper()
msg_add_overall_malicious_type.msg_type = "add_overall_malicious_type"
msg_detail = msg_add_overall_malicious_type.msg_add_overall_malicious_type
msg_detail.malicious_type_list.extend([msg_overall_malicious_type])

msg_del_overall_malicious_type = RequestMessageWrapper()
msg_del_overall_malicious_type.msg_type = "del_overall_malicious_type"
msg_detail = msg_del_overall_malicious_type.msg_del_overall_malicious_type
msg_detail.overall_malicious_type_id = "xx"

# 恶意代码家族

msg_malware_family = MalwareFamilyMessage()
msg_malware_family.name = "WannaCry"
msg_malware_family.desc = "想哭"

msg_add_malware_family = RequestMessageWrapper()
msg_add_malware_family.msg_type = "add_malware_family"
msg_detail = msg_add_malware_family.msg_add_malware_family
msg_detail.malware_family_list.extend([msg_malware_family])

msg_del_malware_family = RequestMessageWrapper()
msg_del_malware_family.msg_type = "del_malware_family"
msg_detail = msg_del_malware_family.msg_del_malware_family
msg_detail.malware_family_id = "xx"

# 编程语言

msg_programing_lang = ProgramingLangMessage()
msg_programing_lang.name = "C#"
msg_programing_lang.desc = "C#"

msg_add_programing_lang = RequestMessageWrapper()
msg_add_programing_lang.msg_type = "add_programing_lang"
msg_detail = msg_add_programing_lang.msg_add_programing_lang
msg_detail.programing_lang_list.extend([msg_programing_lang])

msg_del_programing_lang = RequestMessageWrapper()
msg_del_programing_lang.msg_type = "del_programing_lang"
msg_detail = msg_del_programing_lang.msg_del_programing_lang
msg_detail.programing_lang_id = "xx"

# 函数类型

msg_function_type = FunctionTypeMessage()
msg_function_type.name = "library"
msg_function_type.desc = "库函数"

msg_add_function_type = RequestMessageWrapper()
msg_add_function_type.msg_type = "add_function_type"
msg_detail = msg_add_function_type.msg_add_function_type
msg_detail.func_type_list.extend([msg_function_type])

msg_del_function_type = RequestMessageWrapper()
msg_del_function_type.msg_type = "del_function_type"
msg_detail = msg_del_function_type.msg_del_function_type
msg_detail.function_type_id = "xx"

# 进程行为类型

msg_proc_behv_type = ProcBehvTypeMessage()
msg_proc_behv_type.name = "create"
msg_proc_behv_type.desc = "创建"

msg_add_proc_behv_type = RequestMessageWrapper()
msg_add_proc_behv_type.msg_type = "add_proc_behv_type"
msg_detail = msg_add_proc_behv_type.msg_add_proc_behv_type
msg_detail.proc_behv_type_list.extend([msg_proc_behv_type])

msg_del_proc_behv_type = RequestMessageWrapper()
msg_del_proc_behv_type.msg_type = "del_proc_behv_type"
msg_detail = msg_del_proc_behv_type.msg_del_proc_behv_type
msg_detail.proc_behv_type_id = "xx"

# 系统行为类型

msg_sys_behv_type = SysBehvTypeMessage()
msg_sys_behv_type.name = "query_sys_info"
msg_sys_behv_type.desc = "查询系统信息"

msg_add_sys_behv_type = RequestMessageWrapper()
msg_add_sys_behv_type.msg_type = "add_sys_behv_type"
msg_detail = msg_add_sys_behv_type.msg_add_sys_behv_type
msg_detail.sys_behv_type_list.extend([msg_sys_behv_type])

msg_del_sys_behv_type = RequestMessageWrapper()
msg_del_sys_behv_type.msg_type = "del_sys_behv_type"
msg_detail = msg_del_sys_behv_type.msg_del_sys_behv_type
msg_detail.sys_behv_type_id = "xx"

# 组合行为

msg_behv_feature_type = BehvFeatureTypeMessage()
msg_behv_feature_type.name = "anti-vm"
msg_behv_feature_type.desc = "反虚拟机"

msg_add_behv_feature_type = RequestMessageWrapper()
msg_add_behv_feature_type.msg_type = "add_behv_feature_type"
msg_detail = msg_add_behv_feature_type.msg_add_behv_feature_type
msg_detail.behv_feature_type_list.extend([msg_behv_feature_type])

msg_del_behv_feature_type = RequestMessageWrapper()
msg_del_behv_feature_type.msg_type = "del_behv_feature_type"
msg_detail = msg_del_behv_feature_type.msg_del_behv_feature_type
msg_detail.behv_feature_type_id = "xx"


# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# 具体消息 - 回复

# 测试

msg_response_test = ResponseMessageWrapper()
msg_response_test.msg_type = "response_test"
msg_detail = msg_response_test.msg_response_test
msg_detail.test = "world"


#


# -------------------------------------------------------------------------


v_tmp_msg_request_all = [
    msg_request_test,
    msg_analyze_sample_list,
    msg_add_host_os,
    msg_clone_host_os,
    msg_del_host_os,
    msg_add_comm_target,
    msg_add_comm_target_to_sample,
    msg_connect_comm_target,
    msg_disconnect_comm_target,
    msg_add_attack_target,
    msg_add_attack_target_to_sample,
    msg_connect_attack_target,
    msg_disconnect_attack_target,
    msg_sample_relationship,
    msg_append_file_behv,
    msg_replace_file_behv,
    msg_clear_file_behv,
    msg_append_reg_behv,
    msg_replace_reg_behv,
    msg_clear_reg_behv,
    msg_append_network_behv,
    msg_append_proc_behv,
    msg_replace_proc_behv,
    msg_clear_proc_behv,
    msg_append_sys_behv,
    msg_replace_sys_behv,
    msg_clear_sys_behv,
    msg_append_window_behv,
    msg_replace_window_behv,
    msg_clear_window_behv,
    msg_append_service_behv,
    msg_replace_service_behv,
    msg_clear_service_behv,
    msg_append_mutex_behv,
    msg_replace_mutex_behv,
    msg_clear_mutex_behv,
    msg_append_whatever_behv,
    msg_replace_whatever_behv,
    msg_del_whatever_behv,
    msg_clear_whatever_behv,
    msg_append_behv_feature,
    msg_replace_behv_feature,
    msg_clear_behv_feature,
    msg_update_vt_info,
    msg_update_hybrid_info,
    msg_update_reverseit_info,
    msg_update_malwr_info,
    #
    #
    msg_add_file_type,
    msg_del_file_type,
    msg_add_platform,
    msg_del_platform,
    msg_add_sample_relationship_type,
    msg_del_sample_relationship_type,
    msg_add_overall_malicious_type,
    msg_del_overall_malicious_type,
    msg_add_malware_family,
    msg_del_malware_family,
    msg_add_programing_lang,
    msg_del_programing_lang,
    msg_add_function_type,
    msg_del_function_type,
    msg_add_proc_behv_type,
    msg_del_proc_behv_type,
    msg_add_sys_behv_type,
    msg_del_sys_behv_type,
    msg_add_behv_feature_type,
    msg_del_behv_feature_type,
]


v_tmp_msg_reponse_all = [
    msg_response_test,
]


v_tmp_msg_all = list(v_tmp_msg_request_all + v_tmp_msg_reponse_all)


# -------------------------------------------------------------------------


def test():
    # # Parse - RequestMessageWrapper
    # dict_ = {
    #     "msg_type": "add_host_os",
    #     "msg_add_host_os": {
    #         "platform": "1"
    #     }
    # }
    # msg_wrapper = Parse(json.dumps(dict_), RequestMessageWrapper())
    # log("msg: \n%s\n" % msg_wrapper

    # # Parse - AddHostOsMessage
    # dict_ = {u'msg_add_host_os': {u'author': u'admin', u'sp': 1, u'platform': u'windows', u'version': u'xp', u'arch': u'x86', u'desc': u'xpsp1x86'}}
    # msg_add_host_os = Parse(json.dumps(dict_[dict_.keys()[0]]), AddHostOsMessage())
    # log("msg: \n%s\n" % msg_add_host_os

    # # SerializeToString()
    # str_ = msg_add_host_os.SerializeToString()
    # log("type: %s, len: %d\n" % (type(str_), len(str_))
    # # log("detail: %s" % str_  # 这个打印不出来
    # # # ParseFromString()
    # msg_wrapper = RequestMessageWrapper()
    # msg_wrapper.ParseFromString(str_)
    # log("msg: %s" % msg_wrapper

    pass


# -------------------------------------------------------------------------


def _to_json(msg):
    return MessageToJson(msg, including_default_value_fields=True, preserving_proto_field_name=True)


if __name__ == "__main__":

    # test()

    for msg in v_tmp_msg_all:
        log("msg_%s: \n%s\n" % (msg.msg_type, _to_json(msg)))

    pass


# -------------------------------------------------------------------------
# END OF FILE
# -------------------------------------------------------------------------
