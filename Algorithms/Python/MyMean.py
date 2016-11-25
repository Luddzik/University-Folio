import math
import numpy

def MyMean(matrix):
	X = numpy.zeros((1, matrix.shape[1]))
	for i in matrix[0]:
		X += i/matrix.shape[0]

	return X[0]
