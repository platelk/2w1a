import wheelandarm
import genalgo
import robot
import sys

if __name__ == '__main__':
    vclient = robot.VRepClient()
    vclient.waitUntilAvailable()

    robot = robot.Robot(vclient)

    algo = genalgo.GenAlgo(lambda: wheelandarm.createWheelCandidate(robot), wheelandarm.positionFitness)
    algo.run()

    sys.stdin.readline()

    vclient.stopSimulation()
    vclient.disconnect()


