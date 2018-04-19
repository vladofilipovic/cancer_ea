# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from ga_node import GaNode, initGaNodeIndividual, mutationGaNode

import random

random.seed( 111133 )
      
x = initGaNodeIndividual(GaNode, ['a','b','c','d','e'], 10)  
x.treePrint() 

y = initGaNodeIndividual(GaNode, ['a','b','c','d','e'], 10)  
y.treePrint() 

z = initGaNodeIndividual(GaNode, ['a','b','c','d','e'], 10)  
z.treePrint() 

mutationGaNode(z)
