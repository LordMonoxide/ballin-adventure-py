FAULTLINE = 1
PARTICLE = 2
DIAMOND_SQUARE = 3

import particleDepositionGenerator
import diamondSquareGenerator
import tempGenerator
import salinityGenerator
import rainGenerator

def getGenerator(mode, options = {}):
    
    if (mode == FAULTLINE):
        return faultLineGenerator
    
    elif (mode == PARTICLE):
        return particleDepositionGenerator
    
    elif (mode == DIAMOND_SQUARE):
        return diamondSquareGenerator
    
    
