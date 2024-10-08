# Horology

A 2D tiled-based game made with **Python**, [Arcade](https://api.arcade.academy/en/latest/) and [Tiled](https://www.mapeditor.org/).

## How to install

To run the game you need **Python** installed in your system, and that system really should be a Linux based one. Clone this project:

```shell
git clone https://github.com/fran-00/horology.git
cd horology
```

Create a new virtual environment with **pyenv** (Python <= 3.11 should be fine) and activate it:

```shell
python install 3.11.4
pyenv virtualenv 3.11.4 horology
pyenv activate horology
```

Install project requirements:

```shell
pip install -r requirements.txt
```

Run the game:
```shell
python -m game
```

## TODO List

- [x] Player must stand in the center of the viewport.
- [x] Add a temporary inventory and health bar
- [x] When left mouse button is pressed character shoots bullets.
- [x] Add a custom combat sprite when character shoots bullets.
- [x] Enemies appear when the character passes over a tile that triggers their spawining.
- [x] Move only with WASD. Click left mouse button to attack with a melee weapon, click right mouse button to attack with a "bullet".
- [x] Add melee weapon implementation.
- [ ] Add different sprites when characters take damage and when they attack melee or ranged.
- [ ] Add equipped weapon sprite to player's sprite when attacking.
- [ ] Update sprite loading system to parse tilesets instead of a single file per frame. (Done for bullets, work in progress for player and enemies).
- [x] Add a HUD with equipped weapons, health and weapon selection.
- [ ] Add a way to open the inventory showing a pop up modal pressing I key.
- [ ] Add enemies already present on the map that start chasing the character if they're at a distance that depends on enemy type.
- [ ] Add minimap at the top right of the viewport.
- [x] Add Main Menu to start a new game and open settings.
- [ ] Add game settings (change resolution, difficulty...)
- [ ] Window resizing does NOT scale the resolution but enlarges the portion of the visible map.
- [x] Grab collectible items by pressing E key.
- [ ] Add particle effects when a bullet hits a target or a wall.
- [ ] Add sounds and music.
- [ ] Add random npc spawning and following paths.
- [x] Collectible objects are created directly in the map and program reads their characteristics.
- [ ] Enemies pursue the player in paths that depend on the type of enemy: some are faster and more dangerous than others.
- [ ] Add the ability to enter indoor locations (caves, buildings, etc.) When player goes to a certain tile (like a door) they're teleported to another map.
- [x] Each type of ranged weapon has a different sprite for the bullets it produces.
- [ ] Bullets must be removed from sprite list after traveling a certain distance (presumably when they exit the viewport), otherwise their path will never stop being calculated, consuming resources unnecessarily.

## Known Issues

- [ ] Fix an issue where enemies stop chasing the player when they are too close to a wall. It seems to fail in path calculation because it doesn't use the enemy's hitbox to calculate the collision but the center of their sprite instead.
- [X] After moving the settings access from the game menu to the start menu, they pop up randomly when shooting with a ranged weapon. UPDATE: Fixed, on_hide_view method of MainMenuView was missing and was causing buttons to remain invisible during game.

## Notes

Currently you can't run it with Python 3.12: Pillow 9.3.0 does not support it and **Arcade** requires that specific version. If you are on Windows with Python 3.12 installed in your system you should use **pyenv** (with WSL) or **conda** instead. This probably will change when Arcade will be updated.
