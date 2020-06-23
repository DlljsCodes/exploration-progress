# EDMC plugin for Exploration Progress
import sys

import myNotebook as nb
from config import config
from theme import theme

from system import System
from log import log
import calculate

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
    this.origin_system = tk.StringVar(value=config.get("ExProg_OriginSystem"))
    this.destination_system = tk.StringVar(value=config.get("ExProg_DestinationSystem"))
    nb.Label(frame, text="Origin System").grid()
    nb.Entry(frame, textvariable=this.origin_system).grid()
    nb.Label(frame, text="Destination System").grid()
    nb.Entry(frame, textvariable=this.destination_system).grid()
    nb.Label(frame, text="Exploration Progress by Dlljs").grid()
    return frame


def prefs_changed(cmdr, is_beta):
    # Save settings
    config.set("ExProg_OriginSystem", this.origin_system.get())
    config.set("ExProg_DestinationSystem", this.destination_system.get())
    update_systems()


def plugin_app(parent):
    # Widget for main EDMC window
    this.frame = tk.Frame(parent)
    this.title = tk.Label(this.frame, text="Exploration Progress")
    this.title.grid()
    this.progress = tk.Label(this.frame, text="No Data")
    this.progress.grid()
    this.status = tk.Label(this.frame, text="")
    this.status.grid()
    update_systems()
    return this.frame


def journal_entry(cmdr, is_beta, system, station, entry, state):
    if entry['event'] == 'FSDJump':
        # Arrived in system
        log("New FSDJump event detected, updating current system...")
        current.setName(name=entry["StarSystem"], verify=False, populate=False)
        coords = tuple(entry["StarPos"])
        current.setCoords(coords[0], coords[1], coords[2])
        log("Updated current system")
        update_status()
        update_progress()


def update_systems():
    log("Updating origin and destination systems...")
    origin_name = config.get("ExProg_OriginSystem")
    destination_name = config.get("ExProg_DestinationSystem")
    log("Origin system: " + str(origin_name) + ", Destination system: " + str(destination_name))
    origin.setName(name=origin_name, verify=True, populate=True)
    destination.setName(name=destination_name, verify=True, populate=True)
    log("Origin and destination systems updated")
    update_status()
    update_progress()


def update_progress():
    log("Updating progress...")
    log("Getting coordinates...")
    origin_coords = origin.getCoords()
    destination_coords = destination.getCoords()
    current_coords = current.getCoords()
    log("Calculating percentage...")
    percentage = calculate.calculate_progress(origin_coords, current_coords, destination_coords)
    this.progress["text"] = str(percentage) + "%"
    theme.update(this.frame)
    log("Progress updated")


def update_status():
    log("Updating status...")
    status_message = ""
    status_colour = ""
    if not origin.getNameSet():
        log("Origin system not set")
        status_message = "The origin system hasn't been specified.\n" \
                         "Set it in the Exploration Progress tab in File -> Settings."
        status_colour = "red"
    elif not destination.getNameSet():
        log("Destination system not set")
        status_message = "The destination system hasn't been specified.\n" \
                         "Set it in the Exploration Progress tab in File -> Settings."
        status_colour = "red"
    elif not origin.getNameVerified():
        log("Origin system not verified")
        status_message = "Could not find the origin system " + origin.getName() + " in EDSM database.\n" \
                         "Either it doesn't exist or there was a problem connecting."
        status_colour = "red"
    elif not destination.getNameVerified():
        log("Destination system not verified")
        status_message = "Could not find the destination system " + destination.getName() + " in EDSM database.\n" \
                         "Either it doesn't exist or there was a problem connecting."
        status_colour = "red"
    elif not current.getNameSet():
        log("Current system not set")
        status_message = "Where are you?\n" \
                         "Make a hyperspace jump to find your current location."
        status_colour = "yellow"
    else:
        log("All systems go!")
        status_message = "All systems go!"
        status_colour = "green"

    this.status["text"] = status_message
    this.status["foreground"] = status_colour
    theme.update(this.frame)
    log("Status updated")
