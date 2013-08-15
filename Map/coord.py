import libtcodpy as tcod
import sys
import biome

class Coord:
    
    
    def __init__(self, x, y, map):
        
        self._x = x
        self._y = y
        
        self._map = map
        
        self.altitude = None
        self.temp     = None
        self.salinity = None
        self.rainfall = None
        self.biome = None
        
        self.hasSpring = False;
        self.isRiver = False;
        self.source = False;
        self.isLake = False;
        self.depth = 0;
        
        self.char = ' '
        self.fgColor = tcod.white
        
    
    def x(self):
        return self._x
    def y(self):
        return self._y
    
    def fg(self):
        return self.fgColor
    def bg(self):
        return self.bgColor
    
    def setAltitude(self,val):
        self.altitude = int(val)
    def setTemp(self,val):
        self.temp = int(val)
    def setSalinity(self,val):
        self.salinity = int(val)
    def setRain(self,val):
        self.rainfall = int(val)
    
    def addSpring(self):
        self.hasSpring = True;
        self.depth = tcod.random_get_int(0,1,100);
        self.source = (self._x, self._y)
        
        self.char = tcod.CHAR_RADIO_SET
        self.fgColor = tcod.cyan
        
    def addRiver(self,x,y,sourceX, sourceY, depth):
        self.isRiver = True
        self.depth += depth
        self.source = (sourceX, sourceY)
        
        self.char = '~'
        self.fgColor = tcod.blue
    
    def addLake(self):
        self.isRiver = False
        self.isLake = True
        
        self.char = '~'
        self.fgColor = tcod.blue
        
    def setColors(self):
        self._setBgColor()
        self._setTempColor()
        self._setRainColor()
        self._setSaltColor()
        self._setBiomeColor()
    
    def _setBgColor(self):
        
        if ( self.altitude <= 0 ):
            color = tcod.Color(0, 0, max(255 + self.altitude, 64))
        elif ( self.isLake ):
            color = tcod.dark_blue
        else:
            color = tcod.Color(min(255, self.altitude), min(64 + self.altitude, 255), min(255,self.altitude));
        
        self.bgColor = color
    
    def _setTempColor(self):
        
        #orange[255,128,0]@(64) -> red[255,0,0]@(128)
        if self.temp >= 64:
            color = tcod.Color(255, min(255, 256 - 2 * (self.temp)), 0)
        
        #white[255,255,255]@(32) -> orange[255,128,0]@(64)
        elif self.temp >= 32:
            color = tcod.Color(255, 255 - (4 * (self.temp - 32)), 255 - 8 * (self.temp - 32))
        
        #full blue[0,0,255]@(-32) -> white[255,255,255]@(32)
        elif self.temp >= -32:
            color = tcod.Color( min(255, 4 * (32 + self.temp)), min(255,4 * (32 + self.temp)), 255)
        else:
            color = tcod.Color(0,0,255)
        
        self.tempColor = color
    
    def _setSaltColor(self):
        
        color = tcod.Color(self.salinity, 255, self.salinity)
        
        self.saltColor = color
    
    def _setRainColor(self):
        temp = self.temp
        precip = self.rainfall
        
        if temp > 32:
            #rain above freezing
            color = tcod.Color(0, 0, int(precip*2.55))
        else:
            #snow below
            color = tcod.Color(int(precip*2.55),int(precip*2.55),int(precip*2.55))
        
        self.rainColor = color
    
    def _setBiomeColor(self):
        
        self.biomeColor = self.biome.overlayColor
    
    def calculateBiome(self):
        
        # Below sea level
        if ( self.altitude <= 0 ):
            if ( self.temp >= 32 ):
                self.biome = self._map.biomes[self._map.BIOME_OCEAN]
            else:
                self.biome = self._map.biomes[self._map.BIOME_FROZEN_OCEAN]
        
        # Aboce tree-line
        elif ( self.altitude > self._map.TREE_LINE ):
            self.biome = self._map.biomes[self._map.BIOME_MOUNTAIN]
        
        # Hot Biomes
        elif ( self.temp >=  96 ):
            if ( self.rainfall >= 66 ):
                self.biome = self._map.biomes[self._map.BIOME_RAIN_FOREST]
                
            elif ( self.rainfall >= 32):
                self.biome = self._map.biomes[self._map.BIOME_TROPICAL]
            
            elif ( self.rainfall >= 10):
                self.biome = self._map.biomes[self._map.BIOME_SAVANNA]
            
            else:
                self.biome = self._map.biomes[self._map.BIOME_DESERT]
            
        # Warm Biomes
        elif ( self.temp >=  48):
            if ( self.rainfall >= 66):
                self.biome = self._map.biomes[self._map.BIOME_FOREST]
            
            elif ( self.rainfall >= 24):
                self.biome = self._map.biomes[self._map.BIOME_WOODLAND]
            
            elif ( self.rainfall >= 10):
                self.biome = self._map.biomes[self._map.BIOME_PLAINS]
            else:
                self.biome = self._map.biomes[self._map.BIOME_DESERT]
        
        # Temperate Biomes
        elif ( self.temp >=  32):
            if ( self.rainfall >= 66 ):
                self.biome = self._map.biomes[self._map.BIOME_FOREST]
            
            elif ( self.rainfall >= 10 ):
                self.biome = self._map.biomes[self._map.BIOME_BOREAL]
            
            else:
                self.biome = self._map.biomes[self._map.BIOME_BADLANDS]
        
        # Cold Biomes
        else:
            if ( self.rainfall >= 24 ):
                self.biome = self._map.biomes[self._map.BIOME_ARCTIC]
            
            else:
                self.biome = self._map.biomes[self._map.BIOME_TUNDRA]
            
        
        # Finally, determine whether or not to display a tree on the world map
        if ( not self.isLake and not self.isRiver and not self.hasSpring and
             tcod.random_get_int(0,1,100) <= self.biome.treeDensity):
            self.char = self.biome.treeChar;
            self.fgColor = self.biome.treeColor;
    
    def countRiverNeighbours(self, countLakes = False, adjacentRequireed = False):
        
        count = 0;
        adjacent = False;
        
        for x in range(max(0, self._x - 1), min(self._x+1, self._map.width - 1) + 1):
            for y in range(max(0, self._y - 1), min(self._y+1, self._map.height - 1) + 1):
                if x == self._x and y == self._y:
                    continue
                
                if self._map.coords[x][y].isRiver:
                    if x == self._x or y == self._y:
                        adjacent = True
                    count += 1
                if countLakes and self._map.coords[x][y].isLake:
                    if x == self._x or y == self._y:
                        adjacent = True
                    count += 1
        
        # if the adjacentRequireed flag is set, and no adjacent river tiles were found, return 0
        if adjacentRequireed and not adjacent:
            count = 0
        
        return count
    
    def countLakeNeighbours(self):
        count = 0;
        for x in range(max(0, self._x - 1), min(self._x+1, self._map.width - 1) + 1):
            for y in range(max(0, self._y - 1), min(self._y+1, self._map.height - 1) + 1):
                if x == self._x and y == self._y:
                    continue
                if self._map.coords[x][y].isLake:
                    count += 1
        return count
    
    
    