# Copyright (c) 2019 Alliance for Sustainable Energy, LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

