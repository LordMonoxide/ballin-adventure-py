'''Rainfall Generator'''

import libtcodpy as tcod
import math
import math


def generateRainmap(map):
    print("Rainfall Generation...");
    
    altMap = tcod.heightmap_new(map.width, map.height)
    latMap = tcod.heightmap_new(map.width, map.height)
    
    rainMap = tcod.heightmap_new(map.width, map.height)
    
    for y in range(0, map.height):
        for x in range(0, map.width):
            
            # Cosine wave, dipping to -5 at the poles and the tropics
            latRain = 40-(50*(math.cos(math.pi*y/(map.height/10))))
            tcod.heightmap_set_value(rainMap, x, y, latRain)
    
    tcod.heightmap_add_voronoi(rainMap, int(map.height * map.width / 256), 3, [0.1,0.1, 0.1] )
    
    tcod.heightmap_normalize(rainMap, 0,150)
    tcod.heightmap_clamp(rainMap, 0,100)
    
    for y in range(0, map.height):
        for x in range(0, map.width):
            
            map.setRain(x, y, tcod.heightmap_get_value(rainMap, x, y))