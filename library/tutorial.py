
import curses,time,random,os
if __name__=='__main__':
    os.chdir(os.getcwd().strip('//library'))





#region jank
def demo_select(win): pass
def pref_save(): pass
def pref_read(): pass
def highscore_browser(win): pass
def url_read():
    return 0
"""
The game goes through 10 ticks per second
display dimensions: x: 68 = [0,67] = 1 + (33 + 1 + 33); y: 17 = [0,16]

The games connect to a google sheets webpage. 
The default links need to be removed/become customizable if the game is to be released. 
"""
import time
import curses
import random,ast,os
def game(): pass
game.enablerecording = False; game.skipcutscene = True; game.cloudconnectivity = False
current_dir = os.getcwd()

demo_dir = current_dir+"//Saved Demos//"
tutorial_dir = current_dir+"//Tutorial Files//"


#endregion



class playback_window:
    def __init__(self, x_offset=0, y_offset=0,play_tutorial_demo=None,disable_flash=False):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.disable_flash = disable_flash
        self.designated_demo_filename = play_tutorial_demo
        try:    
            if play_tutorial_demo==None:    
                self.replayfile = random.choice(list(file for file in os.listdir(demo_dir) if file.endswith(".oled")))
                directory = demo_dir
            else: 
                self.replayfile = str(play_tutorial_demo)
                directory = tutorial_dir
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
            self.tile_texture_mapping = {"1": "██","0": "░░","00": "XX",'11': "!!"}
            self.selector = [8, 8]
            self.map_size = (15, 15)
            self.map_data = [["0" for _ in range(self.map_size[1])] for _ in range(self.map_size[0])]
            self.last_tick_played_at = time.monotonic()
            with open(directory+self.replayfile,'r',encoding="utf-8") as demo:
                self.demo_data = ast.literal_eval(demo.readline())
                self.demo_mode=str(demo.readline())[:-1] #<---Cuts off the \n
                self.playertag=str(demo.readline())[:-1]
                self.demo_recorded_time=str(demo.readline())[:-1]
                self.demostats = ast.literal_eval(demo.readline())
                self.demoscore = self.demostats[0]
            self.tick=min(self.demo_data)-1;  #Skips to the first tick with data in demo, sets key to default
            
            self.tick = 0
            self.message = ''
            self.crpt_tuple = (450, 900)
            self.score = 0
            self.demo_fetched = True
        except (IndexError, FileNotFoundError):
            self.demo_fetched=False

    # If these don’t need self, mark them @staticmethod and call via the class.
    @staticmethod
    def flash_safe(stdscr, ms=60):
        if curses.tigetstr('vb'):
            curses.flash(); return
        curses.beep()
        h, w = stdscr.getmaxyx()
        overlay = curses.newwin(h, w, 0, 0)
        try:
            overlay.bkgd(' ', curses.A_REVERSE)
            overlay.erase(); overlay.refresh()
            curses.napms(ms)
        finally:
            del overlay
            stdscr.touchwin(); stdscr.refresh()

    # Instance methods must take self first




    def run_a_frame(self, win, key='noinput'):
        if self.demo_fetched:
            self.tick += 1
            try: #<------Matches the tick to see if there's stored data for this frame


                #Format:
                # [key,selector,(map_data),(powr_tuple),(crpt_tuple),score,message,lwst_powr_tuple_rc]
                fetched_stat = self.demo_data[self.tick]
                if fetched_stat[0]!=None:
                    key = fetched_stat[0]
                if fetched_stat[1]!=None:
                    self.selector = fetched_stat[1]
                if fetched_stat[2]!=None:
                    self.map_data = ast.literal_eval(fetched_stat[2])
                if fetched_stat[4]!=None:
                    self.crpt_tuple = fetched_stat[4]
                if fetched_stat[5]!=None:
                    self.last_tick_played_atcrpt_tuple = fetched_stat[5]


            except: 
                pass
            map_data_visual = []
            for row in range(len(self.map_data)):
                map_data_visual.append("".join(self.tile_texture_mapping[item] for item in self.map_data[row]))
            ######################DISPLAY BELOW
            for y in range(15): #Draws the map
                current_line_rendered = 0
                for x in range(15): #Map split out by lines
                    cell = self.map_data[y][x]
                    tile = self.tile_texture_mapping[cell]
                    try: win.addstr(0 + y+self.y_offset, current_line_rendered+self.x_offset, tile) 
                    except curses.error: pass
                    current_line_rendered += len(tile)
                cell = self.map_data[self.selector[1]][self.selector[0]]; tile=self.tile_texture_mapping[cell]
                win.addstr(0 + self.selector[1]+self.y_offset, 0+len(tile)*self.selector[0]+self.x_offset, tile, curses.color_pair(1))
            if key == 'n':      #Override Patch
                if not self.crpt_tuple[0] / self.crpt_tuple[1] <= 0.45 and not self.disable_flash: 
                    time.sleep(0.1);self.flash_safe(win);self.flash_safe(win);time.sleep(0.15)
            if not self.tick>=max(self.demo_data.keys()):
                if time.monotonic()%3.25<=0.75:
                    if self.replayfile == "default.oled":
                        replay_indicator_text = " [>] Demo Gameplay "
                    else:
                        max_filename_len = 25 #cuts off the filename at chr 25. 
                        if len(self.replayfile)>max_filename_len:
                            replayfilename_truncated = self.replayfile[:max_filename_len-3]+'...'
                        else: replayfilename_truncated = self.replayfile
                        replay_indicator_text = f''' [>]'{replayfilename_truncated}' '''
                    win.addstr(self.y_offset+7,self.x_offset+(30-len(replay_indicator_text))//2,replay_indicator_text)
                    self.last_tick_played_at = time.monotonic()
            else:
                for y in range(15): #flushes the screen
                    for x in range(30):
                        win.addstr(y+self.y_offset,x+self.x_offset,' ')
                replay_indicator_text = " End of Playback "
                win.addstr(self.y_offset+7,self.x_offset+(30-len(replay_indicator_text))//2,replay_indicator_text)
                if time.monotonic() - getattr(self,"last_tick_played_at",0) >= 4:
                    self.__init__(self.x_offset,self.y_offset,play_tutorial_demo=self.designated_demo_filename)
        else:
                replay_indicator_text = [" No available demos... "," yet! ","You can enable demo recording",'''from "settings"''']
                for y,text in enumerate(replay_indicator_text,start=-1):
                    win.addstr(self.y_offset+7+y,self.x_offset+(30-len(text))//2,text)



class main_menu():
    #region menu render functions
    @staticmethod
    def draw_left_bound(win,x_offset=0,y_offset=0):
        for i in range(0,17):    
            win.addstr(i+y_offset,x_offset,'│')
    @staticmethod
    def draw_logo(win,x_offset=1,y_offset=1): 
        logo=[
            r" _______/______________________     ",
            r" __  __ \░░  /___  ____/__  __ \"   ",
            r" _  / / /_  / __  __/  __  / /░/    ",
            r" / /░/ /_  /___▒▒/___  ░▒ /_/ /     ",
            r" \____/ /_____/_____/░░░_____/      "
        ]
        for i in range(5):
            win.addstr(i+y_offset,x_offset,logo[i])
        win.addstr(y_offset,x_offset+1,'Project',curses.A_UNDERLINE | curses.A_ITALIC)
        

    @staticmethod
    def draw_main_menu_options(win,selector_pos=1,x_offset=0): #it returns the max value of options possible
        options = [
            f'''{'Play Project OLED"':<30}''',
            f'''{'Demo Browser':<30}''',
            f'''{'View Scoreboard':<30}''',
            f'''{'Settings':<30}''',
            f'''{'Exit':<30}'''
        ]
        for num,text in enumerate(options,start=1):
            if not selector_pos == num:    
                win.addstr(7+2*(num-1),2+x_offset,text)
            else:
                if False:#num!=5:
                    win.addstr(7+2*(num-1),2+x_offset,text,curses.color_pair(2) | curses.A_REVERSE) 
                else:
                    win.addstr(7+2*(num-1),2+x_offset,text,curses.A_REVERSE)
        return len(options)
    
    @staticmethod
    def draw_play_menu_options(win,selector_pos=1,x_offset=0): #it returns the max value of options possible
        options = [
            f'''{'Fast Mode':<30}''',
            f'''{'Hardcore Mode':<30}''',
            f'''{'Classic Mode':<30}''',
            f'''{'Tutorial':<30}''',
            f'''{'Return':<30}'''
        ]
        for num,text in enumerate(options,start=1):
            if not selector_pos == num:    
                win.addstr(7+2*(num-1),2+x_offset,text)
            else:
                if False:#num!=5:
                    win.addstr(7+2*(num-1),2+x_offset,text,curses.color_pair(2) | curses.A_REVERSE) 
                else:
                    win.addstr(7+2*(num-1),2+x_offset,text,curses.A_REVERSE)
        return len(options)

    @staticmethod
    def draw_bonus_play_menu_options(win,selector_pos=1,x_offset=0): #it returns the max value of options possible
        options = [
            f'''{'Slow Mo"':<30}''',
            f'''{'Alpha':<30}''',
            f'''{'Return':<30}'''
        ]
        for num,text in enumerate(options,start=1):
            return_btn_offset = lambda a : 4 if a == 3 else 0    
            if not selector_pos == num:    
                    
                    win.addstr(7+2*(num-1)+return_btn_offset(num),2+x_offset,text)
            else:
                if False:#num!=5:
                    win.addstr(7+2*(num-1)+return_btn_offset(num),2+x_offset,text,curses.color_pair(2) | curses.A_REVERSE) 
                else:
                    win.addstr(7+2*(num-1)+return_btn_offset(num),2+x_offset,text,curses.A_REVERSE)
        for num in (3,4):
            win.addstr(7+2*(num-1),2+x_offset,' '*30)


        return len(options)

    @staticmethod
    def draw_settings_options(win,selector_pos=1,x_offset=0): #it returns the max value of options possible
        options = [
            f'''{'Enable Demo Recording':<30}''',
            f'''{'Skip Game-over Cutscene':<30}''',
            f'''{'Enable Cloud Connectivity':<30}''',
            f'''{'Bonus Gamemodes':<30}''',
            f'''{'Return':<30}'''
        ]
        indicators_status = {1:getattr(game,'enablerecording',False),
                            2:getattr(game,'skipcutscene',False),
                            3:getattr(game,'cloudconnectivity',False)
                            }
        for num,text in enumerate(options,start=1):
            if num in indicators_status.keys():
                is_indicator = True
                on_or_off=indicators_status[num]
            else: is_indicator = False

            if selector_pos != num:    #not highlighted
                win.addstr(7+2*(num-1),2+x_offset,text)
                if is_indicator:
                    win.addstr(7+2*(num-1),2+x_offset+1+len(text.strip()),
                            ('□','■')[on_or_off],
                            curses.color_pair((3,1)[on_or_off])
                            )
            else:   #highlighted
                if is_indicator:
                    win.addstr(7+2*(num-1),2+x_offset,
                            f"{text.strip()+' '+('□','■')[on_or_off]:<30}",
                            curses.color_pair((3,1)[on_or_off]) | curses.A_REVERSE
                            )

                elif False:#num==5: #"return" highlight
                    win.addstr(7+2*(num-1),2+x_offset,text,curses.color_pair(2) | curses.A_REVERSE)

                else: #normal tiles
                    win.addstr(7+2*(num-1),2+x_offset,text,curses.A_REVERSE)
        return len(options)


    @staticmethod
    def pop_notif(win,message='?',interval=2,color=3):
        win.addstr(7, 0, '█'*69, curses.color_pair(color))
        highscore_message = f'''[!] {message}'''
        win.addstr(8, 0, f'{" "+highscore_message+" ":█^69}', curses.color_pair(color))
        win.addstr(9, 0, '█'*69, curses.color_pair(color))
        win.noutrefresh();curses.doupdate()
        curses.napms(interval*1000)
        for i in range(3):
            win.addstr(7+i, 0, ' '*69)
    #endregion


    
    
    @staticmethod
    def handleselection(win_name,selector,win):
        if win_name == 'main':
            if selector==1: #play menu entered
                main_menu.currentwin = 'main-play'
                return 'change_menu'
            elif selector == 2: #Demo Browser
                selected_demo=demo_select(win=win) #demo_select()
                if selected_demo == 0: 
                    win.nodelay(True)
                    win.erase()
                    #curses.wrapper(main_menu.run(win=win,destination='main')) #none selected
                else:   
                    game.replayfile = selected_demo
                    game.replaymode = True
                    return 'exit_menu_only'
            elif selector == 3:
                highscore_browser(win=win)
                win.nodelay(True)
                win.erase()
                #curses.wrapper(main_menu.run(win=win,destination='main'))
            elif selector == 4:
                main_menu.currentwin = 'main-settings'
                return 'change_menu'
            elif selector == 5:
                return 'exit'



        elif win_name == 'main-play':
            if selector == 5:
                main_menu.currentwin = 'main'
                return 'change_menu'
            elif selector==1: game.mode = 'fast'; return 'exit_menu_only'
            elif selector == 2: game.mode = 'hardcore'; return 'exit_menu_only'
            elif selector == 3: game.mode = 'classic'; return 'exit_menu_only'
            elif selector == 4: main_menu.pop_notif(win,'SoonTM')

            
        elif win_name == 'main-settings':
            if selector == 1:
                game.enablerecording = not game.enablerecording
            elif selector == 2:
                game.skipcutscene = not game.skipcutscene
            elif selector == 3:
                game.cloudconnectivity = not game.cloudconnectivity
                if url_read()==1:
                    game.cloudconnectivity = False
                    main_menu.pop_notif(win,'''Unable to find "oled_connectivity.data"''')
            elif selector == 4:
                main_menu.currentwin = 'main-settings-bonusplay'
                return 'change_menu'
            elif selector == 5:
                main_menu.currentwin = 'main'
                return 'change_menu'
        elif win_name == 'main-settings-bonusplay':
            if selector == 1: game.mode = 'standard'; return 'exit_menu_only'
            elif selector == 2: game.mode = 'alpha'; return 'exit_menu_only'
            elif selector == 3:
                main_menu.currentwin = 'main-settings'
                return 'change_menu'




    



    @staticmethod
    def run(win,erase_sec=2,arrive_at_menu = 'main'):

        win.keypad(True)
        curses.curs_set(0)
        win.nodelay(True)  # set once, not every loop
        curses.start_color()
        #region color pairs
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        #endregion
        game_win = playback_window(x_offset=37+1,y_offset=2)
        selector_pos = 1
        main_menu.currentwin = arrive_at_menu
        main_menu.exit = False
        game.enablerecording = False; game.replaymode = False; game.skipcutscene = False; game.cloudconnectivity = False
        try: #config persistence implementation
            pref_read()
        except: 
            pref_save()
        if url_read()==1: # If no url files exist, flips the setting to "False"
            game.cloudconnectivity = False



        last_erase = time.monotonic()

        while True:
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
                key=key_queued.pop(0)
            except IndexError:key="noinput"
            
            MAX_QUEUE = 128 # Safety
            if len(key_queued) > MAX_QUEUE:
                del key_queued[:-MAX_QUEUE]
            #endregion
            try:
                if time.monotonic()-last_erase>=erase_sec:
                    win.erase()
                    last_erase = time.monotonic()
                game_win.run_a_frame(win)
                if key in ('s','KEY_DOWN'):
                    selector_pos = min(selector_pos+1,num_avai_options)
                if key in ('w','KEY_UP'):
                    selector_pos = max(1,selector_pos-1)
                if key in ('c','b',r'\n'): #selection
                    selection_result = main_menu.handleselection(main_menu.currentwin,selector_pos,win)
                    if selection_result == 'exit_menu_only':
                        break
                    if selection_result == 'exit':
                        main_menu.exit = True
                        break

                    if selection_result == 'change_menu':
                        selector_pos = 1


                main_menu.draw_left_bound(win,x_offset=1)
                
                win.addstr(0,55+1,'A11 Software')
                main_menu.draw_logo(win,x_offset=2,y_offset=1)
                
                if main_menu.currentwin == 'main':
                    num_avai_options = main_menu.draw_main_menu_options(win,selector_pos,x_offset=1) #draws main menu 
                elif main_menu.currentwin == 'main-play':
                    num_avai_options = main_menu.draw_play_menu_options(win,selector_pos,x_offset=1) #draws play menu 
                elif main_menu.currentwin == 'main-settings':
                    num_avai_options = main_menu.draw_settings_options(win,selector_pos,x_offset=1) #draws play menu 
                elif main_menu.currentwin == 'main-settings-bonusplay':
                    num_avai_options = main_menu.draw_bonus_play_menu_options(win,selector_pos,x_offset=1) #draws play menu 


                win.noutrefresh()
                curses.doupdate()  # <- show changes
            except curses.error: pass
            time.sleep(0.1)
        pref_save()

###############################
class game_nonblock:
    def __init__(self, x_offset=0, y_offset=0, designated_map=None):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.tile_texture_mapping = {"1": "██","0": "░░","00": "XX",'11': "!!"}
        self.selector = [8, 8]
        self.map_size = (15, 15)
        if designated_map == None:
            self.map_data = [["0" for _ in range(self.map_size[1])] for _ in range(self.map_size[0])]
            for _ in range(90):    
                self.flip(random.randint(1,14),random.randint(1,14))
        else: 
            if type(designated_map) == str:
                self.map_data=ast.literal_eval(designated_map)
            else: self.map_data = designated_map
        self.tick = 0
        self.message = ''
        self.crpt_tuple = (450, 900)
        self.score = 0
        self.x_offset = x_offset
        self.y_offset = y_offset

    # If these don’t need self, mark them @staticmethod and call via the class.
    @staticmethod
    def flash_safe(stdscr, ms=60):
        if curses.tigetstr('vb'):
            curses.flash(); return
        curses.beep()
        h, w = stdscr.getmaxyx()
        overlay = curses.newwin(h, w, 0, 0)
        try:
            overlay.bkgd(' ', curses.A_REVERSE)
            overlay.erase(); overlay.refresh()
            curses.napms(ms)
        finally:
            del overlay
            stdscr.touchwin(); stdscr.refresh()

    @staticmethod
    def wait_for_key(win, ignore=(curses.KEY_RESIZE,)):
        win.nodelay(False)
        curses.flushinp()
        try:
            while True:
                ch = win.getch()
                if ch not in ignore:
                    return ch
        finally:
            win.nodelay(True)

    # Instance methods must take self first
    def flip(self, y, x):
        seq = [(-1,0),(1,0),(0,0),(0,-1),(0,1)]
        for dy, dx in seq:
            yy, xx = y+dy, x+dx
            if 0 <= yy < 15 and 0 <= xx < 15:
                if self.map_data[yy][xx] in '01':
                    self.map_data[yy][xx] = "0" if self.map_data[yy][xx] == "1" else "1"

    def blow(self, y, x):
        seq = [(-1,0),(1,0),(0,0),(0,-1),(0,1)]
        for dy, dx in seq:
            yy, xx = y+dy, x+dx
            if 0 <= yy < 15 and 0 <= xx < 15:
                self.map_data[yy][xx] = "00"

    def override(self, y, x):
        if 0 <= y < 15 and 0 <= x < 15:
            self.map_data[y][x] = "11"

    def syslog_appended(self, new_content, syslog):
        syslog += str(new_content)
        syslog += ' ' * (30 - (len(syslog) % 30))
        while len(syslog) > 240:
            syslog = syslog[30:]
        return syslog

    @staticmethod
    def locate_random_white_tile(map_data):
        ones = [(y,x) for y,row in enumerate(map_data) for x,v in enumerate(row) if v == '1']
        return random.choice(ones) if ones else (random.randint(0,14), random.randint(0,14))

    def respond_to_key(self, key):
        if key == "w": self.selector[1] -= 1
        if key == "s": self.selector[1] += 1
        if key == "d": self.selector[0] += 1
        if key == "a": self.selector[0] -= 1
        self.selector[0] %= 15
        self.selector[1] %= 15
        if key == "b":
            self.flip(self.selector[1], self.selector[0])

    def run_a_frame(self, win, key):
        self.tick += 1
        self.respond_to_key(key)
        map_data_visual = []
        for row in range(len(self.map_data)):
            map_data_visual.append("".join(self.tile_texture_mapping[item] for item in self.map_data[row]))
        win.addstr(0+self.y_offset, 1+self.x_offset, f"{'Pos: '+str(self.selector)+' |'+' Key: '+str(key):<66}")
        text='[Interactive Page]'
        win.addstr(0+self.y_offset, 68+self.x_offset-len(text),text)
        for y in range(15): #Draws the map

            """
            win.addstr(2 + y+self.y_offset, 0+self.x_offset, " │ ")
            win.addstr(2 + y+self.y_offset, 66+self.x_offset, " │ ")
            win.addstr(2 + y+self.y_offset, 33+self.x_offset, " │ ")

"""            
            map_x_offsett = 36
            drawing_x_pos = map_x_offsett
            for x in range(15): #Map split out by lines
                cell = self.map_data[y][x]
                tile = self.tile_texture_mapping[cell]
                win.addstr(2 + y+self.y_offset, drawing_x_pos+self.x_offset, tile)
                drawing_x_pos += len(tile)
            cell = self.map_data[self.selector[1]][self.selector[0]]; tile=self.tile_texture_mapping[cell]
            win.addstr(2 + self.selector[1]+self.y_offset, map_x_offsett+len(tile)*self.selector[0]+self.x_offset, tile, curses.color_pair(1))

        if key == 'm':
            win.addstr(8+self.y_offset, 36+self.x_offset, '█'*30, curses.color_pair(2))
            win.addstr(9+self.y_offset, 36+self.x_offset, f'{" PAUSED - PRESS ANY KEY ":█^30}', curses.color_pair(2))
            win.addstr(10+self.y_offset, 36+self.x_offset, '█'*30, curses.color_pair(2))
            win.noutrefresh(); curses.doupdate()
            time.sleep(0.25)
            game_nonblock.wait_for_key(win)   # static call
                
        if key == 'n':
            if False:#self.crpt_tuple[0] / self.crpt_tuple[1] <= 0.45:
                self.message = self.syslog_appended("[!] Insufficient integrity. Can't override.", self.message)
            else:
                self.crpt_tuple = (126, 900)
                self.override(self.selector[1], self.selector[0])
                self.message = self.syslog_appended("[!] Override completed!", self.message)
                time.sleep(0.1); game_nonblock.flash_safe(win); game_nonblock.flash_safe(win); time.sleep(0.15)










class GameTutorial:
    def __init__(self, player_name=""):
        self.player_name = player_name
        self.current_step = 0
        self.tutorial_steps = [
            {
                "title": "WELCOME ABOARD",
                "content": [
                    "                         ",
                    '''Welcome to Project OLED"! ''',
                    "A 15x15 action/logic puzzler.",
                    "                         ",
                    "This tutorial shows:",
                    "• Controls & Tiles",
                    "• Flip & Override",
                    "• Integrity/Drain bars",
                    "• Energy Loss scoring",
                    "• Modes + replay",
                    "• Tips & strats"
                ],
                "wait_for_move": False,
                "wait_for_flip": False,
                "wait_for_move_and_flip": False
            },
            {
                "title": "BASIC CONTROLS",
                "content": [
                    "                         ",

                    "Move: [W][A][S][D]",
                    "                         ",
                    "Flip: [B]  (+ cross, 5 tiles)",
                    "      > toggles ■ <> □",
                    "                         ",
                    "Override: [N] > [!!] (perma)",
                    "                         ",
                    "End: [K]    Pause: [M]",
                    "                         ",
                    "Try them on the right.",
                    "Bars are off in this trial."
                    ],
            
            },
            {
                "title": "TYPES OF TILES (BOOM):",
                "content": [
                    "(see that? these're corruption)",
                    "Tile types:",
                    "                            ",
                    '"ON": ■',
                    '"OFF": □',
                    "                            ",
                    '"Corruption": [XX]',
                    "(Permanent OFF tile)",
                    "                            ",
                    '"Override": [!!]',
                    "(Another perma. OFF tile)"
                ],
            
            },
            {
                "title": "BASIC GAME RULES:",
                "content": [
                    "• Objective:",
                    "Convert the most tiles to",
                    '"OFF" (no ■), FAST.',
                    "                            ",
                    '• Flip affects a plus:',
                    'Center, up, down, left, right.',
                    "No diagonals.",
                    "                           ",
                    "• States are toggled: (■< >□)",
                    "Be smart with your moves,",
                    "avoid undoing your progress.",
                    "                            ",
                    "Continued on Next Page..."
                ],
                
            },
             {
                "title": "OVERRIDE [N] (TRIAL)",
                "content": [
                    " ",
                    "• Functionality:",
                    "Override cleans stragglers.",
                    "Target tile becomes [!!].",
                    " ",
                    "• Cost:",
                    "In full game it costs",
                    "Integrity (details next).",
                    " ",' ',
                    "Try [N] now (aim at ■)."
                ],
                
            },
             {
                "title": "WHAT CORRUPTION DOES",
                "content": [
                "• When:",
                "Integrity hits 0:",
                "1-3 random ■ explode and",
                "convert to [XX].",
                ' ',
                "• Why:",
                "Speeds up the game (don't",
                "need to deal with [XX])",
                ' ',
                "• Penalty: ",
                "-150 energy per occurance.",
                ' ',
                ],
                
            },
    
            {
                "title": "INFO PANE & BARS",
                "content": [
                    ' ',
                    "Info pane shows:",
                    ' ',
                    "• Power Drain (top bar)",
                    ' ',
                    "• Integrity Index (next bar)",
                    ' ',
                    "• Energy Loss (score)",
                    ' ',
                    "• Messages & tips"
                ],
                
            },
            {
                "title": "BARS & OVERRIDE",
                "content": [
                    " ",
                    "• Power Drain:",
                    "Drain starts ~50% and",
                    "drops as you clear ■.",
                    "Higher = faster score loss;",
                    " ",
                    "• Integrity Index:",
                    "Decays over time (faster",
                    "when Power Drain is high).",
                    " ", 
                    "Refills as you clear ■",
                    '(25% each reduction)',

                    "                            >>"
                ],
                
            },
            {
                "title": "BARS & OVERRIDE",
                "content": [
                    "• Integrity Index:",
                    "Needed for [N] (req. ≥45%).",
                    "Using [N] -> resets to 15%.",
                    "(Green: ≥45%; Red: ≤15% )",

                    ' ',
                    "Hits 0 → Corruption (1-3 [XX]).",
                    ' ',
                    "What it means:",
                    "Go for more ■ immediately",
                    "after you use [N]"
                ],
                
            },
            {
                "title": "SCORING: TIME",
                "content": [
                    "• Energy Loss: ",
                    "lower is better",
                    " ",
                    "Timed loss every ~2s:",
                    "Fast/Hardcore: 15 x Drain",
                    "Classic: 2 x Drain",
                    "(~1 pt/2s at start)",
                    " ",
                ],
                
            },

            {
                "title": "SCORING: ENDING",
                "content": [
                    "When you press [K] to end:",
                    "Fast/Hardcore:",
                    "  +350 per remaining ■",
                    "Classic:",
                    "  +125 per remaining ■",
                    " ",
                    "Classic plan: reach 2-3 ■,",
                    "then submit to cap time."
                ],
                
            },
            {
                "title": "INTERACTIVE: SWEEPING",
                "content": [
                    "Sweeping drill:",
                    " ",
                    "Use + flips to push ■",
                    "line-by-line into sinks:",
                    "[XX] and [!!].",
                    " ",
                    "This is a core strat that",
                    "helps you tackle clingy ■",
                    "with ease",
                    "(used a lot in the full",
                    "game).               ",
                ],
                
            },


            {
                "title": "MODES:",
                "content": [
                    "The game has 3 unique flavors:",
                    "                          ",
                    "• Fast Mode (FW!!!)",
                    "• Classic Mode (Depression)",
                    "• Hardcore Mode (Harder Fast)",
                    "                          ",
                    "Note: scoring/expected play",
                    "-style can vary depending on",
                    "the gamemode.",
                    "                          ",
                    "Continued on Next Page..."
                ],
                
            },
            {
                "title": "MODES:",
                "content": [
                    "• Fast Mode",
                    "Cons: ",
                    "  > Fastest inte. degredation",
                    "    - explosions come fast",
                    "  > Fastest timed score drop",
                    "    - better be quick!",
                    "                          ",
                    "Pros:",
                    "  > Starts w/ the most",
                    "    perma-off [XX] tiles",
                    "    - less ON tiles to deal",
                    "    with yourself (++++)",
                    "                          ",
                    "Continued on Next Page..."
                    
                ],
                
            },
            {
                "title": "MODES:",
                "content": [
                    "• Fast Mode",
                    "Note:",
                    "  > You're not expected to ",
                    "    quit by pressing [K] in",
                    "    modes outside than Classic",
                    "    (Up to 350pts per tile!)"
                ]
             },
            {
                "title": "MODES:",
                "content": [
                    "• Classic Mode",
                    "A purists' puzzle solving",
                    " > No Integrity system.",
                    " > No [XX]/[!!] at start.",
                    " > Timed loss: 2 x Drain",
                    "   (~1 pt/2s at start).",
                    " > Ending: +125 per ■.",
                    " ",
                    "Continued on Next Page..."
                ],
                
            },
            {
                "title": "MODES:",
                "content": [
                    "Tips:",
                    " > Rush to 0-5 ■ left",
                    " > Don't over-perfect",
                    " > Press [K] once done"
                    "                          ",
                    "                          ",
                    "Continued on Next Page..."
                ],
                
            },

            {
                "title": "MODES:",
                "content": [
                    "• Hardcore Mode",
                    "  > Basically Fast Mode",
                    "  > Starts with way less [XX]",
                    "    tiles - as I said, corrup",
                    "    -tion tiles are there to",
                    '    help you.',
                    "    (nobody believed me)",
                    "  > Harder. ",
                    "    You can't as easily sweep",
                    "    all your remaining ONs",
                    "    under the [XX]s. ",
                    "    ",
                    "                          ",
                    "Continued on Next Page..."
                    
                ],
                
            },
            {
                "title": "MODES:",
                "content": [
                    "• Hardcore Mode",
                    "  > Again, early quitting is",
                    "    not encouraged in this",
                    "    mode; but don't forget",
                    "    to do it in Classic.  ",
                    "                            ",
                    "Continued on Next Page..."
                ]
             },
             {
                 "title": "FINAL WORDS",
                "content": [
                    "  > Again, thank you again",
                    "    for playing. A LOT of  ",
                    "    thoughts were put into ",
                    "    this this to make it ",
                    "    happen.                ",
                    " ",
                    "  > A saved demo is randomly",
                    '    loaded from disk and shown',
                    "    on the main menu.       ",
                    "               ",
                    '  > Demo Recording can be',
                    '    turned on in Settings.'
                ]
             },
             {
                 "title": "FINAL TIPS",
                "content": [
                    "  > Recorded Demos are saved to",
                    '    your "Saved Demos" folder,',
                    "    and accessible thru the",
                    '''    Demo Browser (main''',
                    '    menu)',
                    ' ',
                    "  > A cloud scoreboard feature",
                    "    is available fpr users with",
                    '    a working internet connect',
                    "    -ion and a valid url file. ",
                    ' ',
                    "  > Otherwise, all playdata is",
                    "    saved offline."
                ]
             },

            {
                "title": "Tutorial Complete!",
                "content": [
                    "Congratulations!",
                    "You completed the tutorial!",
                    "                           ",
                    "Press ESC to return to main menu",
                    "and start the game!",
                ],
                
            }
        ]

def run_tutorial(win,playback_speed=2.5):
    curses.start_color()
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK) 
    curses.init_pair(10,curses.COLOR_WHITE,curses.COLOR_BLACK)
    
    tutorial = GameTutorial(player_name="")
    win.clear()
    curses.curs_set(0) 
    win.keypad(True)

    SCREEN_WIDTH = 68
    SCREEN_HEIGHT = 17


    # Set colors
    TITLE_COLOR = curses.color_pair(2) | curses.A_BOLD
    HIGHLIGHT_COLOR = curses.color_pair(2) | curses.A_BOLD
    TEXT_COLOR = curses.color_pair(10)


    while True:
        #region draws the tutorial
        step = tutorial.tutorial_steps[tutorial.current_step]
        win.clear()
        
        title = step["title"]
        #title_dash = "-" * 4
        #title_complete = f"{title_dash}{title}{title_dash}"
        title_complete = f"> {title}"

        win.addstr(2, 3, title_complete, TITLE_COLOR)
        for x in (1,34,67):#pretty vertical lines
            for y in range(15):    
                win.addstr(2+y,x,"│") #restores the overwritten lines


        
        # Display content with proper formatting
        start_y = 3
        current_line = 0
        
        for line in step["content"]:
            pos_y = start_y + current_line
            if line.startswith("•") or line.startswith(("1.","2.","3.","4.","5.")):
                win.addstr(pos_y, 3, line, HIGHLIGHT_COLOR)
            elif line == "":
                continue
            else:
                win.addstr(pos_y, 3, line, TEXT_COLOR)
            current_line += 1

        #gameplay_trial_instance.run_a_frame(win, 'noinput')

        nav_text = f"{tutorial.current_step + 1}/{len(tutorial.tutorial_steps)}|←: Back|→: Next|ESC: Exit"
        if tutorial.current_step + 1 >9:
            nav_text = f"{tutorial.current_step + 1}/{len(tutorial.tutorial_steps)}|←: Back|→: Next|ESC:Exit"

        nav_x = 2

        try: #FIXED FR
            win.addstr(SCREEN_HEIGHT - 1, nav_x+1, nav_text, TEXT_COLOR)
        except: 
            pass

        win.refresh()

        #endregion
        if tutorial.current_step==0: #first step
            win.nodelay(False)
            for y in range(2,17):
                win.addstr(y,36,' '*30) #clears out the right panel
            for y in range(15):    
                win.addstr(2+y,34," ")
                win.addstr(2+y,67,"│") #restores the overwritten lines
            #main_menu.draw_logo(win,x_offset=33,y_offset=7)


            y_ofst=3;x_ofst=35

            ascii_art="""
⢕⢕⢕⢕⠁⢜⠕⢁⣴⣿⡇⢓⢕⢵⢐⢕⢕⠕⢁⣾⢿⣧⠑⢕⢕⠄⢑⢕⠅⢕ 
⢕⢕⠵⢁⠔⢁⣤⣤⣶⣶⣶⡐⣕⢽⠐⢕⠕⣡⣾⣶⣶⣶⣤⡁⢓⢕⠄⢑⢅⢑
⠍⣧⠄⣶⣾⣿⣿⣿⣿⣿⣿⣷⣔⢕⢄⢡⣾⣿⣿⣿⣿⣿⣿⣿⣦⡑⢕⢤⠱⢐
⢠⢕⠅⣾⣿⠋⢿⣿⣿⣿⠉⣿⣿⣷⣦⣶⣽⣿⣿⠈⣿⣿⣿⣿⠏⢹⣷⣷⡅⢐
⣔⢕⢥⢻⣿⡀⠈⠛⠛⠁⢠⣿⣿⣿⣿⣿⣿⣿⣿⡀⠈⠛⠛⠁⠄⣼⣿⣿⡇⢔
⢕⢕⢽⢸⢟⢟⢖⢖⢤⣶⡟⢻⣿⡿⠻⣿⣿⡟⢀⣿⣦⢤⢤⢔⢞⢿⢿⣿⠁⢕
⢕⢕⠅⣐⢕⢕⢕⢕⢕⣿⣿⡄⠛⢀⣦⠈⠛⢁⣼⣿⢗⢕⢕⢕⢕⢕⢕⡏⣘⢕
⢕⢕⠅⢓⣕⣕⣕⣕⣵⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣷⣕⢕⢕⢕⢕⡵⢀⢕⢕
⢑⢕⠃⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⢕⢕⢕
⣆⢕⠄⢱⣄⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢁⢕⢕⠕⢁
"""

            list = ascii_art.split("\n")  

            for dy,string in enumerate(list):     
                win.addstr(y_ofst+dy,x_ofst,string,HIGHLIGHT_COLOR)
            text = '⇧ (totally irrelavant)'
            win.addstr(14,65-len(text),text)



            win.refresh()

            key = win.getch()

            if key == curses.KEY_RIGHT:# next page
                tutorial.current_step += 1
            elif key == 27:  # ESC to exit
                return 0
            


        elif tutorial.current_step in (1,2,3):
            win.nodelay(True)
            if tutorial.current_step == 1: #initializes only once
                try: _ = game_instance 
                except NameError: 
                    game_instance = game_nonblock(x_offset=0, y_offset=0)
            elif tutorial.current_step == 2 and sum('00' == tile for line in game_instance.map_data for tile in line) == 0:
                for boom in range(15): 
                    game_instance.blow(random.randint(0, 14), random.randint(0, 14))
                game_instance.flash_safe(win), win.refresh(); time.sleep(0.15)


            while True: #this loop is broken out once per page change.
                try: key = win.getch()
                except: pass
                if key!=-1: translated_key = chr(key)
                else:translated_key='noinput'
                game_instance.run_a_frame(win,translated_key)
                win.refresh()
                if key == curses.KEY_LEFT:# previous page
                    if tutorial.current_step > 0:
                        tutorial.current_step -= 1
                    break
                elif key == curses.KEY_RIGHT:# next page
                    tutorial.current_step += 1
                    break
                elif key == 27:  # ESC to exit
                    return
                time.sleep(0.1)


        elif tutorial.current_step in (4,5):
            win.nodelay(True)
            if tutorial.current_step == 4: #initializes only once
                allowed_ors=4
                try: _ = or_trial_instance 
                except NameError: 
                    or_trial_instance = game_nonblock(x_offset=0, y_offset=0,designated_map=[['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0'], ['0', '0', '0', '1','0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0','0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']])
            elif tutorial.current_step == 5 and sum('00' == tile for line in or_trial_instance.map_data for tile in line) == 0:
                for _ in range(2): 
                    try:    
                        or_trial_instance.blow(*random.choice([(y,x) for y,row in enumerate(or_trial_instance.map_data) for x,item in enumerate(row) if item=='1']))
                    except: pass
                or_trial_instance.flash_safe(win), win.refresh(); time.sleep(0.15)


            while True: #this loop is broken out once per page change.
                try: key = win.getch()
                except: pass
                if key!=-1: translated_key = chr(key)
                else:translated_key='noinput'
                if translated_key=='n': 
                    if allowed_ors>0:    
                        allowed_ors-=1
                    else: translated_key='noinput'
                or_trial_instance.run_a_frame(win,translated_key)
                win.refresh()
                if key == curses.KEY_LEFT:# previous page
                    if tutorial.current_step > 0:
                        tutorial.current_step -= 1
                    break
                elif key == curses.KEY_RIGHT:# next page
                    tutorial.current_step += 1
                    break
                elif key == 27:  # ESC to exit
                    return
                time.sleep(0.1)

        elif tutorial.current_step in (6,7,8,9,10):
            win.nodelay(True)
            win.addstr(y,36,' '*30) #clears out the right panel
            for y in range(15):    
                win.addstr(2+y,34,"│");win.addstr(2+y,67,"│") #restores the overwritten lines
            win.addstr(8,35,"─"*32)
            text=' SYSTEM LOG '
            win.addstr(8,(34+67)//2-len(text)//2+1,text)
            win.addch(8,34,'├');win.addch(8,67,'┤')
            win.addstr(10,36,'[!] This is where messages are')
            win.addstr(11,36,'delivered!')

            try: _ = time_zero
            except NameError:
                time_zero=time.monotonic()
            while True:
                try: key = win.getch()
                except: pass
                neg_time_passed = (time_zero-time.monotonic())
                if neg_time_passed <-10:
                    win.addstr(12,36,'[!] You might get some tips/')
                    win.addstr(13,36,'tricks from us here as well!')
                if neg_time_passed <-20:
                    win.addstr(14,36,'[!] Enjoy the game!')


                win.addstr(2,36,'POWER DRAIN:')
                win.addstr(4,36,'INTEGRITY INDEX:')
                win.addstr(6,36,'ENERGY LOSS:')
                score = int(neg_time_passed/2)*5
                powr_tuple = (max(0,225*0.45+2*neg_time_passed),225)
                crpt_tuple = (-time.monotonic()%10,10)
                #if tutorial.current_step == 8:
                    #crpt_tuple = ((4.51,10),(1.4,10))[time.monotonic()%1<0.5]
                for y in (3,5):
                    win.addstr(y, 36, '-'*30)

                #region indicators
                    #Power Drain (Grid) indicator
                if powr_tuple[0] / powr_tuple[1] < 0.20:                      
                    win.addstr(3, 36, '^'*(int(30 * (powr_tuple[0] / powr_tuple[1]))),curses.color_pair(1))
                elif powr_tuple[0] / powr_tuple[1] < 0.40:
                    win.addstr(3, 36, '^'*(int(30 * (powr_tuple[0] / powr_tuple[1]))),curses.color_pair(2)) 
                elif powr_tuple[0] / powr_tuple[1] < 0.034: 
                    win.addstr(3, 36, '-'*30,curses.color_pair(2))            
                else:
                    win.addstr(3, 36, '^'*(int(30 * (powr_tuple[0] / powr_tuple[1]))),curses.color_pair(3))
                if time.monotonic()%1>0.5:     #Flashes if progress made
                    win.addstr(3, 36+max(0,-1+int(30 * (powr_tuple[0] / powr_tuple[1]))),'█')


        
                #Corruption Countdown indicator
                if crpt_tuple[0] / crpt_tuple[1] < 0.033:                   
                    win.addstr(5, 36, '-'*30,curses.color_pair(3))          
                elif crpt_tuple[0] / crpt_tuple[1] < 0.15: 
                    win.addstr(5, 36, '^'*(int(30 * (crpt_tuple[0] / crpt_tuple[1]))),curses.color_pair(3))
                elif crpt_tuple[0] / crpt_tuple[1] < 0.45:
                    win.addstr(5, 36, '^'*(int(30 * (crpt_tuple[0] / crpt_tuple[1]))),curses.color_pair(2)) 
                else:
                    win.addstr(5, 36, '^'*(int(30 * (crpt_tuple[0] / crpt_tuple[1]))),curses.color_pair(1))
                    
                #Energy Loss (Counter) Indicator
                if score in range(0,-501,-1):                                        
                    win.addstr(7, 36, str(score),curses.color_pair(1)) #Green
                elif score in range(-501,-1001,-1):
                    win.addstr(7, 36, str(score),curses.color_pair(2)) #Yellow
                else:
                    win.addstr(7, 36, str(score),curses.color_pair(3)) #Red
                if time.monotonic()%1<=0.5: #flashes
                    win.addstr(7, 36, ' '*len(str(score)),curses.color_pair(1))
                #endregion






                win.refresh()
                if key == curses.KEY_LEFT:# previous page
                    if tutorial.current_step > 0:
                        tutorial.current_step -= 1
                    break
                elif key == curses.KEY_RIGHT:# next page
                    tutorial.current_step += 1
                    break
                elif key == 27:  # ESC to exit
                    return
                time.sleep(0.1)
        elif tutorial.current_step in (11,):
            win.nodelay(True)
            if tutorial.current_step == 11: #initializes only once
                try: _ = sweeping_trial_instance 
                except NameError: 
                    sweeping_trial_instance = game_nonblock(x_offset=0, y_offset=0,designated_map=[['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '00', '00', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00', '00', '00', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00', '11', '00', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '00', '00', '00', '00'], ['0','0', '0', '0', '0', '0', '0', '0', '1', '0', '00', '00', '00', '1', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00', '00', '00', '1', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00', '00', '00', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '00', '00', '00', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '00', '00', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00', '00', '00', '1'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00', '00', '00', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '00', '00', '00', '00'], ['0', '0', '0', '0','0', '0', '0', '0', '1', '0', '0', '00', '1', '00', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0','0', '0', '00', '00', '00'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00', '00']])


            while True: #this loop is broken out once per page change.
                try: key = win.getch()
                except: pass
                if key!=-1: translated_key = chr(key)
                else:translated_key='noinput'
                sweeping_trial_instance.run_a_frame(win,translated_key)
                win.refresh()
                if key == curses.KEY_LEFT:# previous page
                    if tutorial.current_step > 0:
                        tutorial.current_step -= 1
                    break
                elif key == curses.KEY_RIGHT:# next page
                    tutorial.current_step += 1
                    break
                elif key == 27:  # ESC to exit
                    return
                time.sleep(0.1)


        elif tutorial.current_step in (12,13,14):
            win.nodelay(True)
            try: fast_playback
            except NameError: fast_playback=playback_window(x_offset=36,y_offset=2,play_tutorial_demo='Fast')
            while True:
                try: key = win.getch()
                except: pass

                fast_playback.run_a_frame(win)
                win.refresh()
                if key == curses.KEY_LEFT:# previous page
                    if tutorial.current_step > 0:
                        tutorial.current_step -= 1
                    break
                elif key == curses.KEY_RIGHT:# next page
                    tutorial.current_step += 1
                    break
                elif key == 27:  # ESC to exit
                    return
                time.sleep(0.1/playback_speed)

        elif tutorial.current_step in (15,16):
            win.nodelay(True)
            try: classic_playback
            except NameError: classic_playback=playback_window(x_offset=36,y_offset=2,play_tutorial_demo='Classic')
            while True:
                try: key = win.getch()
                except: pass

                classic_playback.run_a_frame(win)
                win.refresh()
                if key == curses.KEY_LEFT:# previous page
                    if tutorial.current_step > 0:
                        tutorial.current_step -= 1
                    break
                elif key == curses.KEY_RIGHT:# next page
                    tutorial.current_step += 1
                    break
                elif key == 27:  # ESC to exit
                    return
                time.sleep(0.1/playback_speed)
        elif tutorial.current_step in (17,18):
            win.nodelay(True)
            try: hardcore_playback
            except NameError: hardcore_playback=playback_window(x_offset=36,y_offset=2,play_tutorial_demo='Hardcore')
            while True:
                try: key = win.getch()
                except: pass

                hardcore_playback.run_a_frame(win)
                win.refresh()
                if key == curses.KEY_LEFT:# previous page
                    if tutorial.current_step > 0:
                        tutorial.current_step -= 1
                    break
                elif key == curses.KEY_RIGHT:# next page
                    tutorial.current_step += 1
                    break
                elif key == 27:  # ESC to exit
                    return
                time.sleep(0.1/playback_speed)

        elif tutorial.current_step in (19,20):
            win.nodelay(True)
            try: _ = tact1_game_instance 
            except NameError: 
                tact1_game_instance = game_nonblock(x_offset=0, y_offset=0,designated_map=[['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '1', '1', '0', '1', '1', '0', '0', '0', '0', '0'], ['0', '0', '0', '0','1', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0'], ['0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0'], ['0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0'], ['0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0'], ['0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0','0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']])
            while True: #this loop is broken out once per page change.
                try: key = win.getch()
                except: pass
                if key!=-1: translated_key = chr(key)
                else:translated_key='noinput'
                tact1_game_instance.run_a_frame(win,translated_key)
                win.refresh()
                if key == curses.KEY_LEFT:# previous page
                    if tutorial.current_step > 0:
                        tutorial.current_step -= 1
                    break
                elif key == curses.KEY_RIGHT:# next page
                    tutorial.current_step += 1
                    break
                elif key == 27:  # ESC to exit
                    return
                time.sleep(0.1)
        


        elif tutorial.current_step == 120:
            win.nodelay(False)
            ascii_art = """
\ \Q
\ \Q
    \ \Q
    \/`\Q
    |   \   _+,_Q
    \   (_[____]_Q
    '._|.-._.-._] ////////Q
^^^^^^^^^^^^'-' '-'^^^^^^^^^^^"""    
            list = ascii_art.split("Q")  
            for dy,string in enumerate(list):     
                win.addstr(5+dy,36,string.replace('\n',''))
            win.refresh()
            key = win.getch()

            if key == curses.KEY_LEFT:# previous page
                if tutorial.current_step > 0:
                    tutorial.current_step -= 1
                break
            elif key == curses.KEY_RIGHT:# next page
                tutorial.current_step += 1
                break
            elif key == 27:  # ESC to exit
                return


        elif tutorial.current_step == 201:
            win.nodelay(False)
            for y in range(15):    
                win.addstr(2+y,34," ")

            x_ofst=3;y_ofst=38
            ascii_art = """
⢸⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣿⣿⣿⣿⣷⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⠀⠀⠀⠀⠀
⢸⣿⣿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠀⠀⠀⠀⠀
⢸⣿⡏⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀
⢸⣿⠃⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀
⢸⡟⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀
⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀
⢸⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀
⠘⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀
⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀
"""
            list = ascii_art.split("\n")  
            for dy,string in enumerate(list):     
                win.addstr(x_ofst+dy,y_ofst,string,HIGHLIGHT_COLOR)
            win.refresh()
            key = win.getch()

            if key == curses.KEY_LEFT:# previous page
                if tutorial.current_step > 0:
                    tutorial.current_step -= 1
                #break
            elif key == curses.KEY_RIGHT:# next page
                tutorial.current_step += 1
                #break
            elif key == 27:  # ESC to exit
                return




            
            
        else:
            win.nodelay(False)
            key = win.getch()

            if key == curses.KEY_LEFT:# previous page
                if tutorial.current_step > 0:
                    tutorial.current_step -= 1
                #break
            elif key == curses.KEY_RIGHT:# next page
                tutorial.current_step += 1
                if tutorial.current_step==len(tutorial.tutorial_steps):return 0 
                #break
            elif key == 27:  # ESC to exit
                return
        #region what is this        
        
"""     
       #if step.get("wait_for_move"):           
                if key in map(ord,'wWaAsSdD'):#[ord("w"),ord("W"),ord("a"),ord("A"),ord("s"),ord("S"),ord("d"),ord("D")]:
                    break
                    
            #elif step.get("wait_for_flip"):
                if key in [ord("c"),ord("C")]:
                    break
                    
            #elif step.get("wait_for_move_and_flip"):
                if key in [ord("c"),ord("C"),ord("w"),ord("W"),ord("a"),ord("A"),ord("s"),ord("S"),ord("d"),ord("D")]:
                    movement = 0
                    flipping = 0
                    while movement < 2 or flipping < 2 :
                        if key in [ord("w"),ord("W"),ord("a"),ord("A"),ord("s"),ord("S"),ord("d"),ord("D")]:
                            movement += 1
                        elif key in [ord("c"),ord("C")]:
                            flipping += 1
"""            #endregion



if __name__ == "__main__":
    curses.wrapper(run_tutorial)
    print("Starting tutorial...")
    print("Tutorial completed!")
