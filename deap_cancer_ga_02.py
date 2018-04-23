"""
This module is an entry  point of the application.

Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

import optparse
import random


from deap import base
from deap import creator
from deap import tools

from command_line import get_execution_parameters
from read_input import read_labels_reads
from ga_node import GaNode
from ga_node import init_ga_node_individual, evaluation_ga_node, mutation_ga_node
from ga_node import assign_reads_to_tree

def main():
    """
    This function is an entry  point of the application.
    """
    # reading command-line argumets and options
    parser = optparse.OptionParser()
    parser.set_defaults(debug=False,xls=False)
    parser.add_option('--debug', action='store_true', dest='debug')
    parser.add_option('--randomized', action='store_true', dest='randomized')
    (options, args) = parser.parse_args()
    
    # obtaining execution paramters
    parameters = get_execution_parameters(options, args)
    if(options.debug):
        print("Execution parameters: ", parameters);
    
    # seeding random process
    if( not options.randomized ):
        random.seed(parameters['RandomSeed'])
     
    # reading read elements from input file
    (labels, reads) = read_labels_reads(options, parameters)
    if( options.debug):
        print("Mutatuion labels:", labels);
        print("Reads (from input):")
        for x in reads:
            print(x);
    
    # create fitness function
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # create strucute of the individual
    creator.create("Individual", GaNode, fitness=creator.FitnessMax)
    
    # create toolbox for execution of the genetic algorithm
    toolbox = base.Toolbox()
    
    # register bolean attribute to toolbbox 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # register individual creation to toolbbox 
    toolbox.register("individual", 
                     init_ga_node_individual, 
                     creator.Individual, 
                     labels=labels, 
                     size=3 * len(labels))
    # register mutation operator to toolbbox 
    toolbox.register("mutate", mutation_ga_node)
    # register population to toolbbox 
    toolbox.register("population", 
                     tools.initRepeat, 
                     list, 
                     toolbox.individual)
 
    # register evaluation function
    toolbox.register("evaluate", evaluation_ga_node, reads)

    # register the crossover operator
    toolbox.register("mate", tools.cxTwoPoint)
    
    # register a mutation operator with a probability to
    # flip each attribute/gene of 0.05
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    
    # operator for selecting individuals for breeding the next
    # generation: each individual of the current generation
    # is replaced by the 'fittest' (best) of three individuals
    # drawn randomly from the current generation.
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()



