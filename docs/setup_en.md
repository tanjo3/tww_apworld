# Setup Guide for The Wind Waker Archipelago

Welcome to The Wind Waker Archipelago! This guide will help you get started with setting up the randomizer and playing
your first multiworld. Whether you are playing, generating, or hosting an Archipelago room with The Wind Waker, you'll
need to follow a few simple steps to get started.

Unfortunately, Mac OS is not officially supported at this time.

## Requirements

You'll need the following components to be able play/generate with The Wind Waker AP world:
* Install [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.4 or higher.\
    **Make sure to install the Generator if you intend to be generating games.**
* The latest version of the [TWW apworld](https://github.com/tanjo3/tww_apworld/releases/latest).
* Install [Dolphin Emulator](https://dolphin-emu.org/download/).\
    **We recommend using the latest development version.**
* The latest version of the [TWW AP Client](https://github.com/tanjo3/wwrando/releases/latest).
* A The Wind Waker ISO (North American version), probably named "Legend of Zelda, The - The Wind Waker (USA).iso".

If you intend to play under linux, you will need to consider the following information.
* Grab the `tar.gz` version of Archipelago not the `AppImage`. The file name should be similar to following on the
release page: `Archipelago_X.X.X_linux-x86_64.tar.gz`.
* For Dolphin, you can use the flatpak package [available on flathub](https://flathub.org/apps/org.DolphinEmu.dolphin-emu).

## Installation
All users should follow these steps:
1. Unzip the downloaded TWW apworld zip file.
2. Place the `tww.apworld` file in your Archipelago installation's `lib/worlds` folder (windows default to:
`%programdata%/Archipelago`).
3. Place the content of the `lib` folder of the APWorld zip into Archipelago's `lib` folder.

If you're playing The Wind Waker, you'll also need to unzip the TWW AP zip file downloaded from the release page.

## Setting Up a YAML
All players playing The Wind Waker must provide the room host with a YAML file containing the settings for their world.
A sample YAML file for The Wind Waker is provided in the TWW apworld download. Refer to the comments in that file for
details about what each setting does.

Once you're happy with your settings, provide the room host with your YAML file and proceed to the next step.

## Generating a Multiworld
If you're generating a multiworld game that includes The Wind Waker, you'll need to do so locally as The online
generator does not yet support The Wind Waker. Follow these steps to generate a multiworld seed:
1. Gather all player's YAMLs. Place these YAMLs into the `Players` folder of your Archipelago installation. If the
folder does not exist, then it must be created manually. The files here should not be compressed.
2. Modify any local host settings for generation, as desired.
3. Run `ArchipelagoGenerate.exe` (without `.exe` on linux) or click `Generate` in the launcher. The generation output
is placed in the `output` folder (usually named something like `AP_XXXXX.zip`).
    * If entrance randomization is enabled, there is an increased chance that the multiworld will fail to generate.
    Simply try again if this happens, or modify the settings to reduce the chance of failure.
    * Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate,
    you will need the corresponding ROM files. A ROM file is not required for The Wind Waker at this stage.
4. Unzip the `AP_XXXXX.zip` file. It should include a `.aptww` file for each player in the room playing The Wind Waker.
Each file will be named `AP_XXXXX_P#_<name>.aptww`, where `@` corresponds to that player's slot number and `<name>` is
their slot (player) name. Distribute each file to the appropriate player.
5. Delete the distributed `.aptww` files and re-zip the remaining files. Use this archive file in the next section to
host a room, or provide this file to the room host.
    * Note that if you are planning to host the room on a local machine, you can skip this step and instead just use the
    original zip file (`AP_XXXXX.zip`).

## Hosting a Room
If you're generating the multiworld, follow the instructions in the previous section. Once you have the a zip file
corresponding to your multiworld, follow
[these steps](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room.
Follow the instructions for hosting on the website from a locally generated game or on a local machine.

## Connecting to a Room
You should have the `aptww` file provided to you by the multiworld generator. You should also have the room's
server name and port number from the room's host.

Once you do, follow these steps to connect to the room:
1. Run the TWW AP Randomizer. If this is the first time you've opened the randomizer, you'll need to specify the path to
your The Wind Waker ISO and the output folder for the randomized ISO. These will be saved for the next time you open the
client.
2. Modify any cosmetic convenience tweaks and player customization options as desired.
[This repository](https://github.com/Sage-of-Mirrors/Custom-Wind-Waker-Player-Models) contains a collection of custom
player models for The Wind Waker. Follow the installation instructions there to set up custom player models.
3. For the APTWW file, browse and locate the path to the `aptww` you received from the multiworld generator.
4. Click `Randomize` at the bottom. This randomizes the ISO and puts it in the output folder you specified. The file
will be named `TWW AP_XXXXX_P#.iso` where `#` is the slot number. Verify that the slot number corresponds to your
slot number.
5. Open Dolphin and use it to open the randomized ISO. Start a new file and get into the game. You don't technically
need to do this step first, but it's good practice.
6. Start `ArchipelagoLauncher.exe` (without `.exe` on linux) and choose `TWW Client`, which will open the text client.
If Dolphin is not already open, or you have yet to start a new file, you will be prompted to do so.
7. Connect to the room by entering the server name and port number at the top and pressing `Connect`. For rooms hosted
on the website, this will be `archipelago.gg:<port>` where `<port>` is the port number. If a game is being hosted from
the `ArchipelagoServer.exe` (without `.exe` on linux), this will default to `38281` but may be changed in the `host.yaml`.
8. Once connected, you will be prompted to enter your slot name. Note that this is *not* your slot number. Instead, it's
the name of your player slot that you are connecting to. This is the same as the name that was set when creating your
YAML file. If the game is hosted on the website, this is also displayed on the room page. The name is case-sensitive.

## Troubleshooting

* If you are getting an error message, check to ensure that `Enable Emulated Memory Size Override` in Dolphin
(under `Options` > `Configuration` > `Advanced`) is **disabled**.
* If you run with a custom GC boot menu, you'll need to skip it by going to `Options` > `Configuration` > `GameCube`
and checking `Skip Main Menu`.
