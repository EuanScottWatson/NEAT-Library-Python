class InnovationNumber:
    def __init__(self):
        self.innovationNo = 0

    def getInnovationNo(self):
        self.innovationNo += 1
        return self.innovationNo - 1
