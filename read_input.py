# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 22:37:58 2018

@author: vlado.filipovic
"""

from bitstring import BitArray

from read_element import ReadElement

def readLabelsReads(options, parameters):
    fileInput = open(parameters['InputFile'], 'r')
    textLine = fileInput.readline().strip()
    # skip comments
    while textLine.startswith("//") or textLine.startswith(";"):
        textLine = fileInput.readline()
    labels = textLine.split()        
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
    return(labels, reads)