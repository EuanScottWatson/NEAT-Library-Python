class ConnectionGenome:

    def __init__(self, inputNode, outputNode, weight, active, innovationNo):
        self.inputNode = inputNode
        self.outputNode = outputNode
        self.weight = weight
        self.active = active
        self.innovationNo = innovationNo

    def copy(self):
        return ConnectionGenome(self.inputNode, self.outputNode, self.weight, self.active, self.innovationNo)

    def disable(self):
        self.active = False

    def setWeight(self, weight):
        self.weight = weight
