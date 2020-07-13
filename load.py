# EDMC plugin for Exploration Progress
import sys
import os

import myNotebook as nb
from ttkHyperlinkLabel import HyperlinkLabel
from config import config
from theme import theme

from system import System
from log import log
import calculate
import database

try:
    # Python 2
    import Tkinter as tk
    import ttk
except ModuleNotFoundError:
    # Python 3
    import tkinter as tk
    import tkinter.ttk as ttk

this = sys.modules[__name__]	# For holding module globals

origin = System()
destination = System()
current = System()

version = "1.0.2-indev"
database_file = "systems.db"
database_file_path = ""


def plugin_start(plugin_dir):
    # Load plugin into EDMC
    global database_file_path
    database_file_path = os.path.join(plugin_dir, database_file)
    database.setup(database_file_path)
    log("Exploration Progress has been loaded")
    return "Exploration Progress"


def plugin_start3(plugin_dir):
    # Python 3 mode
    return plugin_start(plugin_dir)


def plugin_stop():
    # Close plugin as EDMC is closing
    log("Exploration Progress is closing!")


def plugin_prefs(parent, cmdr, is_beta):
    # Plugin settings GUI in EDMC Settings dialog
    success, origin_name, destination_name = database.get_systems(database_file_path, cmdr)
    if not success:
        origin_name = config.get("ExProg_OriginSystem")
        destination_name = config.get("ExProg_DestinationSystem")
    frame = nb.Frame(parent)
    this.origin_system = tk.StringVar(value=origin_name)
    this.destination_system = tk.StringVar(value=destination_name)
    nb.Label(frame, text="Origin System").grid()
    nb.Entry(frame, textvariable=this.origin_system).grid()
    nb.Label(frame, text="Destination System").grid()
    nb.Entry(frame, textvariable=this.destination_system).grid()
    nb.Label(frame, text="Exploration Progress (v" + version + ") by Dlljs").grid()
    HyperlinkLabel(frame, text="View on GitHub", background=nb.Label().cget('background'),
                   url="https://github.com/DlljsCodes/exploration-progress").grid()
    return frame


def prefs_changed(cmdr, is_beta):
    # Save settings
    config.set("ExProg_OriginSystem", this.origin_system.get())
    config.set("ExProg_DestinationSystem", this.destination_system.get())
    database.update(database_file_path, cmdr, this.origin_system.get(), this.destination_system.get())
    update_systems()


def plugin_app(parent):
    # Widget for main EDMC window
    this.frame = tk.Frame(parent)
    this.title = tk.Label(this.frame, text="Exploration Progress")
    this.title.grid()
    this.progress = tk.Label(this.frame, text="No Data")
    this.progress.grid()
    this.bar = ttk.Progressbar(this.frame, length=100, mode="determinate")
    this.bar.grid()
    this.status = tk.Label(this.frame, text="")
    this.status.grid()
    update_systems()
    return this.frame


def journal_entry(cmdr, is_beta, system, station, entry, state):
    if entry['event'] == 'FSDJump' or entry['event'] == 'Location' \
            or entry['event'] == 'StartUp' or entry['event'] == 'CarrierJump':
        # Arrived in system
        log("New event with system info detected, updating current system...")
        current.setName(name=entry["StarSystem"], verify=False, populate=False)
        coords = tuple(entry["StarPos"])
        current.setCoords(coords[0], coords[1], coords[2])
        log("Updated current system")
        update_status()
        update_progress()
        if current.getName() == destination.getName():
            log("Destination reached")
            # Reached destination
            config.set("ExProg_OriginSystem", "")
            config.set("ExProg_DestinationSystem", "")
            update_systems(ui_update=False)
            update_status("destination_reached")


def update_systems(ui_update=False):
    log("Updating origin and destination systems...")
    origin_name = config.get("ExProg_OriginSystem")
    destination_name = config.get("ExProg_DestinationSystem")
    log("Origin system: " + str(origin_name) + ", Destination system: " + str(destination_name))
    origin.setName(name=origin_name, verify=True, populate=True)
    destination.setName(name=destination_name, verify=True, populate=True)
    log("Origin and destination systems updated")
    if ui_update:
        update_status()
        update_progress()


def update_progress():
    log("Updating progress...")
    systems_set = 0
    if origin.getNameSet() and origin.getNameVerified():
        log("Origin system set and verified")
        systems_set += 1
    if destination.getNameSet() and destination.getNameVerified():
        log("Destination system set and verified")
        systems_set += 1
    if current.getNameSet():
        log("Current system set")
        systems_set += 1
    log(str(systems_set) + " system(s) set")
    if systems_set == 3:
        log("Getting coordinates...")
        origin_coords = origin.getCoords()
        destination_coords = destination.getCoords()
        current_coords = current.getCoords()
        log("Calculating percentage...")
        percentage = calculate.calculate_progress(origin_coords, current_coords, destination_coords)
        this.progress["text"] = str(percentage) + "%"
        this.bar["value"] = percentage
    else:
        log("Can't show progress at this time")
        this.progress["text"] = "??.??%"
        this.bar["value"] = 0
    theme.update(this.frame)
    log("Progress updated")


def update_status(external_message=None):
    log("Updating status...")
    status_message = ""
    status_colour = ""
    if external_message == "destination_reached":
        log("Destination reached")
        status_message = "You made it to\n" \
                         "your destination!"
        status_colour = "green"
    elif not origin.getNameSet():
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
                         "Either log into the game or\n" \
                         "make a hyperspace jump to find your current location."
        status_colour = "yellow"
    else:
        log("All systems go!")
        status_message = ""
        status_colour = "green"

    this.status["text"] = status_message
    this.status["foreground"] = status_colour
    theme.update(this.frame)
    log("Status updated")
