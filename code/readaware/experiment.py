#from utils import *
#from Traumschreiber import *
from twisted.internet import reactor, defer, task
import itertools
import random

# This module-level variable (buh!) keeps track of the current state of the experiment
state = "idle"

# This is an asynchroneous co-routine for running the experiment itself
async def experiment(display_duration=15, display_pause=5, offset=2):
    """ Readaware experiment (COROUTINE) 

    Meaningful texts and nonsense texts are displayed alternatively include a pause.

    Args:
        display_duration (int):      Number of seconds a text is displayed.
        display_pause (int):         Number of seconds between the texts.
        offset (int):                Number of seconds data is marked as good after start of text display.
    """
    global state


    good_texts=["t1.html","t2.html","t3.html","t4.html","t5.html"]
    nonsense_texts=["n1.html", "n2.html", "n3.html", "n4.html", "n5.html"]
    pause=["pause.html"]

    def show_text(name):
        import webbrowser
        webbrowser.open_new_tab("/net/home/staff/t/tthelen/ni_course/tflow_edge/experiment/"+name)

    for i in range(len(good_texts)):

        # show good text and set status to "good" after [offest] seconds
        state="idle"
        show_text(good_texts[i])
        await async_sleep(offset)
        state="good"
        await async_sleep(display_duration-offset)

        # show blank screen for [pause] seconds
        state="idle"
        show_text(pause)
        await async_sleep(display_pause)

        # show nonsense text and set status to "nonsense" after [offest] seconds
        state="idle"
        show_text(good_texts[i])
        await async_sleep(offset)
        state="nonsense"
        await async_sleep(display_duration-offset)

        # show blank screen for [pause] seconds
        state="idle"
        show_text(pause)
        await async_sleep(display_pause)

    # The experiment is done!

