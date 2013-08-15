'''Diamond-Square Generator'''

import libtcodpy as tcod

import sys
import math

def generateHeightmap(_map):
    
    _map.MAX_ALTITUDE = 320
    
    mpd_setCornerAltitudes(_map,-_map.MAX_ALTITUDE, _map.MAX_ALTITUDE);
    
    squares = _getSquares(_map);
    
    for sq in squares:
        maxDisp = mpd_maxDisplacement(_map, sq.gen)
        displace(_map, sq.left, sq.top, sq.right, sq.bottom, maxDisp)
        print ("Displacing[" + str( (sq.left, sq.top, sq.right, sq.bottom) ) + \
            "] gen[" + str(sq.gen) + "] max disp [" + str(maxDisp) + "]")
    
    #TODO: _map.smooth(matrixSize)
    
def _getSquares(_map):
    
    x1 = 0
    y1 = 0
    x2 = _map.width - 1
    y2 = _map.height - 1
    
    gen = 0
    
    squares = []
    first = True
    
    while ( True ):
        
        width = max(1, _map.width / 2**gen)
        height = max(1, _map.height / 2**gen)
        
        if ( width < 2 and height < 2 ):
            print("Exiting[" + str(width) + "," + str(height) + "]")
            break
        
        if ( first ):
            print ("Adding first[" + str( (0,0,_map.width - 1, _map.height - 1) ) + "]")
            squares.append(Square(0,0,_map.width - 1, _map.height - 1, 0))
            first = False
        
        for y1 in range(0, _map.height - height, height):
            for x1 in range(0, _map.width - width, width):
                
                x2 = x1 + width
                y2 = y1 + height
                
                #GOTCHA: we add 1 to gen here, so the squares start at generation 1
                squares.append(Square(x1, y1, x2, y2, gen + 1))
        
        gen += 1
    
    return squares


def rectify(val, max):
    if (val > max):
        val = max - (int)(tcod.random_get_float(0,0,1) * (max / 10))
    elif (val < (max * -1)):
        val = (max * -1) + (int)(tcod.random_get_float(0,0,1) * (max / 10))
    return val


def displace(_map,x1, y1, x2, y2, maxDisp):
    
    bigWidth = _map.width
    bigHeight = _map.height
    
    rectWidth = (x2 - x1) + 1;
    rectHeight = (y2 - y1) + 1;

    ###
    #Should probably only do the edges with the OR, do the center with an AND. check results.
    ###
    if (rectWidth > 2 or rectHeight > 2):
        
        
        # Altitudes at the corners of this rectangle
        tlAlt = _map.heightmap(x1, y1);
        trAlt = _map.heightmap(x2, y1);
        blAlt = _map.heightmap(x1, y2);
        brAlt = _map.heightmap(x2, y2);
        
        midAvg = (tlAlt + trAlt + brAlt + blAlt) / 4;
        midX = x1 + ((x2 - x1) / 2);
        midY = y1 + ((y2 - y1) / 2);
        
        #set random height for the midpoint...
        midAlt = rectify(mpd_getDisplacement(midAvg, maxDisp), _map.MAX_ALTITUDE);
        _map.setHeight(midX, midY, midAlt);
        
        #then the edges...clockwise from the top
        topAvg = mpd_edgeAverage(tlAlt, trAlt, midAlt);
        rgtAvg = mpd_edgeAverage(trAlt, brAlt, midAlt);
        btmAvg = mpd_edgeAverage(brAlt, blAlt, midAlt);
        lftAvg = mpd_edgeAverage(blAlt, tlAlt, midAlt);
        
        topAlt = rectify(mpd_getDisplacement(topAvg, maxDisp), _map.MAX_ALTITUDE);
        rgtAlt = rectify(mpd_getDisplacement(rgtAvg, maxDisp), _map.MAX_ALTITUDE);
        btmAlt = rectify(mpd_getDisplacement(btmAvg, maxDisp), _map.MAX_ALTITUDE);
        lftAlt = rectify(mpd_getDisplacement(lftAvg, maxDisp), _map.MAX_ALTITUDE);
        
        _map.setHeight(midX, y1, topAlt);
        _map.setHeight(x2, midY, rgtAlt);
        _map.setHeight(midX, y2, btmAlt);
        _map.setHeight(x1, midY, lftAlt);
    

def mpd_getDisplacement(avg, _max):
    disp = int((avg + (2 * ((tcod.random_get_float(0,0,1)) - .5) * _max)));
    return disp;

def mpd_edgeAverage(a, b, c):
    return ((a + b + c) / 3);

def mpd_maxDisplacement(_map, gen):
    _max = _map.MAX_ALTITUDE
    #maximum dimension
    _dim = max(_map.width, _map.height)
    _tg  = int(math.log(_dim, 2))
    
    maxDisp = max(1,_max - (gen * (_max/_tg)));
    
    return maxDisp

def mpd_setCornerAltitudes(_map, minAlt, maxAlt):
    print('Map w', _map.width, 'h', _map.height)
    
    _map.setHeight(0, 0, tcod.random_get_int(0,minAlt, maxAlt))
    _map.setHeight(_map.width - 1, 0, tcod.random_get_int(0,minAlt, maxAlt))
    _map.setHeight(_map.width - 1, _map.height - 1, tcod.random_get_int(0,minAlt, maxAlt))
    _map.setHeight(0, _map.height - 1, tcod.random_get_int(0,minAlt, maxAlt))



class Square:
    
    def __init__(self, left, top, right, bottom, gen):
        
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.gen = gen
    
