#!/usr/bin/env python
import sys
import random
import board

class Agent:
	def __init__(self, ships):
		self.shots = dict()
		self.ships = ships
		self.numberOfShots = 0
		self.hits = 0
		self.miss = 0
		self.totalDamage = self.calculateTotalDamage(ships)
		self.shotList = list()

	def calculateTotalDamage(self, ships):
		total = 0
		for ship in ships:
			total = total + int(ship.dimension)
		return total

def openFire(agent, shot, gameBoard):
	alreadyShot = agent.shots.get(shot, None)
	if alreadyShot == None:
		agent.shotList = agent.shotList + [str(shot[0]) + "," + str(shot[1])]
		shipSunk = False
		shipHit = False
		agent.numberOfShots = int(agent.numberOfShots) + 1
		agent.shots[shot] = "x"
		hasShip = gameBoard.get(shot, None)
		if hasShip != None:
			agent.hits = int(agent.hits) + 1
			shipHit = True
			hasShip.damageCounter = int(hasShip.damageCounter) + 1
			shipSunk = hasShip.isSunk()
		else:
			agent.miss = int(agent.miss) + 1
			shipHit = False
		return [shipHit, shipSunk]
	else:
		return [False, False]

def huntMode(agent, target, gameBoard):
	boardSize = 10
	shipDestroyed = False
	initialTarget = target
	left = True
	right = True
	up = True
	down = True
	attempt = 0
	while not shipDestroyed:
		attempt = attempt + 1
		if target[0] + 1 < boardSize and down:
			target = (target[0] + 1, target[1])
			[down, shipDestroyed] = openFire(agent, target, gameBoard)
			if not down:
				target = initialTarget
			if down:
				left = False
				right = False

		elif target[0] - 1 >= 0 and up:
			target = (target[0] - 1, target[1])
			[up, shipDestroyed] = openFire(agent, target, gameBoard)
			if not up:
				target = initialTarget
			if up:
				left = False
				right = False

		elif target[1] + 1 < boardSize and right:
			target = (target[0], target[1] + 1)
			[right, shipDestroyed] = openFire(agent, target, gameBoard)
			if not right:
				target = initialTarget
			if right:
				up = False
				down = False

		elif target[1] - 1 >= 0 and left:
			target = (target[0], target[1] - 1)
			[left, shipDestroyed] = openFire(agent, target, gameBoard)
			if not left:
				target = initialTarget
			if left:
				up = False
				down = False

		if not up and not down and not left and not right:
			return True

		if attempt == 100:
			return True 

		if shipDestroyed:
			return True

def startGame(agent, gameBoard, ships):
	boardSize = 10
	hasGameEnded = False
	while not hasGameEnded:
		shot_x = int(random.randint(0, boardSize - 1))		
		shot_y = int(random.randint(0, boardSize - 1))
		target = (shot_x, shot_y)
		shot = agent.shots.get(target, None)
		if shot == None:
			agent.shotList = agent.shotList + [str(target[0]) + "," + str(target[1])]
			agent.shots[target] = "x"
			agent.numberOfShots = int(agent.numberOfShots) + 1
			hasShip = gameBoard.get(target, None)
			if hasShip != None:
				agent.hits = int(agent.hits) + 1
				hasShip.damageCounter = int(hasShip.damageCounter) + 1
				if not hasShip.isSunk(): # submarines only take one shot, so theres no need for hunt mode if theyre hit
					huntMode(agent, target, gameBoard)
			else:
				agent.miss = int(agent.miss) + 1
			if int(agent.hits) == int(agent.totalDamage):
				hasGameEnded = True

def main():
	[gameBoard, ships, buildTime] = board.buildGame()
	agent = Agent(ships)
	startGame(agent, gameBoard, ships)
	#board.printAgentStatistics(agent)
	#board.printData(gameBoard)
	return [agent, gameBoard]

if __name__ == '__main__':
	main()
