# -*- coding: utf-8 -*-

"""
"""

# -------------------------------------------------------------------------

# import time

import zmq
from google.protobuf.json_format import MessageToJson

from test_proto import *
from proto_def.malwrdb_proto_pb2 import *
from malwrdb_settings import *

# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)


# -------------------------------------------------------------------------


def _to_json(msg):
    return MessageToJson(msg, including_default_value_fields=True, preserving_proto_field_name=True)


def _send_one():

    # msg_src = msg_analyze_sample_list

    # msg_src = msg_add_host_os
    # msg_src = msg_clone_host_os
    # msg_src = msg_del_host_os

    # msg_src = msg_add_comm_target
    # msg_src = msg_add_comm_target_to_sample
    # msg_src = msg_connect_comm_target
    # msg_src = msg_disconnect_comm_target

    # msg_src = msg_add_attack_target
    # msg_src = msg_add_attack_target_to_sample
    # msg_src = msg_connect_attack_target
    # msg_src = msg_disconnect_attack_target

    # msg_src = msg_sample_relationship

    msg_src = msg_append_file_behv
    # msg_src = msg_replace_file_behv
    # msg_src = msg_clear_file_behv

    # msg_src = msg_append_reg_behv
    # msg_src = msg_replace_reg_behv
    # msg_src = msg_clear_reg_behv

    # msg_src = msg_append_network_behv

    # msg_src = msg_append_proc_behv
    # msg_src = msg_replace_proc_behv
    # msg_src = msg_clear_proc_behv

    # msg_src = msg_append_sys_behv
    # msg_src = msg_replace_sys_behv
    # msg_src = msg_clear_sys_behv

    # msg_src = msg_append_window_behv
    # msg_src = msg_replace_window_behv
    # msg_src = msg_clear_window_behv

    # msg_src = msg_append_service_behv
    # msg_src = msg_replace_service_behv
    # msg_src = msg_clear_service_behv

    # msg_src = msg_append_mutex_behv
    # msg_src = msg_replace_mutex_behv
    # msg_src = msg_clear_mutex_behv

    # msg_src = msg_append_behv_feature
    # msg_src = msg_replace_behv_feature
    # msg_src = msg_clear_behv_feature

    # msg_src = msg_append_whatever_behv
    # msg_src = msg_replace_whatever_behv
    # msg_src = msg_del_whatever_behv
    # msg_src = msg_clear_whatever_behv

    # msg_src = msg_update_vt_info
    # msg_src = msg_update_hybrid_info
    # msg_src = msg_update_reverseit_info
    # msg_src = msg_update_malwr_info

    #
    #

    # msg_src = msg_add_file_type
    # msg_src = msg_del_file_type
    # msg_src = msg_add_platform
    # msg_src = msg_del_platform
    # msg_src = msg_add_sample_relationship_type
    # msg_src = msg_del_sample_relationship_type
    # msg_src = msg_add_overall_malicious_type
    # msg_src = msg_del_overall_malicious_type
    # msg_src = msg_add_malware_family
    # msg_src = msg_del_malware_family
    # msg_src = msg_add_programing_lang
    # msg_src = msg_del_programing_lang
    # msg_src = msg_add_function_type
    # msg_src = msg_del_function_type
    # msg_src = msg_add_proc_behv_type
    # msg_src = msg_del_proc_behv_type
    # msg_src = msg_add_sys_behv_type
    # msg_src = msg_del_sys_behv_type
    # msg_src = msg_add_behv_feature_type
    # msg_src = msg_del_behv_feature_type

    # -------------------------------------------------------------------------

    # 发送 json
    # msg_send = _to_json(msg_src)
    # 发送 buf
    msg_send = msg_src.SerializeToString()

    # -------------------------------------------------------------------------

    # max_cnt = 500
    max_cnt = 1
    i = 0
    while i < max_cnt:
        i = i + 1
        log("send cnt: %d\n" % i)
        socket.send(msg_send)

        msg_recv = socket.recv()
        log("recv msg: %s" % msg_recv)


def _send_all():
    i = 0
    for msg_src in v_tmp_msg_request_all:
        i = i + 1

        # 发送 json
        # msg_send = _to_json(msg_src)
        # 发送 buf
        msg_send = msg_src.SerializeToString()

        log("send cnt: %d\n" % i)
        socket.send(msg_send)

        msg_recv = socket.recv()
        log("recv msg: %s" % msg_recv)


if __name__ == "__main__":

    ctx = zmq.Context()
    socket = ctx.socket(zmq.REQ)
    socket.connect(this_host)

    # -------------------------------------------------------------------------

    _send_one()
    # _send_all()

    log("send finish...")


# -------------------------------------------------------------------------
# END OF FILE
# -------------------------------------------------------------------------
