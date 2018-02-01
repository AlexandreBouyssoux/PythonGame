# -*- coding: utf-8 -*-

# import
import sys
import TrainBot as tb

if __name__ == "__main__":
    argDict = tb.splitArgs(sys.argv)
    tb.createNewGeneration(int(argDict["generationNumber"])+1)
