# Intro
This repository contains a command-line tool for Maplelegends. 

It is used to calculate the best scrolling sequence to lower the gear making cost.

# How to use
1. Clone this repository.

2. Make sure python is installed

3. Run ```pip install termcolor```, that's the only lib required for now.

4. You're all set. Run ```python main.py``` and interact with the tool using command line.

# Use hints:
The owlrepo data is auto-download when you first time runs main.py.

If you found owlrepo data too old, you can either delete the owl_*.json file and re-run, or use the home page command to update.

And the program will use Scrolls.json first, if no required data then update scrolls from owl_*.json to Scrolls.json

If you want to use a scroll's data from owlrepo instead of local Scroll.json data, delete it in Scroll.json or use command to remove it.

# Functionalities

- [x] manage scrolls data
- [x] manage gears data
- [x] update scrolls data from owlrepo
- [x] generate output besed on a given scrolling sequence and gear
- [x] save/load scrolling sequences to/from file (achieved by QuickCommand)
- [x] generate the best order for given sequence
- [x] generate the best ordered sequence for given expected 10%/30% success number and 60%/70% success number 