# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""
import optparse

from command_line import getExecutionParameters

import random

from read_input import readLabelsReads

from ga_node import GaNode
from ga_node import initGaNodeIndividual, mutationGaNode

from deap import base
from deap import creator
from deap import tools


parser = optparse.OptionParser()
parser.set_defaults(debug=False,xls=False)
parser.add_option('--debug', action='store_true', dest='debug')
parser.add_option('--randomized', action='store_true', dest='randomized')
(options, args) = parser.parse_args()

parameters = getExecutionParameters(options, args)
if(options.debug):
    print("Execution parameters: ", parameters);

if( not options.randomized ):
    random.seed(parameters['RandomSeed'])
 
(labels, reads) = readLabelsReads(options, parameters)
if( options.debug):
    print("Mutatuion labels:", labels);
    print("Reads (from input):")
    for x in reads:
        x.printElement();

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", GaNode, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# attribute generator 
toolbox.register("attr_bool", random.randint, 0, 1)

# structure initializers
toolbox.register("individual", initGaNodeIndividual, creator.Individual, labels=labels, size=2*len(labels))
toolbox.register("mutate", mutationGaNode)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

test_ind = toolbox.individual()
print( test_ind )
if(issubclass(type(test_ind), GaNode)):
    print( "Class Individual is sublass of class GaNode")
else:
    print( "Class Individual is NOT sublass of class GaNode")
    
#test_ind.fitness.values = (12, 0)
toolbox.mutate(test_ind)





