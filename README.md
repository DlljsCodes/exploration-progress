# Exploration Progress

A plugin for [ED Market Connector](https://github.com/EDCD/EDMarketConnector) and a simple Python program that allows [Elite Dangerous](https://www.elitedangerous.com/) explorer players to see their progress from one star system to another. 

## EDMC Plugin
This is a plugin for [ED Market Connector](https://github.com/EDCD/EDMarketConnector) that uses its many features to get real-time information on your CMDR's current location and display an auto updating progress indicator on the EDMC interface. The origin and destination system names are saved to your machine so you don't have to keep entering them every time.

**Please note:** Just like EDMC itself, this plugin only supports the PC & macOS versions of Elite Dangerous. Console (i.e. PS4 & Xbox One) versions are not supported.

### Requirements
* [EDMC](https://github.com/EDCD/EDMarketConnector) (v3.4.6.0+, may work on older versions)
* Internet connection (to connect to [EDSM](https://www.edsm.net/))

### How to Install
1. Get the [latest release](https://github.com/DlljsCodes/exploration-progress/releases/latest)
1. Extract the file
1. Copy the extracted folder into the EDMC plugin directory (you can find this by starting EDMC, going to File -> Settings, clicking on the "Plugins" tab and then clicking on the "Open" button)
1. Restart EDMC if already open

### How to Use
1. Run EDMC
1. Go to File -> Settings and click on the "Exploration Progress" tab
1. Enter the system you started at (Origin System)
1. Enter the system you are heading towards (Destination System)
1. Click "OK"
1. Log into Elite Dangerous or, if already in the game, make a hyperspace jump to find your current location
1. Your progress towards the destination system will be displayed as a percentage and on a progress bar, and will auto-update as you travel

Tip: If you get stuck, see the red text in the Exploration Progress section of the EDMC window

## Standalone Program
Alternatively, you can use the original proof of concept standalone program, which is very simple. It unfortunately does not save your origin and destination systems and cannot automatically get your current system from the game. It also does not auto update, so you'll need to run the program and reenter information every time you want to get an update on your progress. As a result, _this stanalone program may be depreciated in the future_.

### Requirements
* [Python](https://www.python.org/) 3.7
* Internet connection (to connect to [EDSM](https://www.edsm.net/))

### How to Use
1. Get the [latest release](https://github.com/DlljsCodes/exploration-progress/releases/latest)
1. Extract the file
1. Run standalone.py
1. Enter the system you started at (Origin System)
1. Enter the system you are heading towards (Destination System)
1. Enter the system your current system (Current System)
1. Your progress towards the destination system will be displayed as a percentage
