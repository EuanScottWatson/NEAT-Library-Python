import random
from CONFIG import *
from NodeType import *
from ConnectionGenome import *
from NodeGenome import *



class Genome:
    def __init__(self, starter=None):
        self.nodes = {}
        self.connections = {}
        self.config = Configuration()

        if starter:
            for i in starter.nodes.keys():
                self.nodes[i] = starter.nodes[i].copy()

            for i in starter.connections.keys():
                self.connections[i] = starter.connections[i].copy()

    def addNode(self, node):
        self.nodes[node.id] = node

    def addConnection(self, connection):
        self.connections[connection.id] = connection

    def mutation(self):
        for connection in self.connections.values():
            if random.random() < self.config.MUTATION_THRESHOLD:
                connection.setWeight(connection.weight * (random.random * 4 - 2))
            else:
                connection.setWeight(random.random * 4 - 2)

    def newConnectionMutation(self, connectionInnovation):
        keys = self.nodes.keys()
        node1 = self.nodes.get(random.choice(keys))
        node2 = self.nodes.get(random.choice(keys))

        weight = random.random() * 4 - 2

        if (node1.type == NodeType.HIDDEN and node2.type == NodeType.INPUT) or (
                node1.type == NodeType.OUTPUT and node2.type == NodeType.HIDDEN) or (
                node1.type == NodeType.OUTPUT and node2.type == NodeType.INPUT):
            node1, node2 = node2, node1

        if node1.type != node2.type:
            exists = False
            for connection in self.connections.values():
                if connection.inputNode == node1.id and connection.outputNode == node2.id:
                    exists = True
                    break

            if not exists:
                newConnection = ConnectionGenome(node1.id, node2.id, weight, True,
                                                 connectionInnovation.getInnovationNo())
                self.connections[newConnection.innovationNo] = newConnection

    def newNodeMutation(self, connectionInnovation, nodeInnovation):
        keys = self.connections.keys()
        connection = self.connections[random.choice(keys)]
        connection.disable()

        node1 = self.nodes[connection.inputNode]
        node2 = self.nodes[connection.outputNode]
        newNode = NodeGenome(NodeType.HIDDEN, nodeInnovation.getInnovationNo())

        connection1 = ConnectionGenome(node1.id, newNode.id, 1, True, connectionInnovation.getInnovationNo())
        connection2 = ConnectionGenome(newNode.id, node2.id, connection.weight, True, connectionInnovation.getInnovationNo())

        self.nodes[newNode.id] = newNode
        self.connections[connection1.innovationNo] = connection1
        self.connections[connection2.innovationNo] = connection2
