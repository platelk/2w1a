from genalgo import *
import numpy


def bitfield(n, l=9):
    return [n >> i & 1 for i in range(l,-1,-1)]


class RobotOperation(Candidate):
    def __init__(self, robot, motorToMove=1, rotation=180, DNA=None):
        Candidate.__init__(self)
        self.operation = None
        self.robot = robot
        self.motorToMove = motorToMove
        self.rotation = rotation
        if DNA is not None:
            self.setDNA(DNA)

    def getMotorToMove(self):
        return [self.robot.arm.elbow, self.robot.arm.shoulder, self.robot.arm.wrist][self.motorToMove%3]

    def do(self):
        self.getMotorToMove().setRotation(self.rotation)

    def getDNA(self):
        return [bitfield(self.motorToMove, 1), bitfield(self.rotation, 8)]

    def setDNA(self, DNA):
        self.motorToMove = int(''.join([str(e) for e in DNA[0]]), base=2)
        self.rotation = int(''.join([str(e) for e in DNA[1]]), base=2)

    def copy(self, DNA=None):
        return RobotOperation(self.robot, self.motorToMove, self.rotation, DNA)


class StepCandidate(Candidate):
    def __init__(self, robot, generateOperations=True):
        Candidate.__init__(self)
        self.robot = robot
        self.operations = []
        if generateOperations:
            for i in range(numpy.random.randint(10)+3):
                self.operations.append(RobotOperation(robot, numpy.random.randint(3), numpy.random.randint(340)))

    def getDNA(self):
        return [dna.getDNA() for dna in self.operations]

    def setDNA(self, DNA):
        self.operations = [RobotOperation(self.robot, DNA=operation) for operation in DNA]

    def copy(self, DNA=None):
        tmp = StepCandidate(self.robot)
        tmp.operations = [op.copy() for op in self.operations]
        return tmp

    def do(self):
        for o in self.operations:
            o.do()


def createWheelCandidate(robot):
    return StepCandidate(robot)


def positionFitness(candidate):
    return candidate.robot.position()
