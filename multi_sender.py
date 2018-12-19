import zmq
import numpy as np
from time import sleep
import json
import zlib
import pickle
import math
from scipy import signal

if __name__ == "__main__":
    # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.square.html
    t = np.linspace(0, 1, 500, endpoint=False)
    square = signal.square(2 * np.pi * 5 * t)
    sig_cos = np.cos(2 * np.pi * t)
    sig_sin = np.sin(2 * np.pi * t)
    # pulse-width modulated sine wave
    pwm = signal.square(2 * np.pi * 30 * t, duty=(sig_sin + 1) / 2)

    ctx = zmq.Context()
    skt = ctx.socket(zmq.PUB)
    skt.bind('tcp://127.0.0.1:9000')

    for count, n in enumerate(t):
        flags = 0
        protocol = -1
        sig = math.sin(2 * math.pi * n)
        sin_temp = math.sin(math.pi * n)
        obj = {}
        waves = dict(sin_wave=dict(data=sin_temp, time=count),
                     cos_wave=dict(data=sig_cos[count], time=count),
                     sin_sig_wave=dict(data=sig_sin[count], time=count))
        squares = dict(square_wave=dict(data=square[count], time=count),
                       pulse_width_modulated=dict(data=pwm[count], time=count))
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