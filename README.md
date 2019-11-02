# bokeh-streaming

Simple examples of bokeh streaming data.
The plots intended to be generic and able to infere some of the plot data from the structure of the data sent.
The reciever accepts zlib compressed pickled python dictionaries. 

Download Anaconda from https://www.anaconda.com/distribution/

Create a python environment from the command line.
```bash
conda create env -n plotting python=3.7
```

Install pyzmq and bokeh
```bash
conda create env -n plotting python=3.6
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

bokeh serve --show bokeh_two_plot/ --args --port 9001

```
In terminal two:
```bash
python single_sender
```

Data for a single chart

```
{
    "data point 1": float,
    "data point 2": float, ...
    "time": integer
} 
```

Randomly generated PV example
```json
{
  "pv_0": -0.03568330468421164,
  "pv_1": 0.26250448674065885,
  "pv_2": -1.6901414072228789,
  "pv_3": -0.018940116305679516,
  "pv_4": -1.2290262355952999,
  "pv_5": -0.5880334694278473,
  "pv_6": -0.525664695078223,
  "pv_7": 0.1917121948689335,
  "pv_8": 0.4704982063254248,
  "pv_9": -1.709025667850248,
  "pv_10": 0.01112962508032731,
  "pv_11": 0.8119457471683316,
  "pv_12": -0.3676396520228328,
  "pv_13": 0.35318272766044667,
  "time": 0
}
```


Data structure for multiple topics/charts

```
{
  "Data for chart 1": {
    "data point 1": float,
    "data point 2": float, ...
    "time": integer
  },  
   "Data for chart 2": {
    "data point 1": float,
    "data point 2": float, ...
    "time": integer
  },...
}
```

Example pv data
```json
{
  "Power P (KW)": {
    "dg_30_PVPanels": 261.9179106555036,
    "dg_36_PVPanels": 337.49414367971985,
    "dg_72_PVPanels": 312.72475536152064,
    "dg_60_PVPanels": 221.95755130439775,
    "dg_18_PVPanels": 211.03686710385787,
    "dg_90_PVPanels": 292.33645857697115,
    "dg_54_PVPanels": 60.33543378420453,
    "dg_48_PVPanels": 180.93488835551187,
    "time": 1,
    "dg_42_PVPanels": 130.51091791720054,
    "dg_66_PVPanels": 286.8685841973896,
    "dg_78_PVPanels": 130.93986245593857,
    "dg_84_PVPanels": 261.637758357402,
    "dg_12_PVPanels": 100.85157625964355,
    "dg_6_PVPanels": 526.3539577948383
  },
  "Load Demand (MW)": {
    "time": 1,
    "Load Demand (MW)": 12.202891997438853
  },
  "PVGeneration(MW)": {
    "time": 1,
    "PVGeneration(MW)": 3315.9006658041
  }
}
```

 