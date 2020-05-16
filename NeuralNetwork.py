from Neuron import *
from NodeType import *


class NeuralNetwork:
    def __init__(self, genome):
        self.inputs = []
        self.outputs = []
        self.unprocessed = []

        self.neurons = {}

        for id in genome.nodes.keys():
            neuron = Neuron()
            n = genome.nodes[id]

            if n.type == NodeType.INPUT:
                neuron.addInput()
                self.inputs.append(id)
            elif n.type == NodeType.OUTPUT:
                self.outputs.append(id)

            self.neurons[id] = neuron

        for id in genome.connections.keys():
            c = genome.connections[id]
            if c.active:
                inputNeuron = self.neurons[c.inputNode]
                outputNeuron = self.neurons[c.outputNode]

                inputNeuron.addOutput(c.outputNode, c.weight)
                outputNeuron.addInput()

    def feedForward(self, inputValues):
        for id in self.neurons.keys():
            self.neurons[id].reset()

        self.unprocessed = []
        self.unprocessed.extend(self.neurons.values())

        for i in range(0, len(inputValues)):
            inputNeuron = self.neurons[self.inputs[i]]
            inputNeuron.addInputValue(inputValues[i])
            inputNeuron.calculateOutput()

            for j in range(len(inputNeuron.outputIDs)):
                outputNueron = self.neurons[inputNeuron.outputIDs[j]]
                outputNueron.addInputValue(inputNeuron.finalOutput * inputNeuron.outputWeights[j])

            self.unprocessed.remove(inputNeuron)

        attempts = 0
        while len(self.unprocessed) > 0:
            attempts += 1
            if attempts > 1000:
                return None

            duplicate = self.unprocessed.copy()
            for i in range(len(duplicate)):
                next = duplicate[i]
                if next.ready():
                    next.calculateOutput()
                    for j in range(len(next.outputIDs)):
                        outputId = next.outputIDs[j]
                        self.neurons[outputId].addInputValue(next.finalOutput * next.outputWeights[j])
                    self.unprocessed.remove(next)

        outputValues = []
        for i in range(len(self.outputs)):
            outputValues.append(self.neurons[self.outputs[i]].finalOutput)

        return outputValues
