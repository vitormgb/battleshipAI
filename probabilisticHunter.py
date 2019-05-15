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

def buildProbabilisticBoard(boardSize):
	probabilisticBoard = dict()
	for i in range(boardSize):
		for j in range(boardSize):
			key = (i,j)
			probabilisticBoard[key] = 1/float(boardSize*boardSize)
	return probabilisticBoard

def mostLikelyPosition(probabilisticBoard, agent):
	firePosition = None
	for key in probabilisticBoard.keys():
		alreadyShot = agent.shots.get(key, None)
		if alreadyShot == None and firePosition == None and probabilisticBoard[key] != 0 and probabilisticBoard[key] != 1:
			firePosition = key
		if firePosition != None:
			if probabilisticBoard[key] > probabilisticBoard[firePosition] and probabilisticBoard[key] != 1 and probabilisticBoard[key] != 0:
				firePosition = key
	return firePosition

def updateRemainingProbabilities(probabilisticBoard, numberOfShots, boardSize):
	for key in probabilisticBoard.keys():
		if probabilisticBoard[key] != 0 and probabilisticBoard[key] != 1:
			probabilisticBoard[key] = probabilisticBoard[key] + 1/float(boardSize*boardSize - numberOfShots)
			if probabilisticBoard[key] >= 1:
				probabilisticBoard[key] = 0.99
	return probabilisticBoard


def updateProbabilisticBoard(ship, probabilisticBoard, firePosition, numberOfShots, boardSize):
	if ship != None:
		probabilisticBoard[firePosition] = 1
		if firePosition[0] + 1 < boardSize and probabilisticBoard[(firePosition[0] + 1, firePosition[1])] != 0 and probabilisticBoard[(firePosition[0] + 1, firePosition[1])] != 1:
			probabilisticBoard[(firePosition[0] + 1, firePosition[1])] = round(probabilisticBoard[(firePosition[0] + 1, firePosition[1])] + 1/float(boardSize*boardSize - numberOfShots),2)
			if probabilisticBoard[(firePosition[0] + 1, firePosition[1])] >= 1:
				probabilisticBoard[(firePosition[0] + 1, firePosition[1])] = 0.99
		
		if firePosition[0] - 1 >= 0 and probabilisticBoard[(firePosition[0] - 1, firePosition[1])] != 0 and probabilisticBoard[(firePosition[0] - 1, firePosition[1])] != 1:
			probabilisticBoard[(firePosition[0] - 1, firePosition[1])] = round(probabilisticBoard[(firePosition[0] - 1, firePosition[1])] + 1/float(boardSize*boardSize - numberOfShots),2)
			if probabilisticBoard[(firePosition[0] - 1, firePosition[1])] >= 1:
				probabilisticBoard[(firePosition[0] - 1, firePosition[1])] = 0.99

		if firePosition[1] + 1 < boardSize and probabilisticBoard[(firePosition[0], firePosition[1] + 1)] != 0 and probabilisticBoard[(firePosition[0], firePosition[1] + 1)] != 1:
			probabilisticBoard[(firePosition[0], firePosition[1] + 1)] = round(probabilisticBoard[(firePosition[0], firePosition[1] + 1)] + 1/float(boardSize*boardSize - numberOfShots),2)
			if probabilisticBoard[(firePosition[0], firePosition[1] + 1)] >= 1:
				probabilisticBoard[(firePosition[0], firePosition[1] + 1)] = 0.99

		if firePosition[1] - 1 >= 0 and probabilisticBoard[(firePosition[0], firePosition[1] - 1)] != 0 and probabilisticBoard[(firePosition[0], firePosition[1] - 1)] != 1:
			probabilisticBoard[(firePosition[0], firePosition[1] - 1)] = round(probabilisticBoard[(firePosition[0], firePosition[1] - 1)] + 1/float(boardSize*boardSize - numberOfShots),2)
			if probabilisticBoard[(firePosition[0], firePosition[1] - 1)] >= 1:
				probabilisticBoard[(firePosition[0], firePosition[1] - 1)] = 0.99
	else:
		probabilisticBoard[firePosition] = 0
		probabilisticBoard = updateRemainingProbabilities(probabilisticBoard, numberOfShots, boardSize)

