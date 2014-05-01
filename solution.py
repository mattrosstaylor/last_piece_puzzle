#!/bin/python

################################
# The Last Piece Puzzle Solver #
#         Matt R Taylor        #
################################

###################
# Utility Classes #
###################

class Piece:
	def __init__(self, name, polarity, shape):
		self.name = name
		self.polarity = polarity # denotes whether a piece goes 'in' or 'out' at the origin
		self.shape = shape # list of coordinates for each block in the shape

	def __str__(self):
		return self.name

class Board:
	def __init__(self):
		self.size = 8
		self.empty = None
		self.grid = []
		self.order = []

		for y in range(self.size):
			self.grid.append([self.empty] * self.size)

	# returns true if a piece can be placed at the given position and orientation - takes polarity into account
	def testWithPolarity(self, piece, x, y, orientation):
		if (x % 2 == 0) ^ (y % 2 == 0) == piece.polarity:
			return False
		return self.test(piece,x,y,orientation)

	# returns true if a piece can be placed at the given position and orientation
	def test(self, piece, x, y, orientation):
		for part in piece.shape:
			if orientation == 0:
				xx = x+part[0]
				yy = y+part[1]
			elif orientation == 1:
				xx = x-part[1]
				yy = y+part[0]
			elif orientation == 2:
				xx = x-part[0]
				yy = y-part[1]
			elif orientation == 3:
				xx = x+part[1]
				yy = y-part[0]

			if not self.testCoordinate(xx,yy):
				return False
		return True

	# returns true if a cell is empty
	def testCoordinate(self, x, y):
		if (0 <= x < self.size) and (0 <= y < self.size) and (self.grid[x][y] == self.empty):
			return True
		else:
			return False

	# places a piece at the given position and orientation
	def place(self, piece, x, y, orientation):
		for part in piece.shape:
			if orientation == 0:
				self.grid[x+part[0]][y+part[1]] = piece.name
			elif orientation == 1:
				self.grid[x-part[1]][y+part[0]] = piece.name
			elif orientation == 2:
				self.grid[x-part[0]][y-part[1]] = piece.name
			elif orientation == 3:
				self.grid[x+part[1]][y-part[0]] = piece.name
		self.order.append(piece.name)

	# remove a piece from the given position and orientation
	def remove(self, piece, x, y, orientation):
		for part in piece.shape:
			if orientation == 0:
				self.grid[x+part[0]][y+part[1]] = self.empty
			elif orientation == 1:
				self.grid[x-part[1]][y+part[0]] = self.empty
			elif orientation == 2:
				self.grid[x-part[0]][y-part[1]] = self.empty
			elif orientation == 3:
				self.grid[x+part[1]][y-part[0]] = self.empty
		self.order.pop()

	# process a piece as a placement candidate
	# for a given piece and orientation, add  tuple (piece, x, y orientation) to the lookup list for each cell covered by the piece
	def addAsCandidate(self, piece, x, y, orientation):
		for part in piece.shape:
			if orientation == 0:
				self.grid[x+part[0]][y+part[1]].append([piece, x, y, orientation])
			elif orientation == 1:
				self.grid[x-part[1]][y+part[0]].append([piece, x, y, orientation])
			elif orientation == 2:
				self.grid[x-part[0]][y-part[1]].append([piece, x, y, orientation])
			elif orientation == 3:
				self.grid[x+part[1]][y-part[0]].append([piece, x, y, orientation])

	def __str__(self):
		output = ''
		if len(self.order) > 0:
			output += 'Order: ' +' '.join(self.order) +'\n'
		for y in range(self.size):
			for x in range(self.size):
				if self.grid[x][y] == None:
					output += '- '
				else:
					output += self.grid[x][y] +' '
			output += '\n'
		return output


#####################
# Piece Definitions #
#####################

pieces = []
# small
pieces.append(Piece('?', 0, [[0,0],[0,1],[1,0]]))
pieces.append(Piece('j', 0, [[0,0],[0,1],[0,2],[-1,2]]))
pieces.append(Piece('l', 1, [[0,0],[0,1],[0,2],[1,2]]))
pieces.append(Piece('s', 1, [[0,0],[0,1],[1,1],[1,2]]))
pieces.append(Piece('t', 1, [[0,0],[1,0],[-1,0],[0,1]]))

