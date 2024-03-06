# The Wind Waker Archipelago

The Wind Waker Archipelago modifies the base randomizer created by LagoLunatic to work with Archipelago multiworlds.
Dev5ter started the original project and has been maintained by the community since.

## Installation & Usage
See the [setup guide](https://github.com/tanjo3/tww_apworld/blob/master/docs/setup_en.md) for instructions.

## How does The Wind Waker get randomized?
Items get shuffled between the different locations in the game, so each playthrough is unique. Randomized locations
include chests, items received from NPC, and treasure salvaged from the ocean floor. The randomizer also includes
quality-of-life features such as a fully opened world, removing many cutscenes, increased sailing speed, and more.


In-game item models still need to be implemented in the project's current state. Instead, all items in the game will be
a green rupee. This is a temporary measure until item models are implemented. You'll receive the actual item for that
location from the Archipelago server.

## Which locations get shuffled?
All randomizable locations will have their items shuffled each seed. However, the randomizer is designed so that only
certain groups of locations can contain progression items. The remaining locations will only contain items unnecessary
to beat the game, such as rupees or Heart Pieces.

## What is the goal of The Wind Waker?
Reach and defeat Ganondorf atop Ganon's Tower. This will require all eight shards of the Triforce of Courage, the
fully-powered Master Sword (unless it's swordless mode), Light Arrows, and any other items necessary to reach Ganondorf.

## I need help! What do I do?
Refer to the [FAQ](https://lagolunatic.github.io/wwrando/faq/) first. If you are still stuck, please ask in the Wind
Waker thread (under `future-game-design`) in the Archipelago server.

## Known issues
* "Tower of the Gods - Stone Tablet" has been reported to be sent earlier than intended.
* It has been reported that some long sidequests ("Lenzo's House - Become Lenzo's Assistant" and "Linda and Anton") are
not sent properly.

Feel free to report any other issues in the Wind Waker thread in the Archipelago server! I'll take a look and see what I
can do. Suggestions for improvements are also welcome.

## Planned Features
* Support for remaining randomization options (such as required bosses mode)
* In-game item models

## Running from source
Download and install git from here: https://git-scm.com/downloads  
Then clone this repository with git by running this in a command prompt:  
`git clone https://github.com/tanjo3/tww_apworld.git`  

If you're on Windows, download and install Python 3.11 from here: https://www.python.org/downloads/release/python-3118/  
If you're on Linux, run this: `sudo apt-get install python3.11`  

Open the `tww` folder in a command prompt and install dependencies by running:  
`py -3.11 -m pip install -r requirements.txt` (on Windows)  
`python3 -m pip install $(cat requirements.txt) --user` (on Linux)  

## Credits
This randomizer would not be possible without the help from:
* LagoLunatic: (base randomizer)
* Dev5ter: (initial TWW AP implmentation)
* CrainWWR: (multiworld and Dolphin memory assistance, additional programming)
* Celeste (Tia): (logic and typo fixes, additional programming)
* DaemonHunter: (additional programming)
* Ouro: (tracker support)
* Tubamann: (additional programming)
* Necrofitz: (additional documentation)
* Gamma / SageOfMirrors: (additional programming)
* Cyb3RGER: (reference for `TWWClient`)
