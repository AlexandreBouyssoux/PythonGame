# -*- coding: utf-8 -*-

# import
import numpy as np

# constant
SPEED_ATTENUATION = 0.5

# class


class Interactions(object):
    def __init__(self):
        pass

    def isCollision(base1, base2):
        """
        throw True if there is a collision between 2 objects of class Base
        """
        # diffX is distance between player along X
        diffX = base1.getX() - base2.getX()
        # diffY is distance between player along Y
        diffY = base1.getY() - base2.getY()
        # distance is real desitance between center of objects
        distance = np.sqrt(diffX**2 + diffY**2)
        if distance < base1.size() + base2.size():
            b = True
        else:
            b = False
        return b

    def ballSpeedAfterCollision(base, player):
        """
        calculate the new speed of the ball after a collision with a player
        """
        normalizationDistance = base.getSize() + player.getSize()
        coeffSpeedX = abs(base.getX() - player.getX()) / normalizationDistance
        coeffSpeedY = abs(base.getY() - player.getY()) / normalizationDistance
        playerXSpeed, playerYSpeed = player.getSpeed()
        ballXSpeed = -SPEED_ATTENUATION*base.getSpeed()[0] + \
            playerXSpeed*coeffSpeedX
        ballYSpeed = -SPEED_ATTENUATION*base.getSpeed()[1] + \
            playerYSpeed*coeffSpeedY
        base.setSpeed(ballXSpeed, ballYSpeed)