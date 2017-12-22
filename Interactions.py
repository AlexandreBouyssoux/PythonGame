# -*- coding: utf-8 -*-

# import
import numpy as np

# constant
COEFF_UP_SPEED = 2
PLAYER_BOUNCING_BACK = -0.5
# class


class Interactions(object):
    def __init__(self):
        pass

    def isCollision(self, base1, base2, verbose=0):
        """
        throw True if there is a collision between 2 objects of class Base
        """
        # diffX is distance between player along X
        diffX = base1.getX() - base2.getX()
        # diffY is distance between player along Y
        diffY = base1.getY() - base2.getY()
        # distance is real desitance between center of objects
        distance = np.sqrt(diffX**2 + diffY**2)
        # distance threshold : we take different bounding boxes for the ball
        if type(base1) == type(base2):
            distanceThreshold = base1.size/2 + base2.size/2 + 5
        else:
            distanceThreshold = 3*base1.size/4 + 3*base2.size/4
        if distance < distanceThreshold:
            if verbose > 0:
                print("distance: {} | Base1size: {} | Base2size: {}".format(
                        distance, base1.size, base2.size))
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

    def playerBehaviorAfterCollision(self, player1, player2):
        """
        prevent the collision between two differnt players
        """
        player1.x -= player1.xSpeed
        player1.y -= player1.ySpeed
        player2.x -= player2.xSpeed
        player2.y -= player2.ySpeed
        player1.xSpeed *= PLAYER_BOUNCING_BACK
        player1.ySpeed *= PLAYER_BOUNCING_BACK
        player2.xSpeed *= PLAYER_BOUNCING_BACK
        player2.ySpeed *= PLAYER_BOUNCING_BACK

    def isBallintoCage(self, cage, ball):
        xMin = cage.upRightCorner[0]
        xMax = xMin + cage.w
        yMin = cage.upRightCorner[1]
        yMax = yMin + cage.h
        collision = False
        x = ball.getX()
        y = ball.getY()
        if x >= xMin and x <= xMax and y >= yMin and y <= yMax:
            collision = True
        return collision

    def isCollisionWithBox(self, box, base):
        pass

    def baseBehaviorAfterBoxCollision(self, box, base):
        pass
