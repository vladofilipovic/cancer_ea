# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""


import random
import re, optparse

from bitstring import BitArray

from read_element import ReadElement

from ga_node import GaNode, initGaNodeIndividual, mutationGaNode

from deap import base
from deap import creator
from deap import tools


randomSeed_re = re.compile(r'[R|r]andom[S|s]eed=[0-9]+')
inputFile_re = re.compile(r'[I|i]nput[F|f]ile=.*\.in')

parser = optparse.OptionParser()
parser.set_defaults(debug=False,xls=False)
parser.add_option('--debug', action='store_true', dest='debug')
parser.add_option('--randomized', action='store_true', dest='randomized')
(options, args) = parser.parse_args()

if options.debug:
    print( 'option debug is activated')
if options.randomized:
    print ('option randomized is activated')

if options.debug:
   print("Command-line parameters are:", end=' ')
   for arg in args:
       print( arg, end = ' ')
   print()
   
if len(args) > 2:
    raise ValueError("Too many command line arguments.")
if len(args) <= 1:
    raise ValueError("Too few command line arguments.")  

parameters = {'InputFile': 'XXX.in', 'RandomSeed': 111}
if not randomSeed_re.match(args[0]) :
    if not randomSeed_re.match(args[1]):
        raise ValueError("One argument should be in form: 'randomSeed=DDD', where 'DDD' is postitive integer.")
    else:
        parameters['RandomSeed'] = args[1].split('=')[1]
else:
    parameters['RandomSeed'] = args[0].split('=')[1]
if not inputFile_re.match(args[0]):
    if not inputFile_re.match(args[1]):
        raise ValueError("One argument should be in form 'inputFile=XXX.in' where 'XXX' is file name.")
    else:
        parameters['InputFile'] = args[1].split('=')[1]
else:
    parameters['InputFile'] = args[0].split('=')[1]
if options.debug:
    print( 'Parameters: ', parameters)

if( not options.randomized ):
    random.seed( parameters['RandomSeed'])
 
fileInput = open(parameters['InputFile'], 'r')
textLine = fileInput.readline().strip()
while textLine.startswith("//") or textLine.startswith(";"):
    textLine = fileInput.readline()
labelsMutation = textLine.split()
if options.debug:
    print("Mutation labels (from input):\n", labelsMutation)
    
i = 1
textLine=fileInput.readline().strip()
reads = [];
while textLine!="":
    if textLine.startswith("//") or textLine.startswith(";"):
        textLine = fileInput.readline()
        continue
    bitLine = textLine.replace(" ", "")
    ba = BitArray(bin = bitLine)
    readElem = ReadElement(i, ba)
    reads.append(readElem)
    textLine=fileInput.readline().strip()
    i= i+1
if options.debug:
    print("Reads (from input):")
    for x in reads:
        x.printElement();

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", GaNode, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator 
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
toolbox.register("individual", initGaNodeIndividual, creator.Individual, labels=labelsMutation, size=10)
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





