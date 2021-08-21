# EDMC plugin for Exploration Progress
import sys
import os
import logging
import semantic_version

import myNotebook as nb
from ttkHyperlinkLabel import HyperlinkLabel
from config import appname, appversion, config
from theme import theme

from system import System
import calculate

try:
    # Python 2
    import Tkinter as tk
    import ttk
except ModuleNotFoundError:
    # Python 3
    import tkinter as tk
    import tkinter.ttk as ttk

# Get EDMC version
if isinstance(appversion, str):
    edmc_version = semantic_version.Version(appversion)
elif callable(appversion):
    edmc_version = appversion()

# Setup logging
plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f'{appname}.{plugin_name}')
if not logger.hasHandlers():
    level = logging.INFO
    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

this = sys.modules[__name__]	# For holding module globals

origin = System()
destination = System()
current = System()

plugin_version = semantic_version.Version("1.0.3")

def plugin_start():
    # Load plugin into EDMC
    logger.info("Exploration Progress has been loaded")
    return "Exploration Progress"


def plugin_start3(plugin_dir):
    # Python 3 mode
    return plugin_start()


def plugin_stop():
    # Close plugin as EDMC is closing
    logger.info("Exploration Progress is closing!")


def plugin_prefs(parent, cmdr, is_beta):
    # Plugin settings GUI in EDMC Settings dialog
    frame = nb.Frame(parent)
    this.origin_system = tk.StringVar(value=get_config_str_value("ExProg_OriginSystem"))
    this.destination_system = tk.StringVar(value=get_config_str_value("ExProg_DestinationSystem"))
    nb.Label(frame, text="Origin System").grid()
    nb.Entry(frame, textvariable=this.origin_system).grid()
    nb.Label(frame, text="Destination System").grid()
    nb.Entry(frame, textvariable=this.destination_system).grid()
    nb.Label(frame, text=f"Exploration Progress (v{plugin_version}) by Dlljs").grid()
    HyperlinkLabel(frame, text="View on GitHub", background=nb.Label().cget('background'),
                   url="https://github.com/DlljsCodes/exploration-progress").grid()
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
        logger.info("New event with system info detected, updating current system...")
        current.setName(name=entry["StarSystem"], verify=False, populate=False)
        coords = tuple(entry["StarPos"])
        current.setCoords(coords[0], coords[1], coords[2])
        logger.info("Updated current system")
        update_status()
        update_progress()


def get_config_str_value(key):
    # Wrapper for either config.get_str() (EDMC <=5.0.0) or config.get (EDMC >5.0.0)
    if edmc_version > semantic_version.Version("5.0.0-beta1"):
        # At least EDMC 5.0.0
        logger.debug(f"EDMC version {edmc_version} should be at least 5.0.0-beta1")
        value = config.get_str(key)
    else:
        # Before EDMC 5.0.0
        logger.debug(f"EDMC version {edmc_version} should be before 5.0.0-beta1")
        value = config.get(key)
    return value


def update_systems():
    logger.info("Updating origin and destination systems...")
    origin_name = get_config_str_value("ExProg_OriginSystem")
    destination_name = get_config_str_value("ExProg_DestinationSystem")
    logger.debug(f"Origin system: {origin_name}, Destination system: {destination_name}")
    origin.setName(name=origin_name, verify=True, populate=True)
    destination.setName(name=destination_name, verify=True, populate=True)
    logger.info("Origin and destination systems updated")
    update_status()
    update_progress()


def update_progress():
    logger.info("Updating progress...")
    systems_set = 0
    if origin.getNameSet() and origin.getNameVerified():
        logger.debug("Origin system set and verified")
        systems_set += 1
    if destination.getNameSet() and destination.getNameVerified():
        logger.debug("Destination system set and verified")
        systems_set += 1
    if current.getNameSet():
        logger.debug("Current system set")
        systems_set += 1
    logger.debug(f"{systems_set} system(s) set")
    if systems_set == 3:
        logger.debug("Getting coordinates...")
        origin_coords = origin.getCoords()
        destination_coords = destination.getCoords()
        current_coords = current.getCoords()
        logger.debug("Calculating percentage...")
        percentage = calculate.calculate_progress(origin_coords, current_coords, destination_coords)
        this.progress["text"] = str(percentage) + "%"
        this.bar["value"] = percentage
    else:
        logger.debug("Can't show progress at this time")
        this.progress["text"] = "??.??%"
        this.bar["value"] = 0
    theme.update(this.frame)
    logger.info("Progress updated")


def update_status():
    logger.info("Updating status...")
    status_message = ""
    status_colour = ""
    if not origin.getNameSet():
        logger.debug("Origin system not set")
        status_message = "The origin system hasn't been specified.\n" \
                         "Set it in the Exploration Progress tab in File -> Settings."
        status_colour = "red"
    elif not destination.getNameSet():
        logger.debug("Destination system not set")
        status_message = "The destination system hasn't been specified.\n" \
                         "Set it in the Exploration Progress tab in File -> Settings."
        status_colour = "red"
    elif not origin.getNameVerified():
        logger.debug("Origin system not verified")
        status_message = "Could not find the origin system " + origin.getName() + " in EDSM database.\n" \
                         "Either it doesn't exist or there was a problem connecting."
        status_colour = "red"
    elif not destination.getNameVerified():
        logger.debug("Destination system not verified")
        status_message = "Could not find the destination system " + destination.getName() + " in EDSM database.\n" \
                         "Either it doesn't exist or there was a problem connecting."
        status_colour = "red"
    elif not current.getNameSet():
        logger.debug("Current system not set")
        status_message = "Where are you?\n" \
                         "Either log into the game or\n" \
                         "make a hyperspace jump to find your current location."
        status_colour = "dark orange"
    else:
        logger.debug("All systems go!")
        status_message = ""
        status_colour = "green"

    this.status["text"] = status_message
    this.status["foreground"] = status_colour
    theme.update(this.frame)
    logger.info("Status updated")
