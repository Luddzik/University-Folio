#__author__ = s1345559
import scipy.io
import numpy
import math
import scipy.spatial.distance as dist

data = scipy.io.loadmat("cifar10.mat")

#calculate the distance between the test and the trainMatrix
def ecludianDistance(test, trainMatrix):
	return dist.cdist([test], [trainMatrix], 'euclidean')

#calculate the nearest 'k' points from test data in trainingData
def kNearest(k, testData, trainingData):
	dic = {}
	for i in range(len(trainingData)):
		index = i
		dic[str(ecludianDistance(testData, trainingData[i]))] = (index)
		
	distances = dic.keys()
	distances.sort()
	
	kShortestDistances = []
	for x in range(k):
		kShortestDistances.append((distances[x], dic[distances[x]]))
		del dic[distances[x]]
		
	return kShortestDistances

#hold names for folds and classes, to be able to access them later
folds = ['fold1_features', 'fold2_features', 'fold3_features', 'fold4_features', 'fold5_features', 'fold6_features', 'fold7_features', 'fold8_features', 'fold9_features', 'fold10_features']
classes = ['fold1_classes', 'fold2_classes', 'fold3_classes', 'fold4_classes', 'fold5_classes', 'fold6_classes', 'fold7_classes', 'fold8_classes', 'fold9_classes', 'fold10_classes']

#choose id from the given vector	
def choose_id(dictionary):
	categories = []
	for i in range(1, 11):
		category_counter = 0
		for value in dictionary.values():
			if (value == i):
				category_counter += 1
		categories.append(category_counter)

#in case of a tie, choose the closest distance vector, by removing the further away vector		
	maxNumber = max(categories)
	for category in categories:
		if (maxNumber == category):
			if (categories.index(maxNumber) != categories.index(category)):
				del dictionary[dictionary.keys()[-1]]
				choose_id(dictionary)
				
	return (categories.index(maxNumber) + 1) 

#classify the vector with an ID		
def classify(k, testData, foldName):
	closestPictures = {}
	for fold in folds:
		if (fold != foldName):  #if folds are different do below
			points = kNearest(k, testData, data[fold])
			for p in points:
				closestPictures[p[0]] = [p[1], fold]
				
	closestDistances = closestPictures.keys()
	closestDistances.sort()
	
	KClosestPictures = {}
	for x in range(k):
		KClosestPictures[closestDistances[x]] = closestPictures[closestDistances[x]]
		del closestPictures[closestDistances[x]]
		
	KClosestPicturesIDs = {}
	for d in KClosestPictures.keys():
		classNumber = folds.index(KClosestPictures[d][1])
		KClosestPicturesIDs[d] = data['fold' + str(classNumber +1) + '_classes'][KClosestPictures[d][0]][0]
		
	return choose_id(KClosestPicturesIDs)

#this method will do classifiation for a complete feature-fold, and it returns the IDs in a list.
def totalClassification(k, trainingPic): 
	id_classes = []
	temp = 0
	for i in data[trainingPic][:5]:
		id_classes.append(classify(k, i, trainingPic))
		temp += 1
		print temp
	return id_classes

#this method will check how accurate the code is, comparing the classified ID to actual ID, returning a matrix
def confusion_matrix(ids1, ids2):
	confusionMatrix = numpy.zeros((10,10), dtype=int)
	actualIDs = [item for sublist in ids2 for item in sublist]
	for count1, count2 in zip(ids1, actualIDs):
		confusionMatrix[count1-1][count2-1] += 1
	return confusionMatrix	

#this method does full accuracy test between along all folds.
def fullConfusion(k):
	fullConfusionMatrix = numpy.zeros((10,10), dtype = int)
	temp = 0
	for fold in folds:
		temp += 1
		print ("fold: " + str(temp))
		ids = totalClassification(k, fold)
		fullConfusionMatrix += confusion_matrix(ids, data['fold' +str(folds.index(fold) +1) + '_classes'])
	print fullConfusionMatrix
	
	accuracy = 0
	for i in range(10):
		accuracy += (fullConfusionMatrix[i][i])/float(sum(fullConfusionMatrix[i]))
		
	return accuracy/10
print fullConfusion(3)
print fullConfusion(5)

