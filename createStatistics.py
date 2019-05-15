#!/usr/bin/env python
import sys
import dummy
import hunter
import probabilistic
import probabilisticHunter

def main():
	#outputFile = open('probabilisticHunterStats.out', 'w')
	gameBoardFile = open('probabilisticGameBoard.out', 'w')
	playerFile = open('probabilisticPlayerBoard.out', 'w')
	i = 1
	while i <= 10**5:
		[agent, gameBoard] = dummy.main()
		if agent.numberOfShots < 80:
			for key in gameBoard.keys():
				gameBoardFile.write(str(key[0]) + "," + str(key[1]) + "," + str(gameBoard[key].shipId) + '\n')
			for key in agent.shotList:
				playerFile.write(key + "\n")
			gameBoardFile.close()
			playerFile.close()
			sys.exit()
		#outputFile.write(str(i) + " " + str(agent.numberOfShots) + " " + str(agent.miss) + " " + str(agent.numberOfShots - agent.miss) + " " + str(round((agent.hits/float(agent.miss)),4)) + "\n")
		i = i + 1

if __name__ == '__main__':
	main()