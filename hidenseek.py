# A hide n seek game to help learn about 3d coordinates

### IMPORTANT ###
# Issue this command in the Minecraft console:
# setworldspawn 0 0 0
# This makes the coordinates on the debug F3 screen match up with
# what's being reported to the Python interface.

import mcpi.minecraft as minecraft
import mcpi.block as block
from mcpi.vec3 import Vec3
import time
from random import randint, randrange
from time import sleep

mc = minecraft.Minecraft.create(address="localhost")
pos = mc.player.getTilePos()

#Pick a spot between 50 and 100 blocks away in the x and z directions
#can be either positive or negative
offsetX = randint(50, 100) * randrange(-1, 2, 2) #Generates either -1 or 1
offsetZ = randint(50, 100) * randrange(-1, 2, 2) #Generates either -1 or 1

hideX = pos.x + offsetX
hideZ = pos.z + offsetZ

#Find the surface level at that location.

#Start at the top of the world and work down until you meet
#the ground (or water or leaves)
for candidateY in range(255, 0, -1):
    if(mc.getBlock(hideX, candidateY, hideZ) != block.AIR):
        break

if candidateY < 10:
    print("Please try again to find a better hiding place away from the bedrock")
    exit(1)

hideY = candidateY - 5

#Create a 3 by 3 cube of gold blocks
mc.setBlocks(hideX - 1, hideY - 1, hideZ - 1, hideX + 1, hideY + 1, hideZ + 1, block.GOLD_BLOCK)
#Make the centre a diamond block. Mine this to stop the countdown and win.
mc.setBlock(hideX, hideY, hideZ, block.DIAMOND_BLOCK)

positionMessage = str(hideX) + ", " + str(hideY) + ", " + str(hideZ)
message = "Block is hiding at " + positionMessage
mc.postToChat(message)
print message

gameTimeSeconds = 120
startTimeSeconds = time.time()

displayUpdatedForTime = None

while True:
    elapsedTimeSeconds = time.time() - startTimeSeconds
    timeLeftSeconds = gameTimeSeconds - elapsedTimeSeconds
    timeLeftSecondsRounded = int(timeLeftSeconds) + 1
    if timeLeftSeconds < 0:
        mc.postToChat("You lost!!")
        mc.setBlock(mc.player.getTilePos() + (Vec3(0, 1, 0)), block.LAVA_FLOWING)
        break #Break out of loop if time is up
    if mc.getBlock(hideX, hideY, hideZ) != block.DIAMOND_BLOCK.id:
        mc.postToChat("Well done; you mined the diamond!")
        break #Break out of loop if the block has been found and mined
    if timeLeftSecondsRounded % 10 == 0 and displayUpdatedForTime != timeLeftSecondsRounded:
        #Post an update on chat every 10 seconds
        displayUpdatedForTime = timeLeftSecondsRounded
        mc.postToChat(str(timeLeftSecondsRounded) + " seconds left to find block at " + positionMessage)
    #Sleep for a short while to avoid this being a tight loop
    sleep(0.1)

