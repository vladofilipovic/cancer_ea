# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from bitstring import BitArray

from ga_node import GaNode

import random

random.seed( 111133 )
      
x = initIndividual(GaNode, ['a','b','c','d','e'], 10)  
x.printGaSubtree() 

y = initIndividual(GaNode, ['a','b','c','d','e'], 10)  
y.printGaSubtree() 

z = initIndividual(GaNode, ['a','b','c','d','e'], 10)  
z.printGaSubtree() 

mutation(z)
z.printGaSubtree() 
