########### Rohan Pandit ############

from __future__ import division
import numpy as np
import sys
from copy import deepcopy
from time import clock

SIZE= 9
CELLSIZE=3
sys.setrecursionlimit(500)

class Cell(object):
	matrix=None
	def __init__(self, val, x, y, matrix):
		if val != '.':
			self.val=[int(val)]
		else:
			self.val=range(1,10)
		self.x=x
		self.y=y
		self.cellx=(x//CELLSIZE)*CELLSIZE
		self.celly=(y//CELLSIZE)*CELLSIZE
		Cell.matrix=matrix

	def removeFromRow(self):
		num=self.val[0]
		row = Cell.matrix[:,self.y]
		#print("\n num=%s"%num)
		for cell in row:
			if num in cell.val and self.x != cell.x:
				cell.val.remove(num)

	def removeFromCol(self):
		num=self.val[0]
		col = Cell.matrix[self.x,:]
		for cell in col:
			if num in cell.val and self.y != cell.y:
				cell.val.remove(num)

	def removeFromCell(self):
		num=self.val[0]
		matrix=Cell.matrix
		for y in xrange(self.celly, self.celly+CELLSIZE):
			for x in xrange(self.cellx, self.cellx+CELLSIZE):
				print(matrix[x][y])
				if num in matrix[x][y].val and (self.x != x or self.y !=y):
					matrix[x][y].val.remove(num)


	def __str__(self):
		return "%s at (%s, %s)"%(self.val, self.x, self.y)
	def __repr__(self):
		return self.__str__()


def createMatrix(M):
	matrix = np.zeros((SIZE,SIZE), dtype=Cell)
	for y in xrange(SIZE):
		for x in xrange(SIZE):
			matrix[x][y]=Cell(M[x][y],x,y,matrix)
	return matrix

def displayMatrix(matrix):
	for y in xrange(matrix.shape[1]):
		print
		for x in xrange(matrix.shape[0]):
			if len(matrix[x][y].val)==1:
				print(str(list(matrix[x][y].val)[0])+ " "),
			else:
				print(". "),
	print("\n")
	#print(matrix)

def recur(matrix):
	matrix=simpleChanges(matrix)

	if check(matrix) or badMatrix(matrix):
		return matrix

	oldMatrix= deepcopy(matrix)
	r,c = smallestSet(matrix)

	for guess in matrix[r][c].val:
		print("guessing %s at (%s,%s)"%(guess,r,c))
		displayMatrix(matrix)
		matrix[r][c].val = [guess]

		matrix= recur(matrix)

		if check(matrix):
			return matrix

		matrix= restoreValues(matrix, oldMatrix)

	return matrix

def restoreValues(matrix, oldMatrix):
	for y in xrange(matrix.shape[1]):
		for x in xrange(matrix.shape[0]):
			matrix[x][y].val=oldMatrix[x][y].val
	return matrix

def smallestSet(matrix):
	for v in xrange(2, 9):
		for y in xrange(matrix.shape[1]):
			for x in xrange(matrix.shape[0]):
				if len(matrix[x][y].val)==v:
					return (x,y)

def simpleChanges(matrix):
	for y in xrange(matrix.shape[0]):
		for x in xrange(matrix.shape[1]):
			if len(matrix[x][y].val)==1:
				matrix[x][y].removeFromRow()
				matrix[x][y].removeFromCol()
				matrix[x][y].removeFromCell()
	return matrix

def badMatrix(matrix):
	for y in xrange(matrix.shape[1]):
		for x in xrange(matrix.shape[0]):
			if len(matrix[x][y].val)<1:
				return True #Bad matrix

def check(matrix):
	#check filled
	for y in xrange(matrix.shape[1]):
		for x in xrange(matrix.shape[0]):
			if len(matrix[x][y].val)!=1:
				return False #Bad matrix
	#print("filled")

	#check rows
	for y in xrange(matrix.shape[1]):
		row=matrix[:,y]
		rowNumbers= [cell.val[0] for cell in row]
		for n in range(1,SIZE+1):
			if n not in rowNumbers:
				return False
	#print("rows")

	#check cols
	for x in xrange(matrix.shape[0]):
		col=matrix[x,:]
		colNumbers= [cell.val[0] for cell in col]
		for n in range(1,SIZE+1):
			if n not in colNumbers:
				return False

	#print("cols")

	#check cells
	cells= [matrix[x: x+CELLSIZE, y: y+CELLSIZE] for x in range(0, matrix.shape[0], CELLSIZE) for y in range(0, matrix.shape[1], CELLSIZE)]

	for cell in cells:
		cell=cell.flatten()
		cellNumbers= [element.val[0] for element in cell]
		for n in range(1,SIZE+1):
			if n not in cellNumbers:
				return False
	#print("cells")
	return True

def solve(chars):
	start=clock()
	chars=list(chars)
	M=np.resize(chars, (SIZE, SIZE))
	matrix=createMatrix(M.transpose())

	print("starting")
	displayMatrix(matrix)
	matrix=recur(matrix)

	if(check(matrix)):
		print("--------------------------solved! %s sec"%(clock()-start))
	else:
		print("--------------------------failed %s sec"%(clock()-start))
		recur(matrix)
		print(matrix)
	displayMatrix(matrix)


def main():
		f=open(sys.argv[1])
		allChars= list(f.read().splitlines())
		start=clock()

		#map(solve, allChars)
		solve("48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....")
		#solve("8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..")
		print("######################### %s %sx%s Sudokus solved in %s seconds ##########################" %(len(allChars), SIZE, SIZE, clock()-start))
		print("Avg time = %s"%((clock()-start)/len(allChars)))

if __name__ == "__main__":
		main()
