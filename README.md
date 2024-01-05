# The Great Relocation

A 2D tiled-based game made with **Python**, [Arcade](https://api.arcade.academy/en/latest/) and [Tiled](https://www.mapeditor.org/).

## How to install

To run the game you need **Python** installed in your system, and that system really should be a Linux based one. Clone this project:

    https://github.com/fran-00/groi_2D.git
    cd groi_2D

Create a new virtual environment with **pyenv** (Python <= 3.11 should be fine) and activate it:

    python install 3.11.4
    pyenv virtualenv 3.11.4 relocation
    pyenv activate relocation

Install project requirements:

    pip install -r requirements.txt

Run the game:

    python launcher.py

## Known Issues

Currently you can't run it with Python 3.12: Pillow 9.3.0 does not support it and **Arcade** requires that specific version. If you are on Windows with Python 3.12 installed in your system you should use **pyenv** (with WSL) or **conda** instead. This probably will change when Arcade will be updated.

## TODO List

- [x] Player must stand in the center of the viewport.
- [x] Add a temporary inventory and health bar
- [x] When left mouse button is pressed character shoots bullets.
- [x] Add a custom combat sprite when character shoots bullets.
- [x] Enemies appear when the character passes over a tile that triggers their spawining.
- [ ] Other enemies are already present on the map and start chasing the character if they're at a distance that depends on enemy type.
- [ ] Add melee weapon implementation.
- [ ] Add minimap at the top right of the viewport.
- [ ] Add Main Menu to start and load game.
- [ ] Add a GUI with inventory, health, mana, quests...
- [ ] Move both with WASD and mouse click through a cursor. (Or maybe not)
- [ ] If you point with cursor at an enemy instead of moving you shoot at it.
- [ ] Window resizing does NOT scale the resolution but enlarges the portion of the visible map. (Or maybe not)
- [ ] Grab items with mouse click (and/or pressing a key like E) and not hovering over them like now.
- [ ] Add particle effects when a bullet hits a target or a wall.
- [ ] Add sounds and music.
- [ ] Collectible objects are created directly in the map and program reads their characteristics.
- [ ] Enemies pursue the player in paths that depend on the type of enemy: some are faster and more dangerous than others.
- [ ] Add the ability to enter indoor locations (caves, buildings, etc.) When player enters an indoor location, they're teleported to the point on the map indicated by specific coordinates when they passes through the entrance.
- [ ] Each type of ranged weapon has a different sprite for the bullets it produces.
- [ ] Bullets must be removed from sprite list after traveling a certain distance (presumably when they exit the viewport), otherwise their path will never stop being calculated, consuming resources unnecessarily.
- [ ] Add different sprites when characters take damage and when they attack melee or ranged.
- [ ] Fix an issue where enemies stop chasing the player when they are too close to a wall. It is likely due to an error in calculating the size of the grid during AStarBarrierList class initialization.
