import math


class Neuron:
    def __init__(self):
        self.finalOutput = 0
        self.inputValues = []
        self.outputWeights = []
        self.outputIDs = []

    def addOutput(self, id, weight):
        self.outputWeights.append(weight)
        self.outputIDs.append(id)

    def ready(self):
        for f in self.inputValues:
            if f is None:
                return False

        return True

    def addInput(self):
        self.inputValues = [None for _ in range(len(self.inputValues) + 1)]

    def calculateOutput(self):
        outputSum = 0
        for f in self.inputValues:
            outputSum += f

        self.finalOutput = self.sigmoid(outputSum)

    def sigmoid(self, x):
        return 1 / (1 + math.e ** (-1 * x))

    def addInputValue(self, input):
        for i in range(len(self.inputValues)):
            if self.inputValues[i] is None:
                self.inputValues[i] = input
                break

    def reset(self):
        self.finalOutput = 0
        self.inputValues = [None for _ in range(len(self.inputValues))]
