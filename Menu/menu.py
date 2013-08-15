import libtcodpy as tcod
import menu_options
import window
import sys

class Menu:
    
    MENU_TOP = 10
    MENU_LEFT = 10
    MENU_WIDTH = 20
    MENU_HEIGHT = 8
    
    _selection = 0
    
    options = menu_options.options
    
    def __init__(self):
        _winMain = window.Window(self.MENU_TOP, self.MENU_LEFT, 
                                 self.MENU_WIDTH, self.MENU_HEIGHT);
    
    
    def doMenu(self):
        
        tcod.console_set_foreground_color(0, tcod.white);
        
        selectedLine = 1
        
        while True:
            
            tcod.console_clear(0)
            
            index = 1
            
            for mode, name in self.options:
                tcod.console_print_left(
                        0, self.MENU_LEFT+2, self.MENU_TOP+index, 
                        tcod.BKGND_NONE, name)
                if (selectedLine == index):
                    self._selection = mode
                    tcod.console_put_char(0, self.MENU_LEFT+1, 
                                          self.MENU_TOP+index, '>')
                index += 1
            
            tcod.console_flush();
            
            # Get Input
            key = tcod.console_wait_for_keypress(True);
            
            if (key.vk == tcod.KEY_DOWN):
                selectedLine += 1
                if (selectedLine > len(self.options)):
                    selectedLine = 1
                
            elif (key.vk == tcod.KEY_UP):
                selectedLine -= 1
                if (selectedLine <= 0):
                    selectedLine = len(self.options)
            
            if (key.vk == tcod.KEY_ENTER):
                return self._selection
        