# EDMC plugin for Exploration Progress
import sys

import myNotebook as nb
from config import config

from system import System
from log import log

try:
    # Python 2
    import Tkinter as tk
except ModuleNotFoundError:
    # Python 3
    import tkinter as tk

this = sys.modules[__name__]	# For holding module globals

origin = System()
destination = System()
current = System()


def plugin_start():
    # Load plugin into EDMC
    log("Exploration Progress has been loaded")
    return "Exploration Progress"


def plugin_start3(plugin_dir):
    # Python 3 mode
    return plugin_start()


def plugin_stop():
    # Close plugin as EDMC is closing
    log("Exploration Progress is closing!")


def plugin_prefs(parent, cmdr, is_beta):
    # Plugin settings GUI in EDMC Settings dialog
    frame = nb.Frame(parent)
    this.origin_system = tk.StringVar(value=config.get("OriginSystem"))
    this.destination_system = tk.StringVar(value=config.get("DestinationSystem"))
    nb.Label(frame, text="Origin System").grid()
    nb.Entry(frame, textvariable=this.origin_system).grid
    nb.Label(frame, text="Destination System").grid()
    nb.Entry(frame, textvariable=this.destination_system).grid()
    nb.Label(frame, text="Exploration Progress by Dlljs")
    return frame


def prefs_changed(cmdr, is_beta):
    # Save settings
    config.set("OriginSystem", this.origin_system.get())
    config.set("DestinationSystem", this.destination_system.get())
    origin.setName(name=this.origin_system, verify=True, populate=True)
    destination.setName(name=this.destination_system, verify=True, populate=True)


def plugin_app(parent):
    # Widget for main EDMC window
    this.frame = tk.Frame(parent)
    title = tk.Label(this.frame, text="Exploration Progress")
    title.grid()
    progress = tk.Label(this.frame, text="No Data")
    progress.grid()
    status = tk.Label(this.frame)
    status.grid()
    return this.frame


def journal_entry(cmdr, is_beta, system, station, entry, state):
    if entry['event'] == 'FSDJump':
        # Arrived in system
        current.setName(name=entry["StarSystem"], verify=False, populate=False)
        coords = tuple(entry["StarPos"])
        current.setCoords(coords[0], coords[1], coords[2])
