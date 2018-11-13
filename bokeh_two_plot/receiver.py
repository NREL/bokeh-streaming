from collections import deque
import zmq
import numpy as np
import zlib
import pickle
import json

buffer = deque(maxlen=100)


def recv_zipped_pickle(zmq_socket, flags=0):
    """reconstruct a Python object sent with zipped_pickle"""
    zobj = zmq_socket.recv()
    # print(zobj)
    # pobj = zlib.decompress(zobj)
    # return pickle.loads(pobj)
    jobj = zlib.decompress(zobj)
    return json.loads(jobj)

def stream_receive():
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.SUB)
    zmq_socket.setsockopt_string(zmq.SUBSCRIBE, "")
    zmq_socket.connect("tcp://127.0.0.1:9000")

    poller = zmq.Poller()
    poller.register(zmq_socket, zmq.POLLIN)
    
    while True:
        events = dict(poller.poll(1000))
        if zmq_socket in events:
            buffer.append(recv_zipped_pickle(zmq_socket))

