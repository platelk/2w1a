import wheelandarm
import argparse
import genalgo
import robot
import sys

if __name__ == '__main__':
    loadfile = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--load", help = "saved file you want to load")
    args = parser.parse_args()

    if args.load:
      loadfile = args.load

    vclient = robot.VRepClient()
    #vclient.stopSimulation()

    robot = robot.Robot(vclient)

    algo = genalgo.GenAlgo(lambda: wheelandarm.createWheelCandidate(robot), wheelandarm.positionFitness, loadfile=loadfile, nbPopulate=2)
    algo.run()

    #sys.stdin.readline()

    vclient.stopSimulation()
    vclient.disconnect()
