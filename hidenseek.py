# A hide n seek game to help learn about 3d coordinates

### IMPORTANT ###
# Issue this command in the Minecraft console if you're on the PC version:
# setworldspawn 0 0 0
# This makes the coordinates on the debug F3 screen match up with
# what's being reported to the Python interface.

import mcpi.minecraft as minecraft
import mcpi.block as block
from mcpi.connection import RequestError
from mcpi.vec3 import Vec3
import time
from random import randint, randrange
from time import sleep

mc = minecraft.Minecraft.create(address="localhost")
try:
    pos = mc.player.getTilePos()
except RequestError:
    print("Error: Can't find a player to work with. Are you in the Minecraft world?")
    exit(2)

#Pick a spot between 50 and 100 blocks away in the x and z directions
#can be either positive or negative
offsetX = randint(50, 100) * randrange(-1, 2, 2) #Generates either -1 or 1
offsetZ = randint(50, 100) * randrange(-1, 2, 2) #Generates either -1 or 1

hideX = pos.x + offsetX
hideZ = pos.z + offsetZ

print("Finding a y-coordinate at candidate x=%d, z=%d" % (hideX, hideZ))

#Find the surface level at that location.
#Cover between 255 and -255 as a y-coordinate due to the world spawn point
#could be anywhere between 0 and 255 y-coordinate.

columnBlockData = mc.getBlocks(hideX, 255, hideZ, hideX, -255, hideZ)

#We get Air(0) returned for blocks that don't exist and the highest blocks are at the end of the array
assert len(columnBlockData) == 511

#Start at the top of the world and work down until you meet
#the ground (or water or leaves)
for candidateYArray in range(len(columnBlockData) - 1, 0, -1):
    if(columnBlockData[candidateYArray] != block.AIR.id):
        candidateY = candidateYArray - 255
        break

        # Here's the more chatty way to do it; asking the value of each block
        # for candidateY in range(255, -255, -1):
        #     if (mc.getBlock(hideX, candidateY, hideZ) != block.AIR):
        #         break

assert candidateY != None #We should have got a candidate value

if candidateYArray <= 5:
    print("Please try again to find a better hiding place away from the lowest possible y-coordinate")
    exit(1)

if block.BEDROCK.id in columnBlockData[candidateYArray-5:candidateYArray]:
    print("Please try again to find a better hiding place away from the bedrock")
    exit(1)

hideY = candidateY - 5

#Create a 3 by 3 cube of gold blocks
mc.setBlocks(hideX - 1, hideY - 1, hideZ - 1, hideX + 1, hideY + 1, hideZ + 1, block.GOLD_BLOCK)
#Make the centre a diamond block. Mine this to stop the countdown and win.
mc.setBlock(hideX, hideY, hideZ, block.DIAMOND_BLOCK)

gameTimeSeconds = 100
startTimeSeconds = time.time()

displayUpdatedForTime = None

ticks = 0

while True:
    elapsedTimeSeconds = time.time() - startTimeSeconds
    timeLeftSeconds = gameTimeSeconds - elapsedTimeSeconds
    timeLeftSecondsRounded = int(timeLeftSeconds) + 1
    if timeLeftSeconds < 0:
        mc.postToChat("You lost!!")
        mc.setBlock(mc.player.getTilePos() + (Vec3(0, 1, 0)), block.LAVA_FLOWING)
        break #Break out of loop if time is up
    if mc.getBlock(hideX, hideY, hideZ) != block.DIAMOND_BLOCK.id:
        winningMessage = "Well done; you mined the diamond!"
        winningMessage2 = "You've earned %d points" % timeLeftSecondsRounded
        mc.postToChat(winningMessage)
        mc.postToChat(winningMessage2)
        print(winningMessage)
        print(winningMessage2)
        break #Break out of loop if the block has been found and mined
    if timeLeftSecondsRounded % 10 == 0 and displayUpdatedForTime != timeLeftSecondsRounded:
        displayUpdatedForTime = timeLeftSecondsRounded
        print("%d seconds left" % timeLeftSecondsRounded)

    #Sleep for a short while to avoid this being a tight loop
    sleep(0.4)

    if ticks % 5 == 0:
        userposition = mc.player.getTilePos()
        mc.postToChat("%d seconds left" % timeLeftSecondsRounded)
        blockMessage =   "Block at : %4d, %4d, %4d" % (hideX, hideY, hideZ)
        userPosMessage = "You're at: %4d, %4d, %4d" % (userposition.x, userposition.y, userposition.z)
        mc.postToChat(blockMessage)
        mc.postToChat(userPosMessage)
        print(blockMessage)
        print(userPosMessage)

    ticks += 1