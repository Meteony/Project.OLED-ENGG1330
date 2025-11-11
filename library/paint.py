"""
The game goes through 10 ticks per second
display dimensions: x: 68 = [0,67] = 1 + (33 + 1 + 33); y: 17 = [0,16]

Complete curses rewrite
Changed the directories of several file IO's
Attempts to fix the flickering once and for all
"""
import time
import curses
import random
import os
import getpass
import ast

if __name__=='__main__':
    try:
        os.chdir(os.getcwd().strip('//library'))
    except:
        pass


#region file directories initialization
current_dir = os.getcwd()
if not os.path.isdir('Saved Demos'):
    os.makedirs('Saved Demos')
demo_dir = current_dir+"//Saved Demos//"
tutorial_dir = current_dir+"//Tutorial Files//"

#endregion



#region main game

def flash_safe(stdscr, ms=60):
    """
    Try a real visual bell if the terminal supports it; otherwise:
    - beep(), and
    - briefly show a full-screen reverse-video overlay.
    """
    # If the terminal advertises a visual bell capability ("vb"), use it.
    # setupterm() is already run by curses.wrapper/initscr.
    if curses.tigetstr('vb'):
        curses.flash()
        return

    # Fallbacks: a tiny beep + quick reverse-video overlay.
    curses.beep()
    h, w = stdscr.getmaxyx()
    overlay = curses.newwin(h, w, 0, 0)
    try:
        overlay.bkgd(' ', curses.A_REVERSE)
        overlay.erase()
        overlay.refresh()
        curses.napms(ms)            # ~60 ms flash
    finally:
        # Remove overlay and force a repaint of underlying content
        del overlay
        stdscr.touchwin()
        stdscr.refresh()

def wait_for_key(win, ignore=(curses.KEY_RESIZE,)):
    win.nodelay(False)          # block until a key arrives
    curses.flushinp()           # drop queued events (incl. old KEY_RESIZE)
    try:
        while True:
            ch = win.getch()    # blocks; no exceptions
            if ch not in ignore:
                return ch
    finally:
        win.nodelay(True)                 
