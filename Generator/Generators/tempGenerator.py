'''Temperature Generator'''
import libtcodpy as tcod


def generateTempmap(_map):
    print("Temperature Generation...")
    
    _rand = tcod.random_get_instance()
    _tm = tcod.heightmap_new(_map.width, _map.height)
    
    _altMap = tcod.heightmap_new(_map.width, _map.height)
    _latMap = tcod.heightmap_new(_map.width, _map.height)
    
    for y in range(0, _map.height):
        for x in range(0, _map.width):
            
            latitude = -int(180*y/_map.height - 90)
            latTemp = int(-(latitude*latitude)/51 + 128)
            
            tcod.heightmap_set_value(_latMap, x, y, latTemp)
            
            alt = _map.heightmap(x, y)
            
            if (alt > 0):
                # expect alt to peak out around 255-320
                altTemp = -alt/4
            else:
                altTemp = tcod.random_get_int(_rand,-10, 10)
                
            tcod.heightmap_set_value(_altMap, x, y, altTemp)
    
    tcod.heightmap_add_hm(_altMap, _latMap, _tm)
    
    
    tcod.heightmap_rain_erosion(
            _tm, 
            _map.width*_map.height/2,     #number of raindrops
            0.2,                        #erosion cooef (f)
            0.2)                        #sediment cooef (f)
    
    tcod.heightmap_normalize(_tm, -32, 128)
    
    dx = [-1,1,0]
    dy = [0,0,0]
    weight = [0.33,0.33,0.33]
    tcod.heightmap_kernel_transform(_tm,3,dx,dy,weight,-32,128);
    
    for y in range(0, _map.height):
        for x in range(0, _map.width):
            _map.coords[x][y].setTemp(tcod.heightmap_get_value(_tm, x, y))
    return True