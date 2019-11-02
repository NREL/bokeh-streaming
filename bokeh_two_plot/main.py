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
from bokeh.models import ColumnDataSource, HoverTool,  SaveTool, ZoomOutTool, ZoomInTool, BoxZoomTool, ResetTool
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.palettes import Category20_20, Inferno256, Greys256, Set2_8

from datetime import datetime
import receiver

import os
import time

os.environ['TZ'] = 'UTC'
time.tzset()
# https://github.com/zeromq/pyzmq/blob/master/examples/serialization/serialsocket.py

FPS = 5

doc = curdoc()
first_time=True

source_dict_top = {}

def create_figure(title='Power P'):
    hover = HoverTool(tooltips=[
        ('Name', '@name'),
        ("Time", "@time"),
        ("Date", "@date"),
        (title, "@data")
    ])
    f = figure(plot_width=700,
               plot_height=500,
               x_axis_type='datetime',
               # x_axis_type='auto',
               tools=[hover, SaveTool(), ZoomOutTool(), ZoomInTool(), BoxZoomTool(), ResetTool()],
               title="Real-Time " + title + " Plot"
               )
    f.xaxis.axis_label = "Time"
    f.yaxis.axis_label = title
    f.xaxis.formatter = DatetimeTickFormatter(
        seconds="%X",
        # seconds=["%H:%M:%S"]
        # seconds="%d %B %Y",
        # minutes="%d %B %Y",
        # hours="%d %b %Y",
        # days="%d %b %Y",
        # months="%d %b %Y",
        # years="%d %b %Y"
    )
    return f


def update_mutli_line():
    global first_time
    # global source_dict
    # print(len(receiver.buffer))
    if len(receiver.buffer) > 0:
        top_data = receiver.buffer.popleft()
        print(top_data.keys())
        print('first' in top_data.keys())
        if 'first' in top_data.keys():  # reset graph
            print(top_data['first'])
            first_time = True
            doc.clear()
            # doc.remove_root()
            return

        if first_time:
            print('Start creation')
            figure_container = []

            for key_name in top_data.keys():
                data = top_data[key_name]
                keys = list(data.keys())
                print(keys)
                # keys.remove('time')
                temp_figure = create_figure(key_name)
                color_spectrum = Category20_20
                if len(keys) < 9:
                    color_spectrum = Set2_8
                if len(keys) > 20:
                    color_spectrum = Greys256
                source_dict_top[key_name] = {}
                for name, color in zip(keys, color_spectrum):
                    source_dict_top[key_name][name] = ColumnDataSource({'time': [], 'date': [], 'data': [], 'name':[]})
                    print('name ' + repr(name))
                    line_style = 'solid'
                    if 'forecast' in name.lower():
                        line_style = 'dashed'
                    temp_figure.line(x='time', y='data', source=source_dict_top[key_name][name], color=color, legend=name, name=name,
                                     line_width=3, line_dash=line_style)
                temp_figure.legend.location = "top_left"
                temp_figure.legend.click_policy = "hide"
                figure_container.append(temp_figure)

            print('End creation')
            first_time = False
            doc.add_root(column(figure_container, name='Streaming'))

        for key_name in top_data.keys():
            data = top_data[key_name]


            keys = list(data.keys())
            # keys.remove('time')
            for index, name in enumerate(keys):
                first = data[name]['data']
                source = source_dict_top[key_name][name]

                if type(first) is list:
                    print(len(first))
                    print(len(data[name]['time']))
                    new_data = {
                        'time': list(map(datetime.fromtimestamp, data[name]['time'])),
                        'date': list(map(datetime.fromtimestamp, data[name]['time'])),
                        'data': first,
                        'name': [name]*len(first)
                    }
                else:
                    # print(datetime.fromtimestamp(data[name]['time']*1000))
                    new_data = {
                        'time': [datetime.fromtimestamp(data[name]['time'])],
                        'date': [datetime.fromtimestamp(data[name]['time']).strftime("%Y-%m-%d %H:%M:%S")],
                        # 'date': [datetime.fromtimestamp(data[name]['time'])],
                        'data': [first],
                        'name': [name]
                    }
                source.stream(new_data, rollover=360)


# doc.add_periodic_callback(update_mutli_line, 1000/FPS)
doc.add_periodic_callback(update_mutli_line, 1000)  # Slow down for more plots
