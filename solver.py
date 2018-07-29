import png
import sys
import time

class solver:

	def __init__(self, maze):
		self.maze = maze
		self.path = []
		self.choices = []

	# Om te voorkomen dat hij heen en weer gaat lopen mag je niet omdraaien
	def opposite(self, direction):
		if direction == 'T':
			return 'B'
		elif direction == 'B':
			return 'T'
		elif direction == 'L':
			return 'R'
		elif direction == 'R':
			return 'L'
		else:
			return direction

	def getPath(self):
		return self.path

	def reset(self):
		self.path = []
		self.maze.setPosition(13, 3)

	# Zoek de oplossing
	def solve(self, timer):
		running = True
		failsafe = 0
		prevDirection = ''

		while running:
			
			# Opgelost?
			if self.maze.finished():
				print("Jaaa!!")
				running = False
				break

			# Wat zijn de mogelijke zetten?
			possibilities = self.maze.possibilities(self.maze.currentpos[0], self.maze.currentpos[1]);

			
			if len(possibilities) > 0:

				validOption = ''
				tryOption = ''
				dontTry = []

				for choice in self.choices:
					if choice[0] == self.maze.currentpos[0] and choice[1] == self.maze.currentpos[1]:
						if choice[3] == 'F': # Mislukte routes niet nogmaals pakken
							dontTry.append(choice[2])

				for option in possibilities:
					if option != self.opposite(prevDirection):
						if option not in dontTry:
							tryOption = option

						if (validOption == ''): # Is er maar 1 optie? 
							validOption = option
						else:
							validOption = 'X'

				if validOption != 'X' and validOption != '':
					# Als er maar 1 optie is, ga daar heen.
					self.maze.move(validOption)
					
					self.path.append([self.maze.currentpos[0], self.maze.currentpos[1]]);

					prevDirection = validOption

				elif tryOption != '': # Kruispunt
					# Optie bewaren en gaan.
					self.choices.append([self.maze.currentpos[0], self.maze.currentpos[1], self.opposite(prevDirection), 'F'])
					self.choices.append([self.maze.currentpos[0], self.maze.currentpos[1], tryOption, '?'])

					self.maze.move(tryOption)
					
					self.path.append([self.maze.currentpos[0], self.maze.currentpos[1]]);
					

					prevDirection = tryOption
					

				else:
					# Laatste (kruispunt) keuze mislukt
					prevDirection = ''
					self.choices[-1][3] = 'F' #fail
					self.path = []
					# Reset naar laatste kruispunt
					self.maze.setPosition(self.choices[-1][0], self.choices[-1][1])

				time.sleep(timer)
				if(timer > 0):
					self.maze.output(self.path)
				failsafe+=1

				if (failsafe > 500):
					running = False
			else:
				running = False

			
