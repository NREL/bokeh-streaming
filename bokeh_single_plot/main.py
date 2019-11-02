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

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,  SaveTool, ZoomInTool, BoxZoomTool, ResetTool
from bokeh.io import curdoc
from bokeh.palettes import Category20_20, Inferno256, Greys256

import receiver

# https://github.com/zeromq/pyzmq/blob/master/examples/serialization/serialsocket.py

FPS = 5
time_rollover = 20

doc = curdoc()
first_time=True

source_dict ={'pv_0' :  ColumnDataSource({'time': [], 'data': []}),
              'pv_1': ColumnDataSource({'time': [], 'data': []}),
              }
x = ColumnDataSource({'time': [], 'data': []})



def create_figure(title='Power P'):
    hover = HoverTool(tooltips=[
        ('Name', '$name'),
        ("Time", "@time"),
        (title, "@data")
    ])
    f = figure(plot_width=800,
               plot_height=600,
               # x_axis_type='datetime',
               x_axis_type='auto',
               tools=[hover, SaveTool(), ZoomInTool(), BoxZoomTool(), ResetTool()],
               title="Real-Time " + title + " Plot"
               )
    # f= figure()
    # f.line(x='time', y='power', source=source_dict['pv_0'], legend='pv_0')
    # f.line(x='time', y='power', source=source_dict['pv_1'], legend='pv_1')
    f.xaxis.axis_label = "Time"
    f.yaxis.axis_label = title
    return f


def update_mutli_line():
    global first_time
    global time_rollover
    if len(receiver.buffer) > 0:
        data = receiver.buffer.popleft()
        print(data)
        keys = list(data.keys())
        keys.remove('time')
        if first_time:
            f = create_figure('Power Q')
            color_spectrum = Category20_20
            if len(keys) > 20:
                color_spectrum = Greys256
            for name, color in zip(keys, color_spectrum):
                source_dict[name] = ColumnDataSource({'time': [], 'data': []})
                source_dict[name+'_data'] = []
                f.line(x='time', y='data', source=source_dict[name],color=color, legend=name, name=name)
                first_time=False
                # break
            f.legend.location = "top_left"
            f.legend.click_policy = "hide"
            doc.add_root(f)

        for index, name in enumerate(keys):
            first = data[name]
            source = source_dict[name]
            # data_list = source_dict[name + '_data']
            # data_list.append(first)
            # source.data.update(time=range(data['time']), power=data_list)
            # source.data.update(time=range(len(data_list)), power=data_list)
            new_data = {
                'time': [data['time']],
                'data': [first],
            }
            source.stream(new_data, rollover=20)

doc.add_periodic_callback(update_mutli_line, 1000/FPS)


