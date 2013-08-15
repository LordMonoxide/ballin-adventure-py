import libtcodpy as tcod

class biome:
    overlayColor = tcod.Color(128,128,128)
    treeColor = tcod.green
    treeChar = '}'
    treeName = 'tree'
    treeDensity = 0
    
    def __init__(self, name, options):
        
        self.name = name
        
        if 'overlayColor' in options:
            self.overlayColor = options['overlayColor']
        if 'treeColor' in options:
            self.treeColor = options['treeColor']
        if 'treeChar' in options:
            self.treeChar = options['treeChar']
        if 'treeName' in options:
            self.treeName = options['treeName']
        if 'treeDensity' in options:
            self.treeDensity = options['treeDensity']
