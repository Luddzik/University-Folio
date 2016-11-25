#__author__ = s1345559
import scipy.io
import math
import numpy
import MyMean as MyMean
import MyCov as mycov

data = scipy.io.loadmat("cifar10.mat")

categories = ['category1', 'category2','category3', 'category4', 'category5','category6', 'category7', 'category8','category9', 'category10']
folds = ['fold1_features', 'fold2_features', 'fold3_features', 'fold4_features', 'fold5_features', 'fold6_features', 'fold7_features', 'fold8_features', 'fold9_features', 'fold10_features']
classes = ['fold1_classes', 'fold2_classes', 'fold3_classes', 'fold4_classes', 'fold5_classes', 'fold6_classes', 'fold7_classes', 'fold8_classes', 'fold9_classes', 'fold10_classes']

def classesFinder(foldName):
	categoriesPictures = {'category1' : [], 'category2' : [], 'category3' : [], 'category4' : [], 'category5' : [], 'category6' : [], 'category7' : [], 'category8' : [], 'category9' : [], 'category10' : []}
	for category in categories:
		categoryID = categories.index(category) +1
		#print categoryID
		for fold in folds:
			foldIndex = folds.index(fold) +1
			#print foldIndex
			if (fold != foldName):
				pictureIndex = 0
				for picture in data[fold]:
					if(data['fold' + str(foldIndex) + '_classes'][pictureIndex] == categoryID):
						categoriesPictures[category].append(picture)
					pictureIndex += 1
	return categoriesPictures

def gaussianProbability(testVector,logDetCovTrainData, invCovTrainData, meanTrainData): 
	d = testVector - meanTrainData
	c = numpy.dot(d, invCovTrainData)
	c = numpy.dot(c,d.T)
	c = c*(-0.5)
	c = c - ((0.5)*(logDetCovTrainData))
	return c
	
def gaussianClassifier(testVector, foldName, trainData):
	probEachCategory = []
	for category in categories:
		meanTrainData = MyMean(trainData[category])
		cov = mycov.MyCov(trainData[category])
		invCovTrainData = numpy.linalg.inv(cov)
		logDetCovTrainData = numpy.log(numpy.linalg.logdet(cov))
		probEachCategory.append(gaussianProbability(testVector, logDetCovTrainData, invCovTrainData, meanTrainData))
		
	bestClass = max(probEachCategory)
	return probEachCategory.index(bestClass) +1
	
def totalGaussianClassification(matrix):
	trainData = classesFinder(matrix)
	id_classes = []
	for picture in data[matrix]:
		id_classes.append(gaussianClassifier(picture, matrix, trainData))
	return id_classes
	
def guassianDiscriminantClassifier(testVector, foldName, invCovTrainData, logDetCovTrainData, trainData): 
	probOfEachCategory = []
	for category in categories:
		meanTrainData = MyMean.MyMean(TrainData[category])
		probOfEachCategory.append(gaussianProbability(testVector, logDetCovTrainData, invCovTrainData, meanTrainData))
	bestClass = max(probOfEachCategory)
	return probOfEachCategory.index(bestClass) + 1

def totalGaussianClassificationDiscriminant(matrix): #this method will do classifiation for a complete feature-fold, and it returns the ids in a list.
	trainData = classesFinder(matrix)
	id_classes = []
	allPoints = []
	for fold in folds:
		allPoints.append(data[fold])
	cov = mycov.MyCov(allPoints)
	invCovTrainData = numpy.linalg.inv(cov)
	logDetCovTrainData = numpy.log(numpy.linalg.logdet(cov))		
	for picture in data[matrix]:
		id_classes.append(guassianDiscriminantClassifier(picture, matrix, invCovTrainData, logDetCovTrainData, trainingPictures))
	return id_classes

#test:
print totalGaussianClassificationDiscriminant('fold1_features')
#print data['fold2_classes']

def logdet(covariance):
    """
    This should be equivalent to the following:
    
    >>> covariance_logdet = numpy.linalg.slogdet(covariance)[1]

    """
    L = np.linalg.cholesky(covariance)
    covariance_logdet = 2*np.sum(np.log(np.diagonal(L)))
    return covariance_logdet

