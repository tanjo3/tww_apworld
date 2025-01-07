# The Wind Waker Archipelago

The Wind Waker Archipelago modifies the base randomizer created by LagoLunatic to work with Archipelago multiworlds.
Dev5ter started the original project, which the community has maintained since then.

## Installation & Usage

See the [setup guide](https://github.com/tanjo3/tww_apworld/blob/master/docs/setup_en.md) for instructions.

## How does The Wind Waker get randomized?

Items get shuffled between the different locations in the game, so each playthrough is unique. Randomized locations
include chests, items received from NPC, and treasure salvaged from the ocean floor. The randomizer also includes
quality-of-life features such as a fully opened world, removing many cutscenes, increased sailing speed, and more.

## Which locations get shuffled?

Only locations put into logic by the world's settings will be randomized. The remaining locations in the game will have
a yellow Rupee, which includes a message that the location is not randomized.

## What is the goal of The Wind Waker?

Reach and defeat Ganondorf atop Ganon's Tower. This will require all eight shards of the Triforce of Courage, the
fully-powered Master Sword (unless it's swordless mode), Light Arrows, and any other items necessary to reach Ganondorf.

## I need help! What do I do?

Refer to the [FAQ](https://lagolunatic.github.io/wwrando/faq/) first. Then, try the
[troubleshooting](https://github.com/tanjo3/tww_apworld/blob/master/docs/setup_en.md#troubleshooting) steps in the setup
guide. If you are still stuck, please ask in the Wind Waker thread (under `future-game-design`) in the Archipelago
server.

## Known issues

- Randomized freestanding rupees, spoils, and bait will also be given to the player picking up the item. The item will
  be sent properly, but the collecting player will receive an extra copy.
- Demo items (items which are held over Link's head) which are **not** randomized, such as rupees from salvages from
  random light rings or rewards from minigames, will not work.
- Item get messages for progressive items received on locations that send earlier than intended will be incorrect. This
  does not affect gameplay.
- The Heart Piece count in item get messages will be off by one. This does not affect gameplay.
- It has been reported that item links can be buggy. Nothing game-breaking, but do be aware of it.

Feel free to report any other issues in the Wind Waker thread in the Archipelago server! I'll take a look and see what I
can do. Suggestions for improvements are also welcome.

## Planned Features

- Dynamic CTMC based on enabled options
- Hint implementation from base randomizer (hint placement options and hint types)
- Integration with Archipelago's hint system (e.g., auction hints)
- EnergyLink support
- Swift Sail logic as an option
- Continued bugfixes

## Running from source

### Installing Git

Download and install git from here: https://git-scm.com/downloads  
Then clone this repository with git by running this in a command prompt:

```
git clone https://github.com/tanjo3/tww_apworld.git
```

### Installing Python

You will need to install Python 3.12. We recommend using `pyenv` to manage different Python versions:

- For Windows, install `pyenv-win` by following
  [these steps](https://github.com/pyenv-win/pyenv-win?tab=readme-ov-file#quick-start).
- For Linux, follow the instructions [here](https://github.com/pyenv/pyenv?tab=readme-ov-file#automatic-installer) to
  install `pyenv` and then follow the instructions
  [here](https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv) to set up your shell
  environment.

After installing `pyenv`, install and switch to Python 3.12 by running:

```sh
pyenv install 3.12
pyenv global 3.12
```

## Credits

This randomizer would not be possible without the help from:

- Celeste (Maëlle): (logic and typo fixes, additional programming)
- CrainWWR: (multiworld and Dolphin memory assistance, additional programming)
- Cyb3R: (reference for `TWWClient`)
- DeamonHunter: (additional programming)
- Dev5ter: (initial TWW AP implmentation)
- Gamma / SageOfMirrors: (additional programming)
- LagoLunatic: (base randomizer, additional assistance)
- Lunix: (Linux support, additional programming)
- Mysteryem: (tracker support, additional programming)
- Necrofitz: (additional documentation)
- Ouro: (tracker support)
- Tubamann: (additional programming)
