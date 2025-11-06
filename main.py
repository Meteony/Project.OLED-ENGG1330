"""
The game goes through 10 ticks per second
display dimensions: x: 68 = [0,67] = 1 + (33 + 1 + 33); y: 17 = [0,16]

Complete curses rewrite
Changed the directories of several file IO's
Attempts to fix the flickering once and for all

─ 
^ Always use this hline plz

"""
while True:
    import time
    import curses
    import random
    import os
    import getpass
    import ast
    from library.connectivity import *
    from library.highscore_browser import highscore_browser
    from library.demo_browser import demo_browser
    from library.print_cutscene import print_clear,gameover_cutscene
    from library.game import game
    from library.alpha import alpha




    #region file directories initialization
    current_dir = os.getcwd()
    if not os.path.isdir('Saved Demos'):
        os.makedirs('Saved Demos')
    demo_dir = current_dir+"//Saved Demos//"
    tutorial_dir = current_dir+"//Tutorial Files//"

    #endregion
    



    #region Cloud Connectivity

    # Standard library only

    #endregion



#region -------------------------------playback/main menu------------------------------------------


    #region hs/demo select browsers
    #endregion

    def pref_save():        #<----- Saves/Initializes the config file (tied to game() attributes)
        pref_data=dict()
        pref_data["enablerecording"]=getattr(game,"enablerecording",False)
        pref_data["skipcutscene"]=getattr(game,"skipcutscene",False)
        pref_data["cloudconnectivity"]=getattr(game,"cloudconnectivity",True)
        with open("oled_pref.data","w",encoding="utf-8") as pref: 
            pref.write(str(pref_data))
    def pref_read():        #<----- Reads the config file & syncs the ER+SC settings (tied to game() attributes)
        with open("oled_pref.data","r",encoding="utf-8") as pref:
            pref_data = ast.literal_eval(pref.readline())
            game.enablerecording = pref_data["enablerecording"]
            game.skipcutscene = pref_data["skipcutscene"]
            game.cloudconnectivity = pref_data["cloudconnectivity"]

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
                    selected_demo=demo_browser(win=win,demo_directory=demo_dir) #demo_select()
                    if selected_demo == 0: 
                        win.nodelay(True)
                        win.erase()
                        #curses.wrapper(main_menu.run(win=win,destination='main')) #none selected
                    else:   
                        game.replayfile = selected_demo
                        game.replaymode = True
                        return 'exit_menu_only'
                elif selector == 3:
                    
                    highscore_browser(win=win,enableconnectivity=getattr(game,"cloudconnectivity",False))
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
                elif selector == 4: 
                    try:
                        from library.tutorial import run_tutorial
                        run_tutorial(win)
                        main_menu.pop_notif(win,"""First time? Try out Slow' Mo in Bonus Gamemodes!""",color=2,interval=5)
                        win.nodelay(True),win.erase()
                        main_menu.currentwin='main-settings-bonusplay'
                        return 'change_menu'
                        
                    #win.nodelay(True),win.refresh()
                    except: 
                        main_menu.pop_notif(win,'An error has occured.')
                        win.nodelay(True),win.erase()
                        main_menu.currentwin='main'
                        return 'change_menu'


                
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
                elif selector == 2: 
                    win.erase()
                    alpha(win)
                    win.erase(),win.nodelay(True)
                    #game.mode = 'alpha'; return 'exit_menu_only'
                elif selector == 3:
                    main_menu.currentwin = 'main-settings'
                    return 'change_menu'
    



        



        @staticmethod
        def run(win,erase_sec=2,arrive_at_menu = 'main',specified_selector = None):

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
            selector_pos = 1 if specified_selector == None else specified_selector
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
                    key_drain = win.getkey().lower()
                    while True:
                        if not key_queued:
                            key_queued.append(key_drain) 
                        elif key_queued[-1]!=key_drain:
                            key_queued.append(key_drain)
                        key_drain = win.getkey().lower()
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
                    if key in ('s','key_down'):
                        try:    
                            selector_pos = min(selector_pos+1,num_avai_options)
                        except UnboundLocalError: selector_pos=1
                    if key in ('w','key_up'):
                        try:
                            selector_pos = max(1,selector_pos-1)
                        except UnboundLocalError: selector_pos=1

                    if key in ('c','b','\n','\r','key_enter'): #selection
                        selection_result = main_menu.handleselection(main_menu.currentwin,selector_pos,win)
                        if selection_result == 'exit_menu_only':
                            break
                        if selection_result == 'exit':
                            main_menu.exit = True
                            break

                        if selection_result == 'change_menu':
                            selector_pos = 1
                    if key in ('x','KEY_BACKSPACE','\b','\x7f'): #Prev. Menu
                        if '-' in main_menu.currentwin:
                            main_menu.currentwin='-'.join(main_menu.currentwin.split('-')[:-1])
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
        
        
        #endregion

    curses.wrapper(main_menu.run)
           
    if getattr(main_menu,'exit',False): break       #<----Quit the program





























    #############################################################################################
    ############################### Main Game Function ##########################################
    #Retrofitting hard
    wrapper = lambda win:game(win=win,mode=getattr(game,"mode",None),replay_mode=
                              getattr(game,"replaymode",False),
                              replay_file=getattr(game,"replayfile",None),
                              enable_recording=getattr(game,"enablerecording",False))
    curses.wrapper(wrapper)







    ################################################################################
    ######################## Ending sequence #######################################

    end_score, end_ticks = game.finalstats          #Fetch the stats


    def score_splash(win): #Tiny curses results screen
        time.sleep(0.5)
        curses.curs_set(0); win.nodelay(True); curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        
        if getattr(game,"newhighscore",False): #New highscores give a special splashscreen
            win.addstr(7, 0, '█'*69, curses.color_pair(4))
            highscore_message = f'''[>] NEW LOCAL HIGHSCORE [{game.finalstats[0]}]'''
            win.addstr(8, 0, f'{" "+highscore_message+" ":█^69}', curses.color_pair(4))
            win.addstr(9, 0, '█'*69, curses.color_pair(4))
            win.noutrefresh(); curses.doupdate()
            time.sleep(5)
            game.newhighscore = False
        else:
            if game.finalstats[0] in range(0,-501,-1):
                color=1
            elif game.finalstats[0] in range(0,-1001,-1):
                color=2
            else: color=3
            """         #Full screen
            for i in (0,1,2,3,4,5,6,10,11,12,13,14,15,16):
                win.addstr(i, 0, '█'*69, curses.color_pair(color))
            """
            win.addstr(7, 0, '█'*69, curses.color_pair(color))
            win.addstr(8, 0, f'{" RATINGS: "+("PERFECT","GOOD","SUBOPTIMAL")[color-1]+" ["+str(game.finalstats[0])+"] ":█^69}', curses.color_pair(color))
            win.addstr(9, 0, '█'*69, curses.color_pair(color))
            win.noutrefresh(); curses.doupdate()
            time.sleep(5)
        if getattr(game,"enablerecording", False) and not getattr(game,"replaymode",False): #"demo saved" screen
            win.addstr(7, 0, '█'*69, curses.color_pair(4))
            demo_saved_message = f'''[>] DEMO SAVED TO "{getattr(game,'saved_demo_name','N/A').upper()}"'''
            win.addstr(8, 0, f'{" "+demo_saved_message+" ":█^69}', curses.color_pair(4))
            win.addstr(9, 0, '█'*69, curses.color_pair(4))
            win.noutrefresh(); curses.doupdate()
            time.sleep(5)

        win.erase(); win.noutrefresh(); curses.doupdate()
        time.sleep(1)

    curses.wrapper(score_splash)


    gameover_cutscene(skip=getattr(game,"skipcutscene",False),end_score=end_score,end_ticks=end_ticks)



    time.sleep(0) #restarts... i assume
