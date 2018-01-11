# -*- coding: utf-8 -*-

# import
import numpy as np
import os
import GUI
import Bot


def loadGenSpeDirectory(generation=0, specie=0):
    """
    load the directory corresponding to generation X and specie Y
    """
    currentPath = os.getcwd()
    generationPath = os.path.join(currentPath,
                                  "GEN_{}".format(str(generation)))
    if not os.path.isdir(generationPath):
        os.makedirs(generationPath)
    speciePath = os.path.join(generationPath, "SPE_{}".format(str(specie)))
    if not os.path.isdir(speciePath):
        os.makedirs(speciePath)
    os.chdir(speciePath)


def createRandomWeigths(generation=0, specie=0):
    """
    create random matrix of weight for w1, w2 and w3.
    w1 is 10*7
    w2 is 10*10
    w3 is 3*10
    """
    loadGenSpeDirectory(generation, specie)

    w1 = np.random.rand(10, 7)
    w2 = np.random.rand(10, 10)
    w3 = np.random.rand(3, 10)

    np.savetxt("w1.txt", w1)
    np.savetxt("w2.txt", w2)
    np.savetxt("w3.txt", w3)


if __name__ == "__main__":
    createRandomWeigths()
