Queueing-tool
=============

Queueing-tool is an Python simulation package for analyzing networks of queues.
The simulations are event based, where events are comprised as arrivals and 
departures of agents that move from queue to queue in the network. The network
is represented as a graph, which is handled by graph-tool.

Check out the [documentation](http://queueing-tool.readthedocs.org/) for more
information about this package.

## What do I need? How do I install it?

It works in Python either 2.7, 3.2, 3.3, and 3.4. In order to install it, you
need [`graph-tool`](http://graph-tool.skewed.de/download#packages) and 
[`numpy`](http://www.numpy.org/). Once you have those, you can install this
package by cloning this repository (or downloading the zip) and running the
following command in a terminal:

```bash
python3 setup.py install --user
```
## Features

  - It's fast. `queueing-tool` is designed for medium sized agent-based simulations -- say the downtown road network of a city with 5000 cars -- and it is build with performance in mind. Using `graph-tool` for the networking component makes most network operations very fast. With a heap based scheduler managing events, things don't get much quicker.
  - It's flexible. You can use general functions (including time dependent functions) for the arrival and departure rates for each queue. You can have queues along the edges (for either directed or undirected graphs) and queues along the nodes too.
  - It's friendly (sometimes). There are functions that make incorporating transportation networks from [openstreetmaps.org](www.openstreetmaps.org) easy.


### Creating Pittsburgh's Transportation Network

The [following](http://nbviewer.ipython.org/gist/djordon/975bf898c1ed2f4c8198) is an old demo showing how to set up downtown Pittsburgh's traffic network. It does not use `queueing_tool`, but details how to use [openstreetmaps.org] with `graph_tool` to create a graph for inclusion with `queueing_tool`.


##### Copyright and license

Code and documentation copyright 2014-2015 Daniel Jordon. Code released under the [MIT license](https://github.com/djordon/queueing-tool/blob/master/LICENSE).
