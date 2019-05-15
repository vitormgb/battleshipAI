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
		if alreadyShot == None and firePosition == None:
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
	if alreadyShot == None:
		agent.shotList = agent.shotList + [str(firePosition[0]) + "," + str(firePosition[1])]
		agent.numberOfShots = int(agent.numberOfShots) + 1
		agent.shots[firePosition] = "x"
		hasShip = gameBoard.get(firePosition, None)
		if hasShip != None:
			agent.hits = int(agent.hits) + 1
			hasShip.damageCounter = int(hasShip.damageCounter) + 1
			shipSunk = hasShip.isSunk()
		else:
			agent.miss = int(agent.miss) + 1
		updateProbabilisticBoard(hasShip, probabilisticBoard, firePosition, agent.numberOfShots, boardSize)
	return [shipSunk, hasShip]


def startGame(agent, gameBoard, ships):
	boardSize = 10
	hasGameEnded = False
	probabilisticBoard = buildProbabilisticBoard(boardSize)
	firstShot = True
	while not hasGameEnded:
		firePosition = None
		if firstShot:
			firstShot = False
			firePosition = (int(boardSize/2 - 1), int(boardSize/2 - 1))
		if firePosition == None:
			firePosition = mostLikelyPosition(probabilisticBoard, agent)
		[shipSunk, hasShip] = openFire(agent, firePosition, gameBoard, probabilisticBoard, boardSize)
		if shipSunk:
			ships.remove(hasShip)
		hasGameEnded = len(ships) == 0
		

def main():
	[gameBoard, ships, buildTime] = board.buildGame()
	agent = Agent(ships)
	startGame(agent, gameBoard, ships)
	#board.printAgentStatistics(agent)
	#board.printData(gameBoard)
	return [agent, gameBoard]

if __name__ == '__main__':
	main()