# medium
pieces.append(Piece('p', 1, [[0,0],[0,1],[0,2],[0,3],[1,1]]))
pieces.append(Piece('q', 0, [[0,0],[0,1],[0,2],[0,3],[-1,1]]))
pieces.append(Piece('r', 1, [[0,0],[0,1],[-1,1],[-1,2],[-1,3]]))
pieces.append(Piece('h', 0, [[0,0],[0,1],[0,2],[1,2],[1,3]]))
pieces.append(Piece('J', 1, [[0,0],[0,1],[0,2],[0,3],[-1,3]]))
pieces.append(Piece('L', 0, [[0,0],[0,1],[0,2],[0,3],[1,3]]))

# large
pieces.append(Piece('S', 1, [[0,0],[0,1],[-1,1],[0,-1],[1,-1]]))
pieces.append(Piece('Z', 0, [[0,0],[0,1],[1,1],[0,-1],[-1,-1]]))
pieces.append(Piece('W', 1, [[0,0],[1,0],[1,1],[0,-1],[-1,-1]]))

##############
# Initialise #
##############

b = Board()
startingPieces = []
for p in pieces:
	startingPieces.append(p.name)

# hard code placement of "last piece" - it can only go in one position
b.place(pieces[0],6,7,3)
startingPieces.remove('?')

#############################
# Cell Order Calculation #
#############################

# cell order is a list containing co-ordinates for each cell on the board - in the order the algorithm will attempt to fill them
cellOrder = []

for diag in reversed(range(16)):
	for c in range(diag+1):
		if c < 8 and diag-c < 8:
			if not diag-c == c:
				cellOrder.append([diag-c, c])
			else:
				cellOrder.append([c, c])

# output board with the priority for each cell (lower is more important)
priorityBoard = Board()
for i in range(len(cellOrder)):
	cell = cellOrder[i]
	priorityBoard.grid[cell[0]][cell[1]] = str(i).zfill(2)
print "Cell Priorities:"
print priorityBoard

######################################
# Calculate Candidate Placement Sets #
######################################

candidateBoard = Board()
for y in range(8):
	for x in range(8):
		candidateBoard.grid[x][y] = []

for piece in pieces:
	if piece.name in startingPieces:
		for cell in cellOrder:
			# don't duplicate orientations for pieces that have rotational symmetry
			if piece.name == 'S' or piece.name == 'Z':
				possibleOrientations = 2
			else:
				possibleOrientations = 4

			for orientation in range(possibleOrientations):
				if b.testWithPolarity(piece, cell[0], cell[1], orientation):
					candidateBoard.addAsCandidate(piece, cell[0], cell[1], orientation)

# output board with the number of potential piece placements for each cell
candidateDisplayBoard = Board()
for i in range(len(cellOrder)):
	cell = cellOrder[i]
	candidateDisplayBoard.grid[cell[0]][cell[1]] = str(len(candidateBoard.grid[cell[0]][cell[1]])).zfill(3)
print "Candidate Placement Set sizes:"
print candidateDisplayBoard

i = 0

##################################
# Ordered Cell Filling Algorithm #
##################################

def solve(board, targetCellIndex, piecesLeft):
	global i
	i+=1

	if len(piecesLeft) == 0:
		print "Solution found after " +str(i) +" iterations"
		print board
		return

	findingNextCell = True
	while findingNextCell:
		targetCell = cellOrder[targetCellIndex]
		if board.grid[targetCell[0]][targetCell[1]] == board.empty:
			findingNextCell = False
		else:
			targetCellIndex+=1
			if targetCellIndex >= len(cellOrder):
				return

	"""
	if i % 1000 == 0:
		print piecesLeft
		print board
		print
	"""

	for c in candidateBoard.grid[targetCell[0]][targetCell[1]]:
		if c[0].name in piecesLeft:
			if board.test(c[0],c[1],c[2],c[3]):
				piecesLeft.remove(c[0].name)
				board.place(c[0],c[1],c[2],c[3])
				solve(board, targetCellIndex+1, piecesLeft)
				board.remove(c[0],c[1],c[2],c[3])
				piecesLeft.add(c[0].name)

#########
# Start #
#########

solve(b, 0, set(startingPieces))
print "\nTotal Iterations: " +str(i)
