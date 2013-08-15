'''Salinity Generator'''
import libtcodpy as tcod

def generateSaltmap(_map):
    print("Salinity Generation...");
    
    _sm = tcod.heightmap_new(_map.width, _map.height)
    
    for y in range(0, _map.height):
        for x in range(0, _map.width):
            
            #very crude "distance from ocean" simulation
            toOcean = _map.distanceToOcean(x,y);
            if toOcean < 1:
                salinity = 255
            else:
                salinity = 255/toOcean
    
    tcod.heightmap_normalize(_sm, 0, 255)
    
    for y in range(0, _map.height):
        for x in range(0, _map.width):
            _map.coords[x][y].setSalinity(tcod.heightmap_get_value(_sm, x, y))
    
    return True