import libtcodpy as tcod
import Map.coord as coord
import Map.biome as biome
import Generator
import datetime
import math
import sys

class Map:
    
    # Display Modes
    OVERLAY_TEMP = 1
    OVERLAY_RAIN = 2
    OVERLAY_BIOME = 3
    OVERLAY_SALT = 4
    
    CHAR_TREE = 't'
    CHAR_TREE_SMALL = '|'
    CHAR_TREE_BIG = 'T'
    CHAR_TREE_DESERT = '+'
    CHAR_TREE_PALM = 'I'
    
    BIOME_DESERT = 0
    BIOME_SAVANNA = 1
    BIOME_TROPICAL = 2
    BIOME_RAIN_FOREST = 3
    BIOME_PLAINS = 4
    BIOME_WOODLAND = 5
    BIOME_FOREST = 6
    BIOME_BADLANDS = 7
    BIOME_BOREAL = 8
    BIOME_TUNDRA = 9
    BIOME_ARCTIC = 10
    BIOME_OCEAN = 11
    BIOME_FROZEN_OCEAN = 12
    BIOME_MOUNTAIN = 13
    
    MAX_ALTITUDE = 320
    TREE_LINE = 192
    
    #zoom-factor
    zoomFactor = 4
    
    #start at 1-to-1 zoom level
    _zoomLevel = 0
    
    # Offset of console viewport, relative to map coords
    _offsetX = 0
    _offsetY = 0
    
    #start with the stats panel shown
    _displayStats = True
    
    #start with no Display Overlays on
    _displayOverlay = None
    
    coords = []
    springs = []
    
    def __init__(self):
        pass
    
    def initDisplay(self, displayWidth, displayHeight):
        self._displayWidth = displayWidth;
        self._displayHeight = displayHeight;
        
        #libtcod consoles to draw to
        self._displayCon = tcod.console_new(displayWidth, displayHeight)
        self._overlay = tcod.console_new(displayWidth, displayHeight)
        
        #position of the "crosshair" within the console
        self._hudX = self._displayWidth/2
        self._hudY = self._displayHeight/2
        
        #the map coord where the "Crosshair" is currently located
        self._selectedX = self._offsetX + self._hudX
        self._selectedY = self._offsetY + self._hudY
        
        self.showCrosshair = True;        
    
    def generate(self, mode, width, height):
        
        if (mode == Generator.Generators.DIAMOND_SQUARE):
            print('Got dimensions', width, height)
            i = 1;
            while (2**i + 1 < width):
                i = i + 1
            width = 2**i + 1
            i = 1;
            while (2**i + 1 < height):
                i = i + 1
            height =  2**i + 1
            
            print('Using dimensions', width, height)
        
        self.width = width
        self.height = height
        self._initCoordsArray()
        
        gen = Generator.gen.Generator(mode)
        gen.generate(self)
    
    
    
    #%%%%%%%%%%%%%%%%%%%%#
    #%% Get map params %%#
    
    def heightmap(self, x, y, zoom=0):
        return self.coords[x][y].altitude
    
    def tempmap(self, x, y, zoom=0):
        return self.coords[x][y].temp
    
    def saltmap(self, x, y, zoom=0):
        return self.coords[x][y].salinity
    
    def getRain(self,x,y):
        return self.coords[x][y].rainfall
    
    def getDepth(self,x,y):
        return self.coords[x][y].depth
    
    def getBiome(self,x,y):
        return self.coords[x][y].biome.name
    
    #TODO: remove these and pre-calculate
    def getMinHeight(self):
        return tcod.heightmap_get_minmax(self._heightMap[0])[0]

    def getMaxHeight(self):
        return tcod.heightmap_get_minmax(self._heightMap[0])[1]
    
    def getMinTemp(self):
        return tcod.heightmap_get_minmax(self._tempMap[0])[0]

    def getMaxTemp(self):
        return tcod.heightmap_get_minmax(self._tempMap[0])[1]
    
    def distanceToOcean(self, x, y):    
        return max(0, self.heightmap(x,y))
    
    
    #%%%%%%%%%%%%%%%%%%%%#
    #%% Set map params %%#
    
    def setHeight(self, x, y, val, hm=False):
        self.coords[x][y].setAltitude(val)
    
    def setTemp(self, x, y, val, tm=False):
        self.coords[x][y].setTemp(val)
    
    def setSalt(self, x, y, val, sm=False):
        self.coords[x][y].setSalinity(val)
    
    def setRain(self, x, y, val):
        self.coords[x][y].setRain(val)
    
    def addSpring(self, x, y):
        if self.heightmap(x,y) > 0 and not self.coords[x][y].hasSpring:
            self.coords[x][y].addSpring();
            self.springs.append( (x, y) );
    
    def addRiver(self, x, y, sourceX, sourceY, depth):
        self.coords[x][y].addRiver(x, y, sourceX, sourceY, depth)
    
    def addLake(self, x, y):
        self.coords[x][y].addLake();
    
    # Get the list of spring coordinates
    def getSprings(self):
        return self.springs;
    
    
    def render(self, console=False, export=False):
        
        if not self._displayWidth or not self._displayHeight:
            print ('ERROR: Display dimensions not set, can not render Map.')
            sys.exit()
        if (self.width < self._displayWidth or self.height < self._displayHeight):
            print ('ERROR: Map size smaller than display size.')
            sys.exit()
        
        
        if console == False:
            console = self._displayCon
        
        if export:
            _offsetX = 0
            _offsetY = 0
            zoom = 0
        else:
            _offsetX = self._offsetX
            _offsetY = self._offsetY
            zoom = self._zoomLevel
        
        
        for cy in range(0, tcod.console_get_height(console) ):
            for cx in range(0, tcod.console_get_width(console) ):
                
                mx = cx + _offsetX
                my = cy + _offsetY
                
                c = self.coords[mx][my]
                
                tcod.console_put_char_ex(
                    console, cx, cy, 
                    c.char, 
                    c.fg(), c.bg())
                
                
                if (self._displayOverlay != None):
                    #TODO: generate overlays once, and move this stuff to the display layer.
                    if (self._displayOverlay == self.OVERLAY_TEMP):
                        
                        bgOverlay = c.tempColor
                    
                    elif (self._displayOverlay == self.OVERLAY_SALT):
                        
                        bgOverlay = c.saltColor
                    
                    elif (self._displayOverlay == self.OVERLAY_RAIN):
                        
                        bgOverlay = c.rainColor
                    
                    elif (self._displayOverlay == self.OVERLAY_BIOME):
                        
                        bgOverlay = c.biome.overlayColor
                    
                    
                    tcod.console_set_back(console, cx, cy, bgOverlay, tcod.BKGND_ALPHA(0.8))
                
                
        if not export:
            
            if ( self._zoomLevel == 0):
                height = self.height
                width = self.width
            elif (self._zoomLevel == 1):
                height = self.height/self.zoomFactor # / self.zoomLevel, right??
                width = self.width/self.zoomFactor
            
            if (self._selectedY <= self._displayHeight/2):
                self._hudY = self._selectedY
            elif (self._selectedY >= height - self._displayHeight/2):
                self._hudY = \
                    self._displayHeight/2 + (self._selectedY - (height - self._displayHeight/2))
            
            if ( self.showCrosshair ):
                if (self._selectedX <= self._displayWidth/2):
                    self._hudX = self._selectedX
                elif (self._selectedX >= width - self._displayWidth/2):
                    self._hudX = self._displayWidth - (width - self._selectedX)
                
                tcod.console_put_char(console, self._hudX, self._hudY, 'X', tcod.BKGND_NONE)
                tcod.console_set_fore(console, self._hudX, self._hudY, tcod.Color(255, 0, 127))
            
            
            if (self._displayStats):
                self._printStats(console)
        
        return console
    
    def setMode(self, mode):
        print('Setting Display Mode: ' + str(mode))
        
        if (mode == self._displayOverlay):
            self._displayOverlay = None
        else: 
            self._displayOverlay = mode
    
    def export(self):
        
        print("Exporting world map with dimensions [" + 
                str(self.width) + ',' + str(self.height) + ']');
        con = tcod.console_new(self.width, self.height);
        
        con = self.render(con, True)
        
        bmp = tcod.image_from_console(con)
        tcod.console_delete(con)
        
        date = datetime.datetime.now()
        timestamp = date.strftime("%Y%m%d-%H%M%S")
        
        tcod.image_save(bmp, 'export/WorldMap'+ timestamp + '.png')
        print "Done."
    
    
    def moveUp(self, step=1):
        
        if (int(self._zoomLevel) == 0):
            height = self.height
        elif (int(self._zoomLevel) == 1):
            height = self.height / self.zoomFactor
        
        if ((self._offsetY > 0) and 
            (self._selectedY <= height - self._displayHeight/2)):
            self._offsetY -= 1
        
        if (self._selectedY > 0):
            self._selectedY -= 1
    
    def moveDown(self, step=1):
        if (self._zoomLevel == 0):
            height = self.height
        elif (self._zoomLevel == 1):
            height = self.height / self.zoomFactor
        
        if ((self._offsetY < height - self._displayHeight) and 
            (self._selectedY >= self._displayHeight/2)):
            self._offsetY += 1
        
        if (self._selectedY < height-1):
            self._selectedY += 1
    
    def moveRight(self, step=1):
        
        if (self._zoomLevel == 0):
            width = self.width
        elif (self._zoomLevel == 1):
            width = self.width / self.zoomFactor
        
        if ((self._offsetX < width - self._displayWidth) and 
            (self._selectedX >= self._displayWidth/2)):
            self._offsetX += 1
        
        if (self._selectedX < width-1):
            self._selectedX += 1
    
    def moveLeft(self, step=1):
        
        if (self._zoomLevel == 0):
            width = self.width
        elif (self._zoomLevel == 1):
            width = self.width / self.zoomFactor
        
        if ((self._offsetX > 0) and 
            (self._selectedX <= width - self._displayWidth/2)):
            self._offsetX -= 1
        
        if (self._selectedX > 0):
            self._selectedX -= 1
    
    #TODO move stats display out of library, and provide a render function
    def toggleStats(self):
        print("toggling stats:", self._displayStats)
        self._displayStats = not self._displayStats
    
    def zoom(self):
        print("Zooming")
        self._zoomLevel = not self._zoomLevel
    
    def _initCoordsArray(self):
        self.coords = [ [coord.Coord(x,y, self) for y in range(self.height)] for x in range(self.width) ]
    
    #TODO allow configuration of biomes
    def _initBiomes(self):
        self.biomes = {
            self.BIOME_DESERT: biome.biome('Desert', {
                'overlayColor': tcod.Color(237,201,175),
                'treeColor': tcod.Color(120,134,107),
                'treeChar': self.CHAR_TREE_DESERT,
                'treeName': 'cactus',
                'treeDensity': 2 
            }),
            self.BIOME_SAVANNA: biome.biome('Savana', {
                'overlayColor': tcod.Color(225,169,95),
                'treeColor': tcod.Color(128,128,0),
                'treeChar': self.CHAR_TREE_SMALL,
                'treeName': 'Boabab',
                'treeDensity': 5
            }),
            self.BIOME_TROPICAL: biome.biome('Tropical', {
                'overlayColor': tcod.Color(0,183,235),
                'treeColor': tcod.Color(0,158,96),
                'treeChar': self.CHAR_TREE_PALM,
                'treeName': 'Palm',
                'treeDensity': 20
            }),
            self.BIOME_RAIN_FOREST: biome.biome('Rain Forest', {
                'overlayColor': tcod.Color(0,66,37),
                'treeColor': tcod.Color(16,128,16),
                'treeChar': self.CHAR_TREE_BIG,
                'treeName': 'Ipe',
                'treeDensity': 95
            }),
            self.BIOME_PLAINS: biome.biome('Plains', {
                'overlayColor': tcod.Color(245,222,179),
                'treeColor': tcod.Color(64,128,64),
                'treeChar': self.CHAR_TREE_SMALL,
                'treeName': 'Pine',
                'treeDensity': 5
            }),
            self.BIOME_WOODLAND: biome.biome('Woodland', {
                'overlayColor': tcod.Color(86,130,3),
                'treeColor': tcod.Color(1,121,111),
                'treeChar': self.CHAR_TREE,
                'treeName': 'Spruce',
                'treeDensity': 30
            }),
            self.BIOME_FOREST: biome.biome('Forest', {
                'overlayColor': tcod.Color(34,139,34),
                'treeColor': tcod.Color(32,196,32),
                'treeChar': self.CHAR_TREE_BIG,
                'treeName': 'Oak',
                'treeDensity': 80
            }),
            self.BIOME_BADLANDS: biome.biome('Badlands', {
                'overlayColor': tcod.Color(124,28,5),
                'treeColor': tcod.Color(0,0,0),
                'treeChar': self.CHAR_TREE_DESERT,
                'treeName': 'Juniper',
                'treeDensity': 3
            }),
            self.BIOME_BOREAL: biome.biome('Boreal', {
                'overlayColor': tcod.Color(154,205,50),
                'treeColor': tcod.Color(96,205,50),
                'treeChar': self.CHAR_TREE,
                'treeName': 'Spruce',
                'treeDensity': 70
            }),
            self.BIOME_TUNDRA: biome.biome('Tundra', {
                'overlayColor': tcod.Color(93,137,186),
                'treeColor': tcod.Color(192,192,192),
                'treeChar': self.CHAR_TREE_SMALL,
                'treeName': 'Arctic Willow',
                'treeDensity': 1
            }),
            self.BIOME_ARCTIC: biome.biome('Arctic', {
                'overlayColor': tcod.Color(192,192,192),
                'treeDensity': 0
            }),
            self.BIOME_OCEAN: biome.biome('Ocean', {
                'overlayColor': tcod.Color(0,105,148),
                'treeDensity': 0
            }),
            self.BIOME_FROZEN_OCEAN: biome.biome('Frozen Ocean', {
                'overlayColor': tcod.Color(192,255,255),
                'treeDensity': 0
            }),
            self.BIOME_MOUNTAIN: biome.biome('Mountain', {
                'overlayColor': tcod.Color(64,64,64),
                'treeDensity': 0
            })
        }
    
    def setBiomes(self):
        
        self._initBiomes()
        
        print "Calculating Biomes..."
        
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.coords[x][y].calculateBiome()
        
        
    
    def setColors(self):
        
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.coords[x][y].altitude = self.heightmap(x,y)
                self.coords[x][y].setColors()
    
    # Override the default character used for different types of trees
    def mapTreeChar(self, char, val):
        
        if char == self.CHAR_TREE:
            self.CHAR_TREE = val
        if char == self.CHAR_TREE_BIG:
            self.CHAR_TREE_BIG = val
        if char == self.CHAR_TREE_SMALL:
            self.CHAR_TREE_SMALL = val
        if char == self.CHAR_TREE_DESERT:
            self.CHAR_TREE_DESERT = val
        if char == self.CHAR_TREE_PALM:
            self.CHAR_TREE_PALM = val
        
        
    
    def _printStats(self, console):
        
        c = self.coords[self._selectedX][self._selectedY]
        
        messages = [
            (1, str(tcod.sys_get_fps()) + " FPS"),
            (2, "Coord: (" + str(self._selectedX)+","+str(self._selectedY)+")"),
            (3, "X-Offset: " + str(self._offsetX)),
            (4, "Y-Offset: " + str(self._offsetY)),
            (5, "Altitude: " + str(c.altitude)),
            (6, "Temp    : " + str(c.temp)),
            (7, "Rain    : " + str(c.rainfall)),
            (8, "Salinity: " + str(c.salinity)),
            (9, "Spring  : " + str(c.hasSpring)),
            (10, "Water   : " + str(c.depth)),
            (11, "Source  : " + str(c.source)),
            (12, "Biome   : " + str(c.biome.name))]
            
        tcod.console_set_foreground_color(console, tcod.Color(255,0,127));
        tcod.console_set_background_color(console, tcod.Color(0,0,0));
        for y, msg in messages:
            tcod.console_print_right(console, self._displayWidth-1, 
                                     y, tcod.BKGND_NONE, msg)
        tcod.console_set_foreground_color(console, tcod.Color(255,255,255));
        
        
        
###/////////////////////////////////////////////////////////////////////////////////////////////////
### EOF    