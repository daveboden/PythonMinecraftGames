# PythonMinecraftGames

You can play games in this repository on Minecraft Pi or on Minecraft PC using the RaspberryJam Forge mod or on a Spigot server with the RaspberryJuice (e.g. https://github.com/daveboden/raspberryjuice).

# Games

## Hide N Seek

hidenseek.py gets the player to use the Debug F3 screen block coordinates to try and find and mine a hidden diamond block.
First get the X (East / West) and Z (North / South) coordinates right then look down and get the Y-coordinate sorted out to find the block.

# Run without a server with RaspberryJam mod

## Install Forge for Minecraft

A plugin framework for Minecraft.

Installer available here: https://files.minecraftforge.net/

## Install Raspberry Jam mod

This makes your PC Minecraft listen on TCP port 4711 for incoming commands, allowing you to ask where the player is located or set blocks inside your Minecraft session.

Installer available here: https://github.com/arpruss/raspberryjammod/releases

## Run Python script

Lots of options; I use PyCharm Community Edition: https://www.jetbrains.com/pycharm/
