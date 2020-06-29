from __future__ import print_function


def log(message):
    # Used for logging messages with a prefix in the EDMC log file
    # Found at %TMP%\EDMarketConnector.log on Windows
    print("[ExProg] " + message)
