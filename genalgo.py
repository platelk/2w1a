import random
import numpy

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


def middleCrossOver(dna1, dna2):
    cdna1 = []
    cdna2 = []

    def mixList(l1, l2):
        tmp = []
        tmp.extend(l1[:(len(l1)/2)])
        tmp.extend(l2[(len(l1)/2):])
        return tmp

    for operation1, operation2 in zip(dna1, dna2):
        print operation1, operation2
        cdna1.append([mixList(operation1[0], operation2[0]), mixList(operation1[1], operation2[1])])
        cdna2.append([mixList(operation2[0], operation1[0]), mixList(operation2[1], operation1[1])])

    if len(cdna1) < len(dna1) or len(cdna2) < len(dna2):
        def expandDNA(cdna, dna):
            for o in dna[len(cdna):]:
                if numpy.random.randint(4) > 1:
                    cdna.append(o)
        expandDNA(cdna1, dna1)
        expandDNA(cdna2, dna2)


    return cdna1, cdna2


def randomSelection(candidate, population):
    return candidate, population[numpy.random.randint(len(population))]


class GenAlgo:
    def __init__(self, createCandidate, fitness, nbPopulate=5, crossOverFct=middleCrossOver, selection=randomSelection):
        self.createCandidate = createCandidate
        self.fitness = fitness
        self.populations = []
        self.nbPopulate = nbPopulate
        self.crossOverFct = crossOverFct
        self.selection = selection

    def createPopulation(self):
        population = []
        for i in range(self.nbPopulate):
            population.append(self.createCandidate())
        self.populations.append(population)

    def crossOver(self, candidate1, candidate2):
        dna1, dna2 = self.crossOverFct(candidate1.getDNA(), candidate2.getDNA())

        child1 = candidate1.copy()
        child1.setDNA(dna1)
        child2 = candidate2.copy()
        child2.setDNA(dna2)

        return child1, child2

    def sortCandidate(self):
        return sorted(self.populations[-1], key=self.fitness)
        #return self.populations[-1]

    def run(self, it=5, state={}):
        self.createPopulation()
        for i in range(it):
            self.sortCandidate()
            newGeneration = []
            for c in self.populations[-1]:
                print c.getDNA()
                print "---"
                c1, c2 = self.selection(c, self.populations[-1])
                child1, child2 = self.crossOver(c1, c2)
                newGeneration.append(child1)
            print "================="
            newGeneration[0].do()
            self.populations.append(newGeneration)
