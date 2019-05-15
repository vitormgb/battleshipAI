#!/usr/bin/env python
import sys
import board
import random

class Agent:
	def __init__(self, ships):
		self.shots = dict()
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
			if hasShip == None:
				agent.miss = int(agent.miss) + 1
			else:
				agent.hits = int(agent.hits) + 1
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
