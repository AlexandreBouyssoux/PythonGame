# -*- coding: utf-8 -*-

# import
import numpy as np
import sys
import os
import GUI
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.models import load_model


# constants
FIT_RECORD = "fitnessRecord.txt"
WINNER = "winner.txt"


# functions


def getGenDirectory(generation):
    currentPath = r"C:\Users\alexa\Documents\PythonProjects\TestJeux"
    generationPath = os.path.join(currentPath,
                                  "GEN_{}".format(str(generation)))
    if not os.path.isdir(generationPath):
        os.makedirs(generationPath)

    return generationPath


def loadGenDirectory(generation):
    """
    load the directory corresponding to generation X and specie Y
    """
    speciePath = getGenDirectory(generation)
    os.chdir(speciePath)


def createModel():
    model = Sequential()
    model.add(Dense(output_dim=15, input_dim=7))
    model.add(Activation("sigmoid"))
    model.add(Dense(output_dim=3))
    model.add(Activation("sigmoid"))
    sgd = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9,
                               nesterov=True)
    model.compile(loss="mse", optimizer=sgd, metrics=["accuracy"])
    return model


def createFirstGeneration(population=50):
    pool = []

    for i in range(population):
        model = createModel()
        pool.append(model)

    for indice, model in enumerate(pool):
        saveModel(model, generationNumber=0, specieNumber=indice)


def loadModel(generationNumber, specieNumber):
    loadGenDirectory(generationNumber)
    modelName = "_".join(["model", str(specieNumber)])
    model = load_model(modelName)
    return model


def saveModel(model, generationNumber, specieNumber):
    loadGenDirectory(generationNumber)
    modelName = "_".join(["model", str(specieNumber)])
    model.save(modelName)


def copyModel(lastGeneration, lastSpecie, newGeneration, newSpecie):
    model = loadModel(lastGeneration, lastSpecie)
    saveModel(model, newGeneration, newSpecie)


def modelMutate(model):
    weights = model.get_weights()
    for xi in range(len(weights)):
        for yi in range(len(weights[xi])):
            if np.random.uniform(0, 1) > 0.85:
                change = np.random.uniform(-0.5, 0.5)
                weights[xi][yi] += change
    model.set_weights(weights)
    return model


def crossOver(generationNumber, specieNumber1, specieNumber2):
    model1 = loadModel(generationNumber, specieNumber1)
    model2 = loadModel(generationNumber, specieNumber2)
    w_spe1 = model1.get_weights()
    w_spe2 = model2.get_weights()
    new_w1 = w_spe1
    new_w2 = w_spe2
    new_w1[0] = w_spe2[0]
    new_w2[0] = w_spe1[0]

    newModel1 = createModel()
    newModel2 = createModel()
    newModel1.set_weights(new_w1)
    newModel2.set_weights(new_w2)

    return newModel1, newModel2


def runGenerationSimulation(generationNumber, specie):
    directory = r"C:\Users\alexa\Documents\PythonProjects\TestJeux"
    directoryGen = getGenDirectory(generationNumber)
    GUI.main(generationNumber, specie)
    with open(os.path.join(directory, "fitness.txt")) as file:
        fitness = file.read()
    with open(os.path.join(directoryGen, FIT_RECORD), "a") as f:
        f.write(fitness + " ")


def createNewGeneration(generationNumber, population=50):
    """
    create a new generation of bot based on the old generation of bot
    """
    indice = list(range(population))
    np.random.shuffle(indice)
    compteur = 0
    c = 0
    listSpecies = []

    lastGenDirectory = getGenDirectory(generationNumber - 1)
    lastGenFitnessFilePath = os.path.join(lastGenDirectory, FIT_RECORD)
    with open(lastGenFitnessFilePath, "r") as file:
        data = file.read()
    lastGenerationFitness = data.split(" ")
    del lastGenerationFitness[-1]

    while len(listSpecies) < 20:
        specie = np.argmax(lastGenerationFitness)
        listSpecies.append(specie)
        del lastGenerationFitness[specie]
        copyModel(generationNumber-1, specie, generationNumber,
                  indice[compteur])
        compteur += 1

    while compteur < population:

        if c <= len(listSpecies) - 2:
            parentSpecie1 = listSpecies[c]
            parentSpecie2 = listSpecies[c+1]
            c += 2
        else:
            randomIndice1 = np.random.randint(len(listSpecies))
            randomIndice2 = np.random.randint(len(listSpecies))
            parentSpecie1 = listSpecies[randomIndice1]
            parentSpecie2 = listSpecies[randomIndice2]

        newModel1, newModel2 = crossOver(generationNumber-1, parentSpecie1,
                                         parentSpecie2)
        newModel1 = modelMutate(newModel1)
        newModel2 = modelMutate(newModel2)
        saveModel(newModel1, generationNumber, indice[compteur])
        saveModel(newModel2, generationNumber, indice[compteur+1])
        compteur += 2


def splitArgs(args):
    argDict = {}
    for arg in args:
        if "--" not in arg:
            continue
        if "generation" in arg:
            argDict["generationNumber"] = arg.split("=")[-1]
        elif "specie" in arg:
            argDict["specie"] = arg.split("=")[-1]
        else:
            print("error")
            sys.exit()
    return argDict


if __name__ == "__main__":
    dictArgs = splitArgs(sys.argv)
    # createFirstGeneration()
    runGenerationSimulation(dictArgs["generationNumber"], dictArgs["specie"])
