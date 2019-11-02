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
import argparse
import json
import zlib
import pickle
import math
from scipy import signal
from datetime import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port", type=int, help="port number, the default is 9001", default=9001, required=False)
    args = parser.parse_args()
    # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.square.html
    t = np.linspace(0, 1, 500, endpoint=False)
    square = signal.square(2 * np.pi * 5 * t)
    sig_cos = np.cos(2 * np.pi * t)
    sig_sin = np.sin(2 * np.pi * t)
    # pulse-width modulated sine wave
    pwm = signal.square(2 * np.pi * 30 * t, duty=(sig_sin + 1) / 2)

    ctx = zmq.Context()
    skt = ctx.socket(zmq.PUB)
    skt.setsockopt(zmq.IMMEDIATE,0)
    skt.bind('tcp://127.0.0.1:'+str(args.port))
    sleep(.3)

    obj = dict(first=dict(first=1, time=1))
    jobj = json.dumps(obj).encode('utf8')
    zobj = zlib.compress(jobj)
    print('zipped pickle is %i bytes' % len(zobj))
    skt.send(zobj)
    sleep(.1)

    # exit()
    import time
    seconds = int(time.time())
    print(datetime.fromtimestamp(1374510722).strftime("%Y-%m-%d %H:%M:%S"))
    exit(0)

    for count, n in enumerate(t):
        # count*=10
        print(seconds+count)
        print(datetime.fromtimestamp((seconds+count) ))
        flags = 0
        protocol = -1
        sig = math.sin(2 * math.pi * n)
        sin_temp = math.sin(math.pi * n)
        obj = {}
        waves = dict(sin_wave=dict(data=sin_temp, time=seconds+count),
                     cos_wave=dict(data=sig_cos[count], time=seconds+count),
                     sin_sig_wave=dict(data=sig_sin[count], time=seconds+count))
        squares = dict(square_wave=dict(data=square[count], time=seconds+count),
                       pulse_width_modulated=dict(data=pwm[count], time=seconds+count))
        # waves['time'] = count
        # squares['time'] = count
        obj['Waves'] = waves
        obj['Squares'] = squares
        pobj = pickle.dumps(obj, protocol)
        jobj = json.dumps(obj).encode('utf8')
        zobj = zlib.compress(jobj)
        #         print('zipped pickle is %i bytes' % len(zobj))
        skt.send(zobj)
        sleep(0.1)
    skt.close()