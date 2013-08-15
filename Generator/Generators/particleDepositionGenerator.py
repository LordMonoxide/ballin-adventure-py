'''Particle Deposition Generator'''
import libtcodpy as tcod
import math

#continent size 1 - 10
CONT_SIZE = 8

def generateHeightmap(_map):
    print("Particle Deposition Generation...");
    
    _rand = tcod.random_get_instance()
    _hm = tcod.heightmap_new(_map.width, _map.height)
    
    #half-width and -height
    _hw = _map.width / 2
    _hh = _map.height / 2
    
    #quarter-width and -height
    _qw = _map.width / 4
    _qh = _map.height / 4
    
    #define our four "continental centers"
    _continents = [
        (_qw, _qh),                             #top-left
        (_map.width - _qw, _qh),                #top-right
        (_qw, _map.height - _qh),               #btm-left
        (_map.width - _qw, _map.height - _qh)]  #btm-right
    
    print("Continents:", _continents)
    
    _avg = min(_map.width, _map.height)
    
    _maxHillHeight = _avg / 4
    _maxHillRad = _avg / 8
    _iterations = _avg * 32
    
    for i in range(0,_iterations):
        
        _quadrant = tcod.random_get_int(_rand, 0, 3)
        
        _qx = _continents[_quadrant][0]
        _qy = _continents[_quadrant][1]
        
        _minX = _qx - ((_qw * CONT_SIZE) / 10)
        _maxX = _qx + ((_qw * CONT_SIZE) / 10)
        
        _minY = _qy - _qh
        _maxY = _qy + _qh
        
        x = tcod.random_get_int(_rand, _minX, _maxX)
        y = tcod.random_get_int(_rand, _minY, _maxY)
        
        
        height = tcod.random_get_int(_rand, -1*_maxHillHeight, _maxHillHeight)
        rad = tcod.random_get_int(_rand, 0, _maxHillRad)
        
        tcod.heightmap_add_hill(_hm, x, y, rad, height)
    
    #"dig out" the space  around the edge of the map
    x = _hw
    for y in range(0, _map.height, max(1,_maxHillRad / 8)):
        
        height = tcod.random_get_int(_rand, _maxHillHeight/-2, -1*_maxHillHeight)
        rad = tcod.random_get_int(_rand, 0, _maxHillRad*2)
        
        tcod.heightmap_add_hill(_hm, 0, y, rad, height)
        tcod.heightmap_add_hill(_hm, _map.width-1, y, rad, height)
    
    for x in range(0, _map.width, max(1,_maxHillRad / 4)):
        
        height = tcod.random_get_int(_rand, _maxHillHeight/-2, -1*_maxHillHeight)
        rad = tcod.random_get_int(_rand, 0, _maxHillRad*2)
        
        tcod.heightmap_add_hill(_hm, x, 0, rad, height)
        tcod.heightmap_add_hill(_hm, x, _map.height-1, rad, height)
    
    tcod.heightmap_rain_erosion(
            _hm, 
            _map.width*_map.height,     #number of raindrops
            0.2,                        #erosion cooef (f)
            0.2)                          #sediment cooef (f)
    
    _dx = [-2,-1,0,1,2]
    _dy = [-2,-1,0,1,2]
    _weight = [0.1,0.1,0.2,0.3,0.3]
    
    tcod.heightmap_kernel_transform(_hm, 5, _dx, _dy, _weight, -64, 255)
    
    tcod.heightmap_normalize(_hm, -255, 392)
    for y in range(0, _map.height):
        for x in range(0, _map.width):
            _map.coords[x][y].setAltitude(tcod.heightmap_get_value(_hm, x, y))
    
    return True