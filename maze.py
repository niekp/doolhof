import png
import sys
import shutil
import os
import time

class maze:
	# Laad de afbeelding in
	def __init__(self, file):

		self.originalfile = file

		r = png.Reader(file)
		l = r.read()

		self.width = l[0]
		self.height = l[1]

		self.image = l[2]
		self.image_list = [];
		self.currentpos = [0, 0]
		self.startpos = [0, 0]
		self.parsedmaze = []

	def whatsAt(self, row, col):
		return self.parsedmaze[row][col]

	# Is je huidige positie gelijk aan de finish?
	def finished(self):
		if (self.parsedmaze[self.currentpos[0]][self.currentpos[1]] == 'E'):
			return True
		else:
			return False

	# Wat zijn de mogelijke zetten vanaf het huidige punt?
	def possibilities(self, row, col):
		options = []
		if self.whatsAt(row, col) != 'W':
			# left
			if (col > 0):
				if self.whatsAt(row, col - 1) == 'P' or self.whatsAt(row, col - 1) == 'E':
					options.append('L')
			# right
			if (col < self.width - 1):
				if self.whatsAt(row, col + 1) == 'P' or self.whatsAt(row, col + 1) == 'E':
					options.append('R')

			# top
			if (row > 0):
				if self.whatsAt(row - 1, col) == 'P' or self.whatsAt(row -1, col) == 'E':
					options.append('T')

			# bottom
			if (row < self.height - 1):
				if self.whatsAt(row + 1, col) == 'P' or self.whatsAt(row + 1, col) == 'E':
					options.append('B')

		return options

	# Beweeg in een richting
	def move(self, direction):
		if direction == 'T':
			self.currentpos[0]-=1
		elif direction == 'B':
			self.currentpos[0]+=1
		elif direction == 'L':
			self.currentpos[1]-=1
		elif direction == 'R':
			self.currentpos[1]+=1

	# Zet de huidige positie op een x,y. Voor de startpositie
	def setPosition(self, row, col):
		self.currentpos[0] = row;
		self.currentpos[1] = col;

	# Parse de afbeelding naar een array
	def parse(self):
		rownum = 0

		self.image_list = list(self.image);

		for row in self.image_list:
			counter = 0
			color = [0, 0, 0]
			rowbuilder = [];
			for col in row:
				color[counter % 3] = col;
				
				if (counter % 3 == 2):
					if color == [255, 255, 255]:
						rowbuilder.append('P')
					elif color == [255, 0, 0]:
						self.endpos = [rownum, int(((counter + 1) / 3) - 1)]
						rowbuilder.append('E')
					elif color == [0, 255, 0]:
						self.startpos = [rownum, int(((counter + 1) / 3) - 1)]
						rowbuilder.append('S')
					else:
						rowbuilder.append('W')

				counter += 1

			rownum += 1
			self.parsedmaze.append(rowbuilder)
			self.currentpos = self.startpos;
		
	# Geef het doolhof weer in de terminal
	def output(self, path):
		rownum = 0
		#time.sleep(0.03)
		#os.system('cls' if os.name == 'nt' else 'clear')
		#os.system('cls' if os.name == 'nt' else 'clear')
		print('\n\n\n');
		for row in self.image_list:
			counter = 0
			colnum = 0
			color = [0, 0, 0]
			fillnum = 0

			for col in row:
				color[counter % 3] = col;
				
				if (counter % 3 == 2):
					if color == [255, 255, 255]:
						fill = False
						fillnum = 0
						for x in path:
							fillnum+=1
							if x[0] == rownum and x[1] == colnum:
								fill = True
								break

						if fill:
							sys.stdout.write('##')
							#sys.stdout.write(('  ' + str(fillnum))[-2:])
						else:
							sys.stdout.write('  ')

					elif color == [255, 0, 0]:
						sys.stdout.write('EE')
					elif color == [0, 255, 0]:
						sys.stdout.write('SS')
					else:
						sys.stdout.write('||')

					colnum+= 1
				counter += 1

			rownum += 1
			sys.stdout.write('\n')