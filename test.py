# -*- coding: utf-8 -*-

import Elements
import Interactions
import Controller
import Game
import Bot
import unittest


class TestElements(unittest.TestCase):

    def reset(self):
        self.base = Elements.Base()
        self.base.setSpeed(0, 0)
        self.base.setPosition(100, 100)

        self.player = Elements.Player()
        self.player.setSpeed(0, 0)
        self.player.setPosition(200, 200)

    def testGravity(self):
        self.reset()
        value1 = self.base._applyGravity()
        self.base.setPosition(100, Elements.WINDOW_SIZE[-1] - self.base.size/2)
        value2 = self.base._applyGravity()
        self.assertTrue(value1)
        self.assertFalse(value2)

    def testSpeedUpdate(self):
        self.reset()
        self.base.setSpeed(1, 0)
        self.base._speedUpdate()
        self.assertEqual(self.base.ySpeed, 5)
        self.assertEqual(self.base.xSpeed, 0.5)

    def testRebondY(self):
        self.reset()
        self.base.setSpeed(0, 0.5*self.base.size + 1)
        self.base.rebondY()
        expectedSpeed = -(0.5*self.base.size + 1)*Elements.COEF_REBOND
        self.assertEqual(self.base.ySpeed, expectedSpeed)

    def testRebondX(self):
        self.reset()
        self.base.setSpeed(1, 0)
        self.base.rebondX()
        expectedSpeed = -Elements.COEF_REBOND
        self.assertEqual(self.base.xSpeed, expectedSpeed)

    def testUpdateXYPosition(self):
        self.reset()
        self.base.setSpeed(10, 10)
        self.base.updateXYPosition()
        self.assertEqual((self.base.x, self.base.y), (110, 110))

    def testMoveLeft(self):
        self.reset()
        self.player.moveLeft()
        self.assertEqual(self.player.xSpeed, -Elements.SPEED_INCREASE)

    def testMoveRight(self):
        self.reset()
        self.player.moveRight()
        self.assertEqual(self.player.xSpeed, Elements.SPEED_INCREASE)

    def testJump(self):
        self.reset()
        self.player.jump()
        self.assertEqual(self.player.ySpeed, Elements.JUMP_HEIGHT)

    def testScore(self):
        self.reset()
        self.player.scores()
        self.assertEqual(self.player.score, 1)


class TestInteractions(unittest.TestCase):

    def reset(self):
        self.ball = Elements.Base()
        self.player1 = Elements.Player()
        self.player2 = Elements.Player()
        self.inter = Interactions.Interactions()
        self.cage = Elements.Box(20, 20, (100, 100))

    def testCollision(self):
        self.reset()
        self.player1.setPosition(500, 500)
        self.player2.setPosition(426, 500)
        value = self.inter.isCollision(self.player1, self.player2)
        self.assertTrue(value)

    def testBallSpeedAfterCollision(self):
        self.reset()
        self.player1.setPosition(500, 500)
        self.ball.setPosition(460, 500)
        self.player1.setSpeed(10, 10)
        self.inter.ballSpeedAfterCollision(self.ball, self.player1)
        self.assertAlmostEqual(self.ball.xSpeed, -12.6, 0)
        self.assertEqual(self.ball.ySpeed, 0.0)

    def testBallintoCage(self):
        self.reset()
        self.ball.setPosition(110, 110)
        value = self.inter.isBallintoCage(self.cage, self.ball)
        self.assertTrue(value)

    def testCollisionWithBox(self):
        self.reset()
        self.ball.setPosition(105, 105)
        self.ball.setSpeed(5, 5)
        self.inter.collisionWithBox(self.cage, self.ball)
        self.assertEqual((self.ball.x, self.ball.y), (105, 75))


class TestGame(unittest.TestCase):

    def reset(self):
        self.game = Game.Game()

    def testSelectPlayerStatus(self):
        self.reset()
        self.game.selectPlayerStatus(Elements.PLAYER, Elements.PLAYER)
        self.assertEqual(self.game.player1.status, Elements.PLAYER)
        self.assertEqual(self.game.player2.status, Elements.PLAYER)

    def testSetGame(self):
        self.reset()
        self.game.player1.setPosition(100, 100)
        self.game.setGame()
        self.assertEqual((self.game.player1.x, self.game.player1.y), (0, 0))

    def testGetScore(self):
        self.reset()
        self.game.player1.scores()
        self.game.player2.scores()
        score1, score2 = self.game.getScore()
        self.assertEqual(score1, 1)
        self.assertEqual(score2, 1)


class TestController(unittest.TestCase):

    def testIsAI(self):
        c = Controller.Controller()
        value = c.isAI(0)
        self.assertTrue(value)

    def testupdateTime(self):
        c = Controller.Controller()
        c.updateTime()
        self.assertEqual(c.time, 60)

    def testConvertTime(self):
        c = Controller.Controller()
        time = 50000
        cTime = c.convertTime(time)
        self.assertEqual(cTime, "00:50:00")

    def testSetGameType(self):
        c = Controller.Controller()
        c.game.gamemode = Game.GAME_MODES[1]
        self.assertEqual(c.game.gamemode, Game.GAME_MODES[1])
        c.setGameType(0)
        self.assertEqual(c.game.gamemode, Game.GAME_MODES[0])


class TestBot(unittest.TestCase):

    def testGiveDirections(self):
        self.game = Game.Game()
        self.player = self.game.player1
        self.bot = Bot.Bot(self.game, self.player)
        self.bot.botPos = (500, 500)
        self.bot.ballPos = (800, 200)
        directionList1 = self.bot.giveDirections()
        for element in directionList1:
            self.assertIn(element, [Bot.JUMP, Bot.RIGHT])


if __name__ == "__main__":
    unittest.main()
