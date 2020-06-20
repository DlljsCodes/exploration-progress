# EDMC plugin for Exploration Progress
from log import log


def plugin_start3(plugin_dir):
    # Load plugin into EDMC in Python 3 mode
    log("Exploration Progress has been loaded from " + plugin_dir)
    return "Exploration Progress"


def plugin_stop():
    # Close plugin as EDMC is closing
    log("Exploration Progress is closing!")