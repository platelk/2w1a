import vrep
import math

class VRepClient:
    def __init__(self, ip='127.0.0.1', port=19997):
        # Close eventual old connections
        vrep.simxFinish(-1)

        self.clientID = -1
        self.opmode = vrep.simx_opmode_oneshot_wait
        # Connect to V-REP remote server
        self.connect(ip, port)

    def connect(self, ip='127.0.0.1', port=19997):
        self.clientID = vrep.simxStart(ip, port, True, True, 5000, 5)
        self.startSimulation()

    def startSimulation(self):
        vrep.simxStartSimulation(self.clientID, self.opmode)

    def isConnected(self):
        return self.clientID != -1

    def getHandler(self, name):
        _, handler = vrep.simxGetObjectHandle(self.clientID, name, self.opmode)
        return handler

    def getObjectPosition(self, obj):
        ret, val = vrep.simxGetObjectPosition(self.clientID, obj, -1, vrep.simx_opmode_streaming)
        return val

    def getObjectOrientation(self, obj):
        ret, val = vrep.simxGetObjectOrientation(self.clientID, obj, -1, vrep.simx_opmode_buffer)
        return val

    def setObjectPosition(self, obj, position):
        return vrep.simxSetObjectPosition(self.clientID, obj, -1, position, vrep.simx_opmode_streaming)

    def setObjectOrientation(self, obj, orientation):
        return vrep.simxSetObjectOrientation(self.clientID, obj, -1, orientation, vrep.simx_opmode_buffer)

    def getJointObjectPosition(self, obj):
        return vrep.simxGetJointPosition(self.clientID, obj, self.opmode)

    def setJointObjectPosition(self, obj, rotation):
        return vrep.simxSetJointTargetPosition(self.clientID, obj, math.radians(rotation), self.opmode)

    def waitUntilAvailable(self):
        # Communication operating mode with the remote API : wait for its answer before continuing (blocking mode)
        # http://www.coppeliarobotics.com/helpFiles/en/remoteApiConstants.htm
        self.opmode = vrep.simx_opmode_oneshot_wait
        return self.opmode

    def stopSimulation(self):
        vrep.simxStopSimulation(self.clientID, self.opmode)

    def disconnect(self):
        vrep.simxFinish(self.clientID)


class Robot:
    def __init__(self, vrep_client):
        self.vrep_client = vrep_client
        self.arm = Arm(vrep_client)
        self.robot = vrep_client.getHandler("2W1A")
        self.savePosition = self.position()
        self.saveOrientation = self.orientation()

    def position(self, pos=None):
        if pos is not None:
            self.vrep_client.setObjectPosition(self.robot, pos)
        return self.vrep_client.getObjectPosition(self.robot)

    def orientation(self, orientation=None):
        if orientation is not None:
            self.vrep_client.setObjectOrientation(self.robot, orientation)
        return self.vrep_client.getObjectOrientation(self.robot)


class Arm:
    def __init__(self, vrep_client):
        self.vrep_client = vrep_client
        self.wrist = Motor(vrep_client, 'WristMotor')
        self.elbow = Motor(vrep_client, 'ElbowMotor')
        self.shoulder = Motor(vrep_client, 'ShoulderMotor')


class Motor:
    def __init__(self, vrep_client, name):
        self.name = name
        self.vrep_client = vrep_client
        self.handler = None
        self.state = 42
        self.rotation = 0
        self.connect()

    def connect(self):
        self.handler = self.vrep_client.getHandler(self.name)
        return self

    def setRotation(self, rotation):
        self.rotation = rotation
        return self.vrep_client.setJointObjectPosition(self.handler, rotation)

    def is_handler_ok(self):
        return self.state == 0
