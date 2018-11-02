from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,  SaveTool, ZoomInTool, BoxZoomTool, ResetTool
from bokeh.io import curdoc
from bokeh.palettes import Category20_20, Inferno256, Greys256

import receiver

# https://github.com/zeromq/pyzmq/blob/master/examples/serialization/serialsocket.py

FPS = 1
rollover = 200

doc = curdoc()
first_time=True

source_dict ={'pv_0' :  ColumnDataSource({'time': [], 'data': []}),
              'pv_1': ColumnDataSource({'time': [], 'data': []}),
              }


def create_figure(title='Power Q'):
    global f
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
    if len(receiver.buffer) > 0:
        data = receiver.buffer.popleft()
        # print(data)
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
            source.stream(new_data, rollover)

doc.add_periodic_callback(update_mutli_line, 1000/FPS)


