import vrep
import math

class VRepClient:
    def __init__(self, ip='127.0.0.1', port=19997):
        # Close eventual old connections
        vrep.simxFinish(-1)
        # Connect to V-REP remote server
        self.clientID = vrep.simxStart(ip, port, True, True, 5000, 5)

    def isConnected(self):
        return self.clientID != -1

    def getHandler(self, name):
        return vrep.simxGetObjectHandle(self.clientID, name, self.opmode)

    def getObjectPosition(self, object):
        return vrep.simxGetObjectPosition(self.clientID, object, -1, vrep.simx_opmode_streaming)

    def getObjectOrientation(self, object):
        return vrep.simxGetObjectOrientation(self.clientID, object, -1, vrep.simx_opmode_buffer)

    def getJointObjectPosition(self, object):
        return vrep.simxGetJointPosition(self.clientID, object, self.opmode)

    def setJointObjectPosition(self, object, rotation):
        return vrep.simxSetJointTargetPosition(self.clientID, object, math.radians(rotation), self.opmode)

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

    def position(self):
        return self.vrep_client.getObjectPosition(self.robot)

    def orientation(self):
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
        self.state, self.handler = self.vrep_client.getHandler(self.name)
        return self.state

    def setRotation(self, rotation):
        self.rotation = rotation
        return self.vrep_client.setJointObjectPosition(self.handler, rotation)

    def is_handler_ok(self):
        return self.state == 0
