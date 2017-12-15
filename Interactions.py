# -*- coding: utf-8 -*-

# import
import numpy as np

# constant
COEFF_UP_SPEED = 2
# class


class Interactions(object):
    def __init__(self):
        pass

    def isCollision(self, base1, base2):
        """
        throw True if there is a collision between 2 objects of class Base
        """
        # diffX is distance between player along X
        diffX = base1.getX() - base2.getX()
        # diffY is distance between player along Y
        diffY = base1.getY() - base2.getY()
        # distance is real desitance between center of objects
        distance = np.sqrt(diffX**2 + diffY**2)
        if distance < (base1.size)/2 + (base2.size)/2:
            b = True
        else:
            b = False
        return b

    def ballSpeedAfterCollision(self, base, player):
        """
        compute the new speed of the ball after a collision with a player
        """
        normalizationDistance = base.getSize()/2 + player.getSize()/2
        coeffSpeedX = (base.getX() - player.getX()) / normalizationDistance
        coeffSpeedY = (base.getY() - player.getY()) / normalizationDistance
        playerXSpeed, playerYSpeed = player.getSpeed()
        ballXSpeed, ballYSpeed = base.getSpeed()
        energy = self.computeEnergy(playerXSpeed, playerYSpeed) + \
            self.computeEnergy(ballXSpeed, ballYSpeed)
        ballXSpeed = energy*coeffSpeedX
        ballYSpeed = COEFF_UP_SPEED*energy*coeffSpeedY
        base.setSpeed(ballXSpeed, ballYSpeed)
        if base.debug:
            print("ballspeed aft. coll.: {} {}".format(ballXSpeed, ballYSpeed))

    def computeEnergy(self, baseSpeedX, baseSpeedY):
        """
        compute the energy of an object based on it's speed
        """
        energy = np.sqrt(baseSpeedX**2 + baseSpeedY**2)
        return energy
