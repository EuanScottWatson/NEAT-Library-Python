from random import randint


class Species:
    def __init__(self, leader):
        self.leader = leader
        self.population = [leader]
        self.fitnessPairs = []
        self.totalFitness = 0

    def addFitness(self, fitness):
        self.totalFitness += fitness

    def resetSpecies(self):
        self.leader = self.population[randint(0, len(self.population) - 1)]
        self.population = []
        self.fitnessPairs = []
        self.totalFitness = 0

    def sortPairs(self):
        self.fitnessPairs.sort(key=lambda x: x.fitness, reverse=True)
