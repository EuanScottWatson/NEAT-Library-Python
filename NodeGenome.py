class NodeGenome:
    def __init__(self, type, id):
        self.type = type
        self.id = id

    def copy(self):
        return NodeGenome(self.type, self.id)