def paint(win):
    paint.player_id=getpass.getuser()
    paint.mode = 'Paint'
    tile_texture_mapping = {
            "1": "██",  #ON
            "0": "░░",  #OFF
            "00": "XX",  #CORR
            '11': "!!"
        }
    if False:pass
    else: #<------------------------------------------Normal/Rec-enabled gameplay
        curses.curs_set(0)
        win.nodelay(True)  # set once, not every loop
        win.keypad(True)
        selector = [0, 0]
        tick = 0
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        selector = [8, 8]
        map_size = (15, 15)  # create the map
       
        try:
            map_data = map_read()
        except FileNotFoundError:
        # initialize_game_map
            map_data = []
            map_data_temp = []
            for _ in range(map_size[0]):
                map_data_temp += ["0"]
            for _ in range(map_size[1]):
                map_data.append(map_data_temp[:])

        
    
    ###Gamemode

        # main loop
        tick = 0

        ##############################DISPLAY DEPENDENCIES
        

        powr_tuple = (122, 225)
        crpt_tuple = (450, 900)
        score = 0
        message=''
        message = syslog_appended(' ',message)

        message = syslog_appended('    [B][N]: Convert a Tile',message)
        message = syslog_appended('      [K]: Save your art',message)
        message = syslog_appended('      [ESC/BACK]:  Erase',message)
        message = syslog_appended('        [ENTER]: Boom!',message)
        message = syslog_appended(' ',message)

        message = syslog_appended(r'      Have fun! \(^o^)/',message)


        #message = f"{' '*33+'[B][N] Convert a Tile]':^33}"+' '*33+f"{'[K] Saves the map':^33}"+' '*33+f"""{'Have fun        ':^33}"""+' '*30
        # < -------------------------------------------------------------------------Start of the loop
        while True:
            tick += 1

            #region Perfect keyboard input registration
            try: key_queued
            except NameError: key_queued=list()

            try: # Drains duplicate input; queues all unique keystrokes
                key_drain = win.getkey()
                while True:
                    if not key_queued:
                        key_queued.append(key_drain) 
                    elif key_queued[-1]!=key_drain:
                        key_queued.append(key_drain)
                    key_drain = win.getkey()
            except curses.error: pass
            try: # Handle the first key in the queue
                key=key_queued.pop(0).lower()
                key_response(key, selector, map_data)
            except IndexError:key="noinput"
            
            MAX_QUEUE = 128 # Safety
            if len(key_queued) > MAX_QUEUE:
                del key_queued[:-MAX_QUEUE]
            #endregion
                        

            #Power Indicator & Progress tracking & Gradual corruption
            powr_tuple = (sum (x == '1' for row in map_data[:] for x in row ),225)
            #endregion

            #region --------------------------------Display Section------------------------------------
            if tick%20==0:  # screen erases every 2s
                #for y in range(17):
                    #win.addstr(y,0,' '*68)
                win.erase()  # clear FIRST
            
            
            
            powr_indicator_str = "-" * 30; crpt_indicator_str = "-" * 30 #Indicators base

            map_data_visual = []
            for row in range(len(map_data)):
                map_data_visual.append("".join(tile_texture_mapping[item] for item in map_data[row]))
            ui_elements = [
                f' │ │ {"POWER DRAIN:":<30} │ ',
                f" │ │ {powr_indicator_str:<30} │ ",
                f' │ │ {r"""INTEGRITY INDEX:""":<30} │ ',
                f' │ │ {crpt_indicator_str:<30} │ ',
                f' │ │ {"ENERGY LOSS:":<30} │ ',
                f" │ │ {score:<30} │ ",
                f' │ ├⎯{" SYSTEM LOG ":⎯^30}⎯┤ ',
                f" │ │ {message[0:30]:^30} │ ",
                f" │ │ {message[30:60]:^30} │ ",
                f" │ │ {message[60:90]:^30} │ ",
                f" │ │ {message[90:120]:^30} │ ",
                f" │ │ {message[120:150]:^30} │ ",
                f" │ │ {message[150:180]:^30} │ ",
                f" │ │ {message[180:210]:^30} │ ",
                f" │ │ {message[210:240]:^30} │ ",
            ]

            ######################DISPLAY BELOW
            try:
                # win.addstr(0, 0, f'Tick: {tick}'+'\n')
                win.addstr(0, 1, f"{'Pos: '+str(selector)+' |'+' Key: '+str(key):<66}")
                name_element = getattr(paint,"player_id",'N/A')
                win.addstr(0, 68-len(name_element), name_element)
                win.addstr(1, 0, f" {' - - ⎯  ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ Project OLED - '+paint.mode.capitalize()+' ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯  ⎯ - - ':^67}")
                for y in range(15): #Draws the map
                    win.addstr(2 + y, 0, " │ ")
                    current_line_rendered = 3
                    for x in range(15): #Map split out by lines
                        cell = map_data[y][x]
                        tile = tile_texture_mapping[cell]
                        win.addstr(2 + y, current_line_rendered, tile)
                        current_line_rendered += len(tile)
                    ui_elements_split = ui_elements[y][2:]
                    win.addstr(2 + y, current_line_rendered, ui_elements_split)
                
                
                
            #region Colored Elements & Flashes
                #Colored Cursor!
                cell = map_data[selector[1]][selector[0]]; tile=tile_texture_mapping[cell]
                win.addstr(2 + selector[1], 3+len(tile)*selector[0], tile, curses.color_pair(1))
                
                #Power Drain (Grid) indicator
                if powr_tuple[0] / powr_tuple[1] < 0.20:                      
                    win.addstr(3, 36, '^'*(int(30 * (powr_tuple[0] / powr_tuple[1]))),curses.color_pair(1))
                elif powr_tuple[0] / powr_tuple[1] < 0.40:
                    win.addstr(3, 36, '^'*(int(30 * (powr_tuple[0] / powr_tuple[1]))),curses.color_pair(2)) 
                elif powr_tuple[0] / powr_tuple[1] < 0.034: 
                    win.addstr(3, 36, '-'*30,curses.color_pair(2))            
                else:
                    win.addstr(3, 36, '^'*(int(30 * (powr_tuple[0] / powr_tuple[1]))),curses.color_pair(3))
                                            
                #Corruption Countdown indicator
                if crpt_tuple[0] / crpt_tuple[1] < 0.033:                   
                    win.addstr(5, 36, '-'*30,curses.color_pair(3))          
                elif crpt_tuple[0] / crpt_tuple[1] < 0.15: 
                    win.addstr(5, 36, '^'*(int(30 * (crpt_tuple[0] / crpt_tuple[1]))),curses.color_pair(3))
                elif crpt_tuple[0] / crpt_tuple[1] < 0.45:
                    win.addstr(5, 36, '^'*(int(30 * (crpt_tuple[0] / crpt_tuple[1]))),curses.color_pair(2)) 
                else:
                    win.addstr(5, 36, '^'*(int(30 * (crpt_tuple[0] / crpt_tuple[1]))),curses.color_pair(1))
                    
                #Energy Loss Indicator
                if score in range(0,-501,-1):                                        
                    win.addstr(7, 36, str(score),curses.color_pair(1)) #Green
                elif score in range(-501,-1001,-1):
                    win.addstr(7, 36, str(score),curses.color_pair(2)) #Yellow
                else:
                    win.addstr(7, 36, str(score),curses.color_pair(3)) #Red
                #if tick%10<5 and score<-0: #flashes
                            #win.addstr(7, 36, ' '*len(str(score)),curses.color_pair(1))
            #endregion




            except:
                pass
            #endregion
            

            if key=='k': #<--------------------End-of-game detection
                #print(map_data[:])
                map_save(map_data[:])
                return
            #endregion
            #region ------------------------------ Pause & Override Button-------------------------------
            elif key=='m':        #Pause functionality
                win.addstr(7, 0, '█'*69, curses.color_pair(2))
                win.addstr(8, 0, f'{" PAUSED  - PRESS ANY KEY TO CONTINUE ":█^69}', curses.color_pair(2))
                win.addstr(9, 0, '█'*69, curses.color_pair(2))
                win.noutrefresh(); curses.doupdate()
                time.sleep(0.25)
                wait_for_key(win)
            elif key in ('\x1b','key_backspace', '\b', '\x7f'):
                score=0
                map_data = []
                map_data_temp = []
                for _ in range(map_size[0]):
                    map_data_temp += ["0"]
                for _ in range(map_size[1]):
                    map_data.append(map_data_temp[:])
            elif key in ('\n', '\r', 'key_enter'):
                blow(*locate_random_white_tile(map_data),map_data=map_data)
                score-=1
            elif key == 'n':      #Override Patch
                override(selector[1],selector[0],map_data)
            #elif key == 'r':
                #game.enablerecording = not getattr(game,'enablerecording',False)
                #tick = 0
            #if getattr(game,'enabblerecording',False):
                #win.addstr(0,0,'REC           ')

            


            win.noutrefresh()
            curses.doupdate()  # <- show changes
            time.sleep(0.1)


