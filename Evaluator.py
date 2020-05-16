from Genome import *
from Species import *
from GenomeFitnessPair import *


def getRandomGenome(species):
    totalFitness = 0
    for gf in species.fitnessPairs:
        totalFitness += gf.fitness

    targetFitness = random.random() * totalFitness
    runningFitness = 0

    for gf in species.fitnessPairs:
        runningFitness += gf.fitness
        if targetFitness < runningFitness:
            return gf.genome


def evaluateGenome():
    return 0


class Evaluator:
    def __init__(self, populationSize, starter, nodeInnovation, connectionInnovation):
        self.nodeInnovation = nodeInnovation
        self.connectionInnovation = connectionInnovation
        self.populationSize = populationSize
        self.config = Configuration()

        self.highestScore = 0
        self.bestGenome = None

        self.population = []
        self.species = []

        for i in range(populationSize):
            self.population.append(Genome(starter))

        self.nextGeneration = []
        self.speciesMap = {}
        self.fitnessMap = {}

    def evaluate(self):
        for s in self.species:
            s.resetSpecies()

        self.speciesMap = {}
        self.fitnessMap = {}
        self.nextGeneration = []

        for g in self.population:
            foundSpecies = False
            for s in self.species:
                if Genome.compatibilityDistance(g, s.leader, self.config.C1, self.config.C2,
                                                self.config.C3) < self.config.DISTANCE_THRESHOLD:
                    s.population.append(g)
                    self.speciesMap[g] = s
                    foundSpecies = True
                    break

            if not foundSpecies:
                newSpecies = Species(g)
                self.species.append(newSpecies)
                self.speciesMap[g] = newSpecies

        for s in self.species:
            if len(s.population) == 0:
                self.species.remove(s)

        for g in self.population:
            s = self.speciesMap[g]
            fitness = evaluateGenome() / len(s.population)
            newPair = GenomeFitnessPair(g, fitness)

            s.addFitness(fitness)
            s.fitnessPairs.append(newPair)
            self.fitnessMap[g] = fitness

            if fitness > self.highestScore:
                self.highestScore = fitness
                self.bestGenome = g

        self.nextGeneration.append(self.bestGenome)

        for s in self.species:
            s.sortPairs()
            self.nextGeneration.append(s.fitnessPairs[0].genome)
            if len(s.fitnessPairs) > 2:
                self.nextGeneration.append(s.fitnessPairs[1].genome)

        while len(self.nextGeneration) < self.populationSize:
            found = False

            s1 = self.getRandomSpecies()
            s2 = self.getRandomSpecies()

            p1 = getRandomGenome(s1)
            p2 = getRandomGenome(s2)

            while not found:
                s1 = self.getRandomSpecies()
                s2 = self.getRandomSpecies()

                p1 = getRandomGenome(s1)
                p2 = getRandomGenome(s2)

                if p1 != self.bestGenome and p2 != self.bestGenome:
                    found = True

            if random.random() < self.config.MUTATION_WITHOUT_CROSSOVER:
                if self.fitnessMap[p1] > self.fitnessMap[p2]:
                    mutatedChild = Genome(p1)
                else:
                    mutatedChild = Genome(p2)

                mutatedChild.mutation()
                self.nextGeneration.append(mutatedChild)
            else:
                if self.fitnessMap[p1] > self.fitnessMap[p2]:
                    child = crossover(p1, p2)
                else:
                    child = crossover(p2, p1)

                if random.random < self.config.MUTATION_THRESHOLD:
                    child.mutation()
                if random.random < self.config.ADD_CONNECTION_MUTATION:
                    child.newConnectionMutation()
                if random.random < self.config.ADD_NODE_THRESHOLD:
                    child.newNodeMutation()

                self.nextGeneration.append(child)

        self.population = self.nextGeneration

    def getRandomSpecies(self):
        totalFitness = 0
        for s in self.species:
            totalFitness += s.totalFitness

        targetFitness = random.random() * totalFitness
        runningFitness = 0

        for s in self.species:
            runningFitness += s.totalFitness
            if (targetFitness < runningFitness):
                return s
