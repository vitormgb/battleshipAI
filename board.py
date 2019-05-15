#!/usr/bin/env python
import sys
import random
import time

class Ship:
	def __init__(self, dimension, shipType, shipId):
		self.dimension = dimension
		self.shipType = shipType
		self.shipId = shipId
		self.damageCounter = 0
		self.position = list()

	def isSunk(self):
		return self.dimension == self.damageCounter

class ShipType:
	CARRIER = (5, "Carrier", "#")
	BATTLESHIP = (4, "Battleship", "%")
	CRUISER = (3, "Cruiser", "@")
	DESTROYER = (2, "Destroyer", "*")
	SUBMARINE = (1, "Submarine", "o")


def buildShipSet():
	ships = list()

	ships.append(Ship(ShipType.CARRIER[0], ShipType.CARRIER[1], ShipType.CARRIER[2]))
	ships.append(Ship(ShipType.BATTLESHIP[0], ShipType.BATTLESHIP[1], ShipType.BATTLESHIP[2]))
	ships.append(Ship(ShipType.CRUISER[0], ShipType.CRUISER[1], ShipType.CRUISER[2]))
	ships.append(Ship(ShipType.DESTROYER[0], ShipType.DESTROYER[1], ShipType.DESTROYER[2]))
	ships.append(Ship(ShipType.DESTROYER[0], ShipType.DESTROYER[1], ShipType.DESTROYER[2]))
	ships.append(Ship(ShipType.SUBMARINE[0], ShipType.SUBMARINE[1], ShipType.SUBMARINE[2]))
	ships.append(Ship(ShipType.SUBMARINE[0], ShipType.SUBMARINE[1], ShipType.SUBMARINE[2]))

	return ships

def buildBoard(ships):
	boardSize = 10
	board = dict()
	for ship in ships:
		shipPlaced = False #initially we consider the ship is not placed
		while not shipPlaced:
			coin = bool(random.getrandbits(1))
			start_x = int(random.randint(0, boardSize - 1))
			start_y = int(random.randint(0, boardSize - 1))	
			shipPositions = list()
			if coin: #horizontal ship position
				if 0 <= start_x + ship.dimension < boardSize:
					for i in range(ship.dimension):
						key = (int(start_x + i), start_y)
						exist = board.get(key, None)
						if exist == None:
							shipPositions.append(key)
						else:
							break
				elif 0 <= start_x - ship.dimension < boardSize:
					i = int(ship.dimension)
					while i > 0:
						key = (int(start_x - i), start_y)
						exist = board.get(key, None)
						i = i-1
						if exist == None:
							shipPositions.append(key)
						else:
							break
			else: #vertical ship position
				if 0 <= start_y + ship.dimension < boardSize:
					for i in range(ship.dimension):
						key = (start_x, int(start_y + i))
						exist = board.get(key, None)
						if exist == None:
							shipPositions.append(key)
						else:
							break
				elif 0 <= start_x - ship.dimension < boardSize:
					i = int(ship.dimension)
					while i > 0:
						key = (start_x, int(start_y - i))
						exist = board.get(key, None)
						i = i-1
						if exist == None:
							shipPositions.append(key)
						else:
							break
			if len(shipPositions) == int(ship.dimension): #ship is placeed
				i = 0
				while i < len(shipPositions):
					key = shipPositions[i]
					board[key] = ship
					i = i + 1
				shipPlaced = True
	return board

def buildGame():
	ships = buildShipSet()
	start_time = time.time()
	board = buildBoard(ships)
	buildTime = time.time() - start_time
	return [board, ships, buildTime]

def printAgentStatistics(agent):
	print "-----------------------------------------------------------"
	print "Agent board setup\n"
	boardSize = 10
	for i in range(boardSize):
		string = ""
		for j in range(boardSize):
			key = (int(i), int(j))
			item = agent.shots.get(key, None)
			if item == None:
				string = string + "- "
			else:
				string = string + item + " "
		print string

	print "\nIdentifiers: \nx: Shot\n-: Not shot"
	print "\nStatistics:"
	print "Total number of shots: " + str(agent.numberOfShots) + "\nNumber of miss: " + str(agent.miss) + "\nAccuracy: " + str(round((agent.hits/float(agent.miss)),4))
	print "-----------------------------------------------------------"

def printData(gameBoard):
	print "Board setup\n"
	for i in range(10):
		string = ""
		for j in range(10):
			key = (int(i),int(j))
			item = gameBoard.get(key, None)
			if item == None:
				string = string + "- "
			else:
				string = string + item.shipId + " "
		print string
	print "\nIdentifiers: \n#: Carrier (size: 5)\n%: Battleship (size: 4)\n@: Cruiser (size: 3)\n*: Destroyer(size: 2)\no: Submarine (size: 1)\n-: Nothing (water)"
	print "-----------------------------------------------------------"



