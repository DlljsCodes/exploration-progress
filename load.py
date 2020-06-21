# EDMC plugin for Exploration Progress
from log import log


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