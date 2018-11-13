import zmq
import numpy as np
from time import sleep
from itertools import cycle
from numpy import random
import zlib
import json
import pickle

data_count = 14

keys = ['pv_' + str(i) for i in range(data_count)]


def waveform_gen(length=10):
    waveforms = []
    for i in range(1):
        waveforms.append(np.random.uniform(-1, 9, size=(length,)))
    return cycle(waveforms)


if __name__ == "__main__":
    ctx = zmq.Context()
    skt = ctx.socket(zmq.PUB)
    skt.bind('tcp://127.0.0.1:9000')

    waveform_gen = waveform_gen()
    for n in range(100):
        flags = 0
        protocol = -1
        b = random.randn(100, )
        obj = dict(zip(keys, b))
        obj['time'] = n
        # pobj = pickle.dumps(obj, protocol)
        # zobj = zlib.compress(pobj)
        jobj = json.dumps(obj).encode('utf8')
        zobj = zlib.compress(jobj)
        print('zipped pickle is %i bytes' % len(zobj))
        skt.send(zobj)
        sleep(0.1)

    skt.close()

