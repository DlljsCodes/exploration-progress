# EDMC plugin for Exploration Progress

def plugin_start3(plugin_dir):
    # Load plugin into EDMC in Python 3 mode
    log("Exploration Progress has been loaded from " + plugin_dir)
    return "Exploration Progress"


def plugin_stop():
    # Close plugin as EDMC is closing
    log("Exploration Progress is closing!")


def log(message):
    # Used for logging messages with a prefix in the EDMC log file
    # Found at %TMP%\EDMarketConnector.log on Windows
    print("[ExProg] " + message)