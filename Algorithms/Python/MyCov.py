import math
import numpy
import MyMean as MyMean

def MyCov(matrix):
	matrixArray = numpy.array(matrix, dtype='float64')
	print matrixArray
	matrixMean = MyMean.MyMean(matrixArray)
	X = numpy.zeros((1, matrixArray.shape[1]))

	for m in matrixArray:
		m = m - matrixMean
		m = m * m.T
		X = X + m

	ans = (X/((matrixArray.shape[0])-1))[0]

	return ans
