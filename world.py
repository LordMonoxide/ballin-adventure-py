#!/usr/bin/python
## -*- coding: Latin-1 -*-

import libtcodpy as tcod
from Menu import menu
import map 
import sys
import logging
import time

WIDTH   = 80;
HEIGHT  = 50;

MAP_WIDTH = 255;
MAP_HEIGHT = 255;

FPS     = 24;

DISPLAY_MAP_WIDTH = 48;
DISPLAY_MAP_HEIGHT = 48;
DISPLAY_MAP_TOP = 1;
DISPLAY_MAP_LEFT = 1;

tcod.console_set_custom_font('fonts/dundalk15x15_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
tcod.console_init_root(WIDTH, HEIGHT, 'Title', False)

tcod.sys_set_fps(FPS)

_menu = menu.Menu();

mode = _menu.doMenu();

if (mode == menu.menu_options.MODE_QUIT):
    sys.exit()

elif (mode > 0):
    _map = map.Map();
    _map.generate(mode, MAP_WIDTH, MAP_HEIGHT)
    _map.initDisplay(DISPLAY_MAP_WIDTH, DISPLAY_MAP_HEIGHT);
    #_map.generateZoomViews()
else:
    sys.exit()

# Map tree characters
tcod.console_map_ascii_code_to_font(200, 0, 5)
_map.mapTreeChar(_map.CHAR_TREE, chr(200))
tcod.console_map_ascii_code_to_font(201, 1, 5)
_map.mapTreeChar(_map.CHAR_TREE_SMALL, chr(201))
tcod.console_map_ascii_code_to_font(202, 2, 5)
_map.mapTreeChar(_map.CHAR_TREE_BIG, chr(202))
tcod.console_map_ascii_code_to_font(203, 3, 5)
_map.mapTreeChar(_map.CHAR_TREE_DESERT, chr(203))
tcod.console_map_ascii_code_to_font(204, 4, 5)
_map.mapTreeChar(_map.CHAR_TREE_PALM, chr(204))


# Main loop
while True:
    
    mapCon = _map.render();
    tcod.console_blit(mapCon, 0,0, 
        DISPLAY_MAP_WIDTH, DISPLAY_MAP_HEIGHT, 0, DISPLAY_MAP_TOP, DISPLAY_MAP_LEFT);
    
    tcod.console_flush();
    
    key = tcod.console_wait_for_keypress(True)
    
    if (key.vk == tcod.KEY_NONE):
        continue
    
    if (key.vk == tcod.KEY_UP):
        _map.moveUp()
    if (key.vk == tcod.KEY_DOWN):
        _map.moveDown()
    if (key.vk == tcod.KEY_RIGHT):
        _map.moveRight()
    if (key.vk == tcod.KEY_LEFT):
        _map.moveLeft()
    
    #Toggle display overlays
    if (key.vk == tcod.KEY_F1):
        _map.setMode(1)
    if (key.vk == tcod.KEY_F2):
        _map.setMode(2)
    if (key.vk == tcod.KEY_F3):
        _map.setMode(3)
    
    if (key.vk == tcod.KEY_F12):
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    
    if (key.vk == tcod.KEY_TAB):
        _map.toggleStats()
    
    
    if (key.c == ord('p') or key.c == ord('P')):
        _map.export();
    
    #if (key.c == ord('z') or key.c == ord('Z')):
        #_map.zoom();
    
    
    if key.vk == tcod.KEY_ESCAPE :
        break
    
    #render
    
    
###/////////////////////////////////////////////////////////////////////////////////////////////////
### EOF    