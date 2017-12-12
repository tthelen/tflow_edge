import asyncio
import logging
loglevel = logging.INFO
logging.basicConfig(level=loglevel)
import numpy as np

from Traumschreiber import *
from twisted.internet import reactor, defer, task

SHOWPLOT = True

########################################
# ID of the traumschreiber you are using
ID = 4
########################################

GAIN =8 
TRAUMSCHREIBER_ADDR = "74:72:61:75:6D:{:02x}".format(ID)

duration=5000
cnt = 0
data = np.zeros((duration,8), dtype='<i2')
outfile = None

all_data = []

def show_experiment():
    import webbrowser
    import os
    webbrowser.open_new_tab("file:///home/staff/t/tthelen/ni_course/tflow_edge/experiment/exp.html")

def data_callback(data_in):
    """Callback for data received from Traumschreiber."""
    global data
    global cnt
    global outfile
    # print(data_in[0][0])
    data = np.roll(data, -1, axis=0)
    data[-1,:] = data_in
    outfile.write("{},{},{},{},{},{},{},{}\n".format(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7]))
    cnt += 1

if SHOWPLOT:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib import pyplot as pp
    def plot():
        try:
            for i,line in enumerate(lines):
                fig.canvas.restore_region(background[i])
                line.set_data(tt, data[:,i])
                ax[i].draw_artist(line)
                #fig.canvas.set_window_title("Data (received {} packages/second)".format(pkgs_per_second))
                fig.canvas.blit(ax[i].bbox)
        except Exception as e:
            print("Encountered exception in plot callback: {}".format(e))

async def run():
    show_experiment()   
    global outfile
    import uuid
    outfile = open("../experiment/data/{}.csv".format(uuid.uuid1().hex),"w")
 
    async with Traumschreiber(addr=TRAUMSCHREIBER_ADDR) as t:
        await t.start_listening(data_callback)
        await async_sleep(1)
        await t.set(gain=GAIN)
        await async_sleep(50)
        if SHOWPLOT:
            plot()


def main(reactor):
    d = defer.ensureDeferred(run())
    return d


if SHOWPLOT:
    # Plot lines
    fig, ax = pp.subplots(nrows=8, ncols=1, figsize=(15,10), sharex=True, sharey=True)
    fig.show()
    fig.canvas.draw()

    tt = np.arange(duration)
    lines = [ax[i].plot(tt, data[:,i])[0] for i in range(8)]
    hlines = [(ax[i].axhline(y=2**11, c="black"), ax[i].axhline(y=-2**11, c="black")) for i in range(8)]
    ax[0].set_ylim([-2**12, 2**12])
    background = [fig.canvas.copy_from_bbox(ax[i].bbox) for i in range(8)]
    task.LoopingCall(plot).start(0.5)

task.react(main)
