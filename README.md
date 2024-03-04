# The Wind Waker Archipelago

The Wind Waker Archipelago modifies the base randomizer created by LagoLunatic to work with Archipelago multiworlds.
Dev5ter started the original project and has been maintained by the community since.

## Installation & Usage
See the [setup guide](https://github.com/tanjo3/tww_apworld/blob/master/docs/setup_en.md) for instructions.

## How does The Wind Waker get randomized?
Items get shuffled between the different locations in the game, so each playthrough is unique. Randomized locations
include chests, items received from NPC, and treasure salvaged from the ocean floor. The randomizer also includes
quality-of-life features such as a fully opened world, removing many cutscenes, increased sailing speed, and more.

In the project's current state, in-game item models are not yet implemented. Instead, all items in the game will be
either a green or red rupee. For locations that are currently supported, you'll find a green rupee. Otherwise, you'll
get a red rupee. This is a temporary measure until item models are implemented. You'll receive the actual item for that
location from the Archipelago server.

## Which locations get shuffled?
All randomizable locations will have their items shuffled each seed. However, the randomizer is designed so that only
certain groups of locations can contain progression items. The remaining locations will only contain items unnecessary
to beat the game, such as rupees or Heart Pieces.

This project is still a work in progress, and many locations still need to be supported. Refer to the settings YAML
(found in the TWW apworld download) for more details about the randomization options and which locations are currently
supported.

## What is the goal of The Wind Waker?
Reach and defeat Ganondorf atop Ganon's Tower. This will require all eight shards of the Triforce of Courage, the
fully-powered Master Sword (unless it's swordless mode), Light Arrows, and any other items necessary to reach Ganondorf.

## I need help! What do I do?
Refer to the [FAQ](https://lagolunatic.github.io/wwrando/faq/) first. If you are still stuck, please ask in the Wind
Waker thread (under `future-game-design`) in the Archipelago server.

## Known issues
* When there are more progression items than progression locations, the randomizer will fail with a `FillError`. In this
case, you should put more locations into logic to ensure there are enough progression locations to place progression
items.
* When randomizing with different key shuffle options, generation may fail. Try again several times, and if it still
fails, try a different key shuffle option.

Feel free to report any other issues in the Wind Waker thread in the Archipelago server! I'll take a look and see what I
can do. Suggestions for improvements are also welcome.

## Planned Features
* Support more locations
* More robust logic for entrance randomization
* Support for remaining randomization options (such as required bosses mode)
* In-game item models

## Running from source
* Clone this repository into the `worlds` folder for your Archipelago source.
* Install `py_dolphin_memory_engine` via pip:
    - ``pip install dolphin-memory-engine``

## Credits
This randomizer would not be possible without the help from:
* LagoLunatic: (base randomizer)
* Dev5ter: (initial TWW AP implmentation)
* CrainWWR: (multiworld and Dolphin memory assistance)
* Celeste (Tia): (logic and typo fixes, additional programming)
* DaemonHunter: (additional programming)
* Ouro: (tracker support)
* Necrofitz: (additional documentation)
* Gamma / SageOfMirrors: (additional programming)
* Cyb3RGER: (reference for `TWWClient`)
