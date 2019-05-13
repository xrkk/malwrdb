# -*- coding: utf-8 -*-

"""
"""

# -------------------------------------------------------------------------


import traceback
import zmq
from zmq.eventloop import ioloop, zmqstream
from zmq.utils import jsonapi
from malwrdb_interface import cmd_to_handler_json, cmd_to_handler_proto  # 不知为何, 这个很耗费时间. 所以, 如果把这个放到 handle_msg(), 就太慢了
from proto_def.malwrdb_proto_pb2 import *
from malwrdb_settings import *


# -------------------------------------------------------------------------
# log


from malwrdb_log import _log


def log(info, is_print=True, level="DEBUG"):
    _log(__file__, level, info, is_print=is_print)


def error(info, is_print=True):
    _log(__file__, "ERROR", info, is_print=is_print)


# -------------------------------------------------------------------------

loop = ioloop.IOLoop.instance()

ctx = zmq.Context()
s = ctx.socket(zmq.REP)
s.bind(this_host)


# -------------------------------------------------------------------------


def handle_json_msg(msg_json):
    """
        检查 msg_type, 把参数传递给对应的 handler
    """
    assert len(msg_json) == 2

    cmd = msg_json["msg_type"]
    if cmd not in cmd_to_handler_json:
        error("recv msg invalid: cmd not exist. cmd: %s. msg: %s" % (cmd, msg_json))

    else:
        handler = cmd_to_handler_json[cmd]

        log("recv cmd: %s, duration: %d" % (cmd, handler[1]))

        try:

            del msg_json["msg_type"]
            # 传递给 handler
            handler[0](msg_json[msg_json.keys()[0]])

        except:
            error("exec cmd exception. backtrace: \n")
            traceback.print_exc()

        else:
            log("exec cmd finish...")


def handle_proto_proto(msg_proto):
    """检查 msg_type, 把参数传递给对应的 handler
    """
    assert msg_proto is not None and msg_proto.msg_type is not None and len(msg_proto.msg_type) != 0

    cmd = msg_proto.msg_type
    if cmd not in cmd_to_handler_proto:
        error("recv msg invalid: cmd not exist. cmd: %s. msg: %s" % (cmd, msg_proto))

    else:
        handler = cmd_to_handler_proto[cmd]

        log("recv cmd: %s, duration: %d" % (cmd, handler[1]))

        try:
            # 传递给 handler
            handler[0](handler[2](msg_proto))

        except:
            error("exec cmd exception. backtrace: \n")
            traceback.print_exc()

        else:
            log("exec cmd finish...")


# -------------------------------------------------------------------------


if __name__ == "__main__":

    recv_cnt = 0

    # TODO: 把这个转到 settings.py
    is_direct_recv = True
    is_recv_json = False

    if is_direct_recv:

        log("start recv...")

        while True:

            # 计数
            recv_cnt = recv_cnt + 1

            # 接收
            msg_raw = s.recv()

            # 处理

            log("raw recv cnt: %d\n" % recv_cnt)
            log("raw recv msg: %s\n" % msg_raw)

            if is_recv_json:
                handle_json_msg(jsonapi.loads(msg_raw))

            else:
                msg_proto = RequestMessageWrapper()
                msg_proto.ParseFromString(msg_raw)
                assert msg_proto is not None
                handle_proto_proto(msg_proto)

            # 回复
            msg_resposne = ResponseMessageWrapper()
            msg_resposne.msg_type = "resposne"
            msg_resposne.msg_response_test.test = u"Done!"
            s.send(msg_resposne.SerializeToString())

            log("continue recv...")

    else:

        # 然而, 这玩意儿并不可靠, 或者说这种使用方式并不对!!!

        stream = zmqstream.ZMQStream(s, loop)

        def echo(msg_raw):

            global recv_cnt
            recv_cnt = recv_cnt + 1

            log("raw recv cnt: %d\n" % recv_cnt)
            log("raw recv msg: %s\n" % msg_raw)

            if is_recv_json:
                handle_json_msg(jsonapi.loads(msg_raw[0]))

            else:
                msg_proto = RequestMessageWrapper()
                msg_proto.ParseFromString(msg_raw[0])
                assert msg_proto is not None
                handle_proto_proto(msg_proto)

            # 回复
            msg_resposne = ResponseMessageWrapper()
            msg_resposne.msg_type = "resposne"
            msg_resposne.msg_test.test = u"Done!"
            s.send(msg_resposne.SerializeToString())

        stream.on_recv(echo)

        log("starting loop...")

        loop.start()

    log("server finish")


# -------------------------------------------------------------------------
# END OF FILE -------------------------------------------------------------
# -------------------------------------------------------------------------
