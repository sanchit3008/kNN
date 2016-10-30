import csv
import math
import operator
import random

def loadDataset(filename, split, trainingset= [], testset= []):
	with open(filename,"rb") as csv_file:
		lines = csv.reader(csv_file)
		dataset = list(lines)
		for x in range(len(dataset)-1):
			for y in range(4):
				dataset[x][y] = float(dataset[x][y])
			if random.random() < split:
				trainingset.append(dataset[x])
			else:
				testset.append(dataset[x])

def euclidean_distance(ins1, ins2, length):
	distance = 0
	for x in range(length):
		distance += pow(ins1[x] - ins2[x] , 2)
	return math.sqrt(distance)

def getNeighbours(trainingset, testInstance, k):
	distances = []
	length = len(testInstance) - 1
	for x in range(len(trainingset)):
		dist = euclidean_distance(testInstance,trainingset[x],length)
		distances.append((trainingset[x],dist))
	distances.sort(key = operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def assignClass(neighbors):
	clasVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in clasVotes:
			clasVotes[response] += 1
		else:
			clasVotes[response] = 1
	sortedVotes = sorted(clasVotes.iteritems(),key = operator.itemgetter(1), reverse = True)
	return sortedVotes[0][0]

def accuracy(testset,predictions):
	correct = 0
	for x in range (len(testset)):
		if testset[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testset))) * 100.0

def main():
	trainingset = []
	testset = []
	split = 0.67
	loadDataset("iris.data",split,trainingset,testset)
	print trainingset
	print testset
	predictions = []
	k = 6
	for x in range((len(testset))):
		neighbors = getNeighbours(trainingset,testset[x],k)
		result = assignClass(neighbors)
		predictions.append(result)
		print('>predicted='+repr(result)+',actual='+repr(testset[x][-1]))
	Accuracy = accuracy(testset,predictions)
	print('Accuracy:'+repr(Accuracy)+'%')

main()

