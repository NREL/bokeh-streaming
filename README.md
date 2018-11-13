# bokeh-streaming

Simple examples of bokeh streaming data.
The plots intended to be generic and able to infere some of the plot data from the structure of the data sent.
The reciever accepts zlib compressed pickled python dictionaries. 


Install pyzmq and bokeh
```bash
conda install pyzmq bokeh
```
Or

```bash
pip install pyzmq bokeh
```

## Single plot
In terminal one:
```bash
bokeh serve --show bokeh_single_plot/
```
In terminal two:
```bash
python single_sender
```

## Multiple plots
In terminal one:
```bash
bokeh serve --show bokeh_two_plot/
```
In terminal two:
```bash
python single_sender
```


 