def openFire(agent, firePosition, gameBoard, probabilisticBoard, boardSize):
	alreadyShot = agent.shots.get(firePosition, None)
	shipSunk = False
	shipHit = False
	if alreadyShot == None:
		agent.numberOfShots = int(agent.numberOfShots) + 1
		agent.shots[firePosition] = "x"
		hasShip = gameBoard.get(firePosition, None)
		if hasShip != None:
			agent.hits = int(agent.hits) + 1
			hasShip.damageCounter = int(hasShip.damageCounter) + 1
			shipSunk = hasShip.isSunk()
			shipHit = True
		else:
			agent.miss = int(agent.miss) + 1
			shipHit = False
		updateProbabilisticBoard(hasShip, probabilisticBoard, firePosition, agent.numberOfShots, boardSize)
	return [shipHit, shipSunk]

def huntMode(agent, target, gameBoard, probabilisticBoard, boardSize):
	shipDestroyed = False
	initialTarget = target
	initialProbability = probabilisticBoard[target]
	left = True
	right = True
	up = True
	down = True
	attempt = 0
	while not shipDestroyed:
		attempt = attempt + 1
		if target[0] + 1 < boardSize and down:
			target = (target[0] + 1, target[1])
			[down, shipDestroyed] = openFire(agent, target, gameBoard, probabilisticBoard, boardSize)
			if not down:
				target = initialTarget
				probabilisticBoard[target] = initialProbability
			if down:
				left = False
				right = False

		elif target[0] - 1 >= 0 and up:
			target = (target[0] - 1, target[1])
			[up, shipDestroyed] = openFire(agent, target, gameBoard, probabilisticBoard, boardSize)
			if not up:
				target = initialTarget
				probabilisticBoard[target] = initialProbability
			if up:
				left = False
				right = False

		elif target[1] + 1 < boardSize and right:
			target = (target[0], target[1] + 1)
			[right, shipDestroyed] = openFire(agent, target, gameBoard, probabilisticBoard, boardSize)
			if not right:
				target = initialTarget
				probabilisticBoard[target] = initialProbability
			if right:
				up = False
				down = False

		elif target[1] - 1 >= 0 and left:
			target = (target[0], target[1] - 1)
			[left, shipDestroyed] = openFire(agent, target, gameBoard, probabilisticBoard, boardSize)
			if not left:
				target = initialTarget
				probabilisticBoard[target] = initialProbability
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
	probabilisticBoard = buildProbabilisticBoard(boardSize)
	firstShot = True
	i = 0
	while not hasGameEnded:
		target = None
		if firstShot:
			firstShot = False
			target = (int(boardSize/2 - 1), int(boardSize/2 - 1))
		if target == None:
			target = mostLikelyPosition(probabilisticBoard, agent)
		shot = agent.shots.get(target, None)
		if shot == None:
			shotStr = str(target[0]) + "," + str(target[1])
			agent.shotList = agent.shotList + [shotStr]
			agent.shots[target] = "x"
			agent.numberOfShots = int(agent.numberOfShots) + 1
			hasShip = gameBoard.get(target, None)
			if hasShip != None:
				agent.hits = int(agent.hits) + 1
				hasShip.damageCounter = int(hasShip.damageCounter) + 1
				if not hasShip.isSunk(): # submarines only take one shot, so theres no need for hunt mode if theyre hit
					huntMode(agent, target, gameBoard, probabilisticBoard, boardSize)
				else:
					probabilisticBoard[target] = 1
			else:
				agent.miss = int(agent.miss) + 1
				probabilisticBoard[target] = 0
			if int(agent.hits) == int(agent.totalDamage):
				hasGameEnded = True
		else:
			probabilisticBoard[target] = 0
def main():
	[gameBoard, ships, buildTime] = board.buildGame()
	agent = Agent(ships)
	startGame(agent, gameBoard, ships)
	#board.printAgentStatistics(agent)
	#board.printData(gameBoard)
	return [agent, gameBoard]

if __name__ == '__main__':
	main()