def flip(y, x, map_data): # Override. Modifies map data in-place
    tiles = ('1','0','00','11')
    map_data[y][x] = tiles[(tiles.index(map_data[y][x])+1)%4]

def override(y, x, map_data): # Override. Modifies map data in-place
    tiles = ('1','0','00','11')
    map_data[y][x] = tiles[(tiles.index(map_data[y][x])-1)%4]

def blow(y, x, map_data): # Corruption tile generation. Modifies map data in-place
    map_size = (15, 15)
    blow_list = []
    blow_sequence = ((-1, 0), (1, 0), (0, 0), (0, -1), (0, 1))
    for delta_y, delta_x in blow_sequence:
        if (delta_y + int(y) in range(map_size[0])) and (delta_x + int(x) in range(map_size[1])):
            blow_list.append([y + delta_y, x + delta_x])
    for b, a in blow_list:
        map_data[b][a] = "00"



def syslog_appended(new_content,syslog):       #Usage: message = s_a(new_message,message)     
    syslog+=str(new_content)
    syslog+=' '*(30-(len(syslog)%30))   
    while len(syslog)>240:
        syslog=str(syslog)[30:] 
    return syslog

def locate_random_white_tile(map_data):
    try: 
        ones_coor = [(y,x) for y,row in enumerate(map_data) for x,item in enumerate(row) if item=='1']
        return random.choice(ones_coor)
    except:
        return (random.randint(1,15),random.randint(1,15))

def key_response(key, selector, map_data_list):
    if key == "w":
        selector[1] -= 1
    if key == "s":
        selector[1] += 1
    if key == "d":
        selector[0] += 1
    if key == "a":
        selector[0] -= 1
    
    selector[0] %= 15  #<--Selector teleportation at boundaries
    selector[1] %= 15 
    
    if key == "b":  # flip
        flip(selector[1], selector[0], map_data_list)
#endregion







def map_save(list):        #<----- Saves/Initializes the config file (tied to game() attributes)
    with open("paint.oledmap","w",encoding="utf-8") as map: 
        map.write(str(list))
def map_read():        #<----- Reads the config file & syncs the ER+SC settings (tied to game() attributes)
    with open("paint.oledmap","r",encoding="utf-8") as map:
        map = ast.literal_eval(''.join(map.readlines()))
    return map











#############################################################################################
############################### Main Game Function ##########################################
if __name__ == '__main__':
    curses.wrapper(paint)


