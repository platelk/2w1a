import numpy
import math
import pickle
import time


def calc_dist(p1,p2):
    return numpy.linalg.norm(numpy.array(p1)-numpy.array(p2))


class Candidate:
    def __init__(self, DNA=None):
        self.name = 'test'
        if DNA is not None:
            self.setDNA(DNA)

    def getDNA(self):
        return []

    def setDNA(self, DNA):
        return True

    def copy(self, DNA):
        return Candidate(DNA=DNA)


def middleCrossOver(dna1, dna2, pos1, pos2):
    cdna1 = []
    cdna2 = []

    def mixList(l1, l2):
        tmp = []
        tmp.extend(l1[:(len(l1)/2)])
        tmp.extend(l2[(len(l1)/2):])
        return tmp

    for operation1, operation2 in zip(dna1, dna2):
        cdna1.append([mixList(operation1[0], operation2[0]), mixList(operation1[1], operation2[1])])
        cdna2.append([mixList(operation2[0], operation1[0]), mixList(operation2[1], operation1[1])])

    if len(cdna1) < len(dna1) or len(cdna2) < len(dna2):
        def expandDNA(cdna, dna):
            for o in dna[len(cdna):]:
                if numpy.random.randint(8) > 1:
                    cdna.append(o)
        expandDNA(cdna1, dna1)
        expandDNA(cdna2, dna2)


    return cdna1, cdna2

def fitnessCrossOver(dna1, dna2, pos1, pos2):
    cdna1 = []
    cdna2 = []

    def mixList(l1, l2):
        tmp = []
        tmp.extend(l1[:(len(l1)/1.5)])
        tmp.extend(l2[(len(l1)/1.5):])
        return tmp

    for operation1, operation2 in zip(dna1, dna2):
        cdna1.append([mixList(operation1[0], operation2[0]), mixList(operation1[1], operation2[1])])
        cdna2.append([mixList(operation2[0], operation1[0]), mixList(operation2[1], operation1[1])])

    if len(cdna1) < len(dna1) or len(cdna2) < len(dna2):
        def expandDNA(cdna, dna):
            for o in dna[len(cdna):]:
                if numpy.random.randint(8) > 1:
                    cdna.append(o)
        expandDNA(cdna1, dna1)
        expandDNA(cdna2, dna2)


    return cdna1, cdna2


def randomCrossOver(dna1, dna2, pos1, pos2):
    cdna1 = []
    cdna2 = []

    def mixList(l1, l2, pos1, pos2):
        tmp = []
        for i in range(len(l1)):
            if numpy.random.randint(pos1+pos2) < pos1:
                tmp.append(l1[i])
            else:
                tmp.append(l2[i])
        return tmp

    for operation1, operation2 in zip(dna1, dna2):
        cdna1.append([mixList(operation1[0], operation2[0], pos1, pos2), mixList(operation1[1], operation2[1], pos1, pos2)])
        cdna2.append([mixList(operation2[0], operation1[0], pos2, pos1), mixList(operation2[1], operation1[1], pos2, pos1)])

    if len(cdna1) < len(dna1) or len(cdna2) < len(dna2):
        def expandDNA(cdna, dna):
            for o in dna[len(cdna):]:
                if numpy.random.randint(9) > 1:
                    cdna.append(o)
        expandDNA(cdna1, dna1)
        expandDNA(cdna2, dna2)


    return cdna1, cdna2


def randomSelection(population):
    return population[numpy.random.randint(len(population))], population[numpy.random.randint(len(population))]


def rankSelection(population):
    def getIdx(population):
        nbRand = 0
        for i in range(len(population)):
            nbRand += (i+1)*len(population)
        r = numpy.random.randint(nbRand)
        return int(math.ceil((r / (len(population))) / len(population)))
    return population[getIdx(population)], population[getIdx(population)]

def newGenerationSelection(populations):
    return populations[:int(len(populations)*0.8)]

class GenAlgo:
    def __init__(self, createCandidate, fitness, nbPopulate=5, crossOverFct=randomCrossOver, selection=randomSelection, loadfile=None, newGenerationSelection=newGenerationSelection):
        self.savefile = './saved/' + str(time.time()) + '.dat'
        self.createCandidate = createCandidate
        self.fitness = fitness
        self.populations = []
        self.nbPopulate = nbPopulate
        self.crossOverFct = crossOverFct
        self.selection = selection
        self.newGenerationSelection = newGenerationSelection
        if (loadfile is not None):
          self.load(loadfile)

    def createPopulation(self):
        population = []
        for i in range(self.nbPopulate):
            population.append(self.createCandidate())
        self.populations.append(population)

    def crossOver(self, candidate1, candidate2):
        dna1, dna2 = self.crossOverFct(candidate1.getDNA(), candidate2.getDNA(), len(self.populations[-1]) - self.populations[-1].index(candidate1), len(self.populations[-1]) - self.populations[-1].index(candidate2))

        child1 = candidate1.copy()
        child1.setDNA(dna1)
        child2 = candidate2.copy()
        child2.setDNA(dna2)

        return child1, child2

    def save(self):
        try:
          with open(self.savefile, 'wb') as savefile:
            pickle.dump(self.populations[-1], savefile)
        except:
          print 'Something gone wrong'

    def load(self, filename):
        with open(filename, 'rb') as loadfile:
          self.populations = [pickle.load(loadfile)]

    def sortCandidate(self):
        tmp = [(self.fitness(i), i) for i in self.populations[-1]]
        tmp = sorted(tmp, key=lambda x: x[0])
        return [i[1] for i in tmp[::-1]], tmp[::-1]

    def printGenerationResume(self, result):
        print "Top 5:"
        for i, c in enumerate(self.populations[-1][:5]):
            print "   ", i, ". ", result[i]
        print "Total score: ", sum([i[0] for i in result])

    def run(self, it=5, state={}):
        if len(self.populations) == 0:
          self.createPopulation()
        for i in range(it):
            print ">>>{ Iteration: ", i, " }<<<"
            self.populations[-1], result = self.sortCandidate()
            newGeneration = []
            for c in range(len(self.populations[-1])):
                c1, c2 = self.selection(self.populations[-1])
                child1, child2 = self.crossOver(c1, c2)
                newGeneration.append(child1)
            self.printGenerationResume(result)
            self.populations.append(newGeneration)
            self.save()
            # Remove bad performing candidate ?
            self.populations[-1] = self.newGenerationSelection(self.populations[-1])
            while len(self.populations[-1]) < self.nbPopulate:
                self.populations[-1].append(self.createCandidate())
