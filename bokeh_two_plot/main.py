from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,  SaveTool, ZoomOutTool, ZoomInTool, BoxZoomTool, ResetTool
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.palettes import Category20_20, Inferno256, Greys256

import receiver

# https://github.com/zeromq/pyzmq/blob/master/examples/serialization/serialsocket.py

FPS = 5

doc = curdoc()
first_time=True

source_dict ={'pv_0' :  ColumnDataSource({'time': [], 'data': []}),
              'pv_1': ColumnDataSource({'time': [], 'data': []}),
              }

def create_figure(title='Power P'):
    hover = HoverTool(tooltips=[
        # ('Name', '$name'),
        ("Time", "@time"),
        (title, "@data")
    ])
    f = figure(plot_width=700,
               plot_height=500,
               # x_axis_type='datetime',
               x_axis_type='auto',
               tools=[hover, SaveTool(), ZoomOutTool(), ZoomInTool(), BoxZoomTool(), ResetTool()],
               title="Real-Time " + title + " Plot"
               )
    f.xaxis.axis_label = "Time"
    f.yaxis.axis_label = title
    return f


def update_mutli_line():
    global first_time
    if len(receiver.buffer) > 0:
        top_data = receiver.buffer.popleft()
        print(top_data)
        if first_time:
            figure_container = []

            for key_name in top_data.keys():
                data = top_data[key_name]
                keys = list(data.keys())
                print(keys)
                keys.remove('time')
                temp_figure = create_figure(key_name)
                color_spectrum = Category20_20
                if len(keys) > 20:
                    color_spectrum = Greys256
                for name, color in zip(keys, color_spectrum):
                    source_dict[name] = ColumnDataSource({'time': [], 'data': []})
                    print('name ' + name)
                    temp_figure.line(x='time', y='data', source=source_dict[name], color=color, legend=name, name=name)
                temp_figure.legend.location = "top_left"
                temp_figure.legend.click_policy = "hide"
                figure_container.append(temp_figure)

            first_time = False
            doc.add_root(column(figure_container, name='Streaming'))

        for key_name in top_data.keys():
            data = top_data[key_name]

            keys = list(data.keys())
            keys.remove('time')
            for index, name in enumerate(keys):
                first = data[name]
                source = source_dict[name]
                new_data = {
                    'time': [data['time']],
                    'data': [first],
                }
                source.stream(new_data, rollover=120)


doc.add_periodic_callback(update_mutli_line, 1000/FPS)
