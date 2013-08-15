import Generators
import libtcodpy as tcod
import map
import sys
import time

#TODO: make the generator a member of the map class, 
#       and call generate() from ie: map.generateTerrain()
class Generator:
    
    def __init__(self, mode):
        
        self._hmGenerator = Generators.getGenerator(mode)
        
        self._tempGenerator = Generators.tempGenerator
        self._salinityGenerator = Generators.salinityGenerator
        self._rainGenerator = Generators.rainGenerator
        self._rand = tcod.random_get_instance()
    #end __init__
    
    def generate(self, _map):
        
        print("Generating!")
        start = time.time();
        self._hmGenerator.generateHeightmap(_map)
        print("Took[" + str(time.time() - start) + "]ms")
        start = time.time();
        self._tempGenerator.generateTempmap(_map)
        print("Took[" + str(time.time() - start) + "]ms")
        start = time.time();
        self._salinityGenerator.generateSaltmap(_map)
        print("Took[" + str(time.time() - start) + "]ms")
        start = time.time();
        self._rainGenerator.generateRainmap(_map)
        print("Took[" + str(time.time() - start) + "]ms")
        start = time.time();
        _map.setBiomes();
        print("Took[" + str(time.time() - start) + "]ms")
        start = time.time();
        self._locateSprings(_map);
        print("Took[" + str(time.time() - start) + "]ms")
        start = time.time();
        self._runRivers(_map);
        print("Took[" + str(time.time() - start) + "]ms")
        start = time.time();
        self._identifyLakes(_map);
        print("Took[" + str(time.time() - start) + "]ms")
        
        _map.setColors()
        return _map;

    #end generate
    
    def _locateSprings(self, _map):
        
        print("Locating Springs...");
        
        for i in range(0, (_map.width * _map.height) / 300 ):
            
            x = tcod.random_get_int(self._rand, 0, _map.width - 1);
            y = tcod.random_get_int(self._rand, 0, _map.height - 1);
            
            if (_map.getBiome(x, y) == 'Desert' ):
                continue
            
            _map.addSpring(x, y);
        
        return True;
    #end _locateSprings
    
    def _runRivers(self, _map):
        print("Running Rivers...");
        
        for coord in _map.getSprings():
            (x, y) = coord
            
            depth = _map.getDepth(x,y)
            river = [(x,y)]
            
            while _map.coords[x][y].altitude > 0 and depth > 0:
                (newx, newy, dug, newAlt) = self._determineLowestNeigbour(x, y, river, _map)
                
                if (newx, newy) != (x, y) and newAlt > 0:
                    
                    river.append( (newx,newy) )
                    #subtract the difference, if any that we might have dug our neighbour
                    if dug > 0:
                        #leave at least one depth
                        depth = max(1, depth - dug)
                        
                    _map.addRiver(newx,newy,x,y,depth)
                    (x, y) = (newx, newy)
                    
                else:
                    break
            
        return True;
    #end _runRivers
    
    # Find the lowest neighbour, if its altitude is greater than ours, dig it down to our level
    def _determineLowestNeigbour(self, x, y, river, _map):
        curAlt = _map.coords[x][y].altitude
        minAlt = 16383
        neighbour = (x, y)
        
        dig = True
        for iy in range(max(0, y-1), min(_map.height, y+2)):
            for ix in range(max(0, x-1), min(_map.width, x+2)):
                
                if (ix, iy) == (x, y):
                    continue;
                
                if (ix, iy) in river:
                    continue;
                
                checkAlt = _map.heightmap(ix,iy)
                if  checkAlt < minAlt:
                    minAlt = checkAlt
                    neighbour = (ix,iy);
                if _map.heightmap(ix,iy) < curAlt:
                    dig = False;
                
                dug = 0
        newAlt = _map.heightmap(neighbour[0], neighbour[1])
        
        if ( dig ):
            oldAlt = _map.coords[x][y].altitude
            dug = newAlt - oldAlt
            _map.coords[neighbour[0]][neighbour[1]].setAltitude(curAlt);
        
        return (neighbour[0], neighbour[1], dug, newAlt)
    #end _determineLowestNeigbour
    
    def _identifyLakes(self,_map):
        print("Identifying Lakes...")
        # Loop on all tiles, rivers with three or more river(orLake) neighbours are lakes
        for x in range(len(_map.coords)):
            for y in range(len(_map.coords[x])):
                
                c = _map.coords[x][y]
                
                if not c.isRiver:
                    continue
                
                if c.countRiverNeighbours(True, True) >= 3:
                    _map.addLake(c.x(), c.y())
        
        # Loop a second time and identify coords with two or more neighbouring lake tiles
        for x in range(len(_map.coords)):
            for y in range(len(_map.coords[x])):
                
                c = _map.coords[x][y]
                
                if not c.isRiver:
                    continue
                if c.countLakeNeighbours() >= 2:
                    _map.addLake(c.x(), c.y())
        
    #end _identifyLakes
    