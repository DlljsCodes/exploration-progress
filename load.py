# EDMC plugin for Exploration Progress
import sys
import TKinter as tk
import myNotebook as nb
from config import config
from system import System
from log import log

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