import os,curses,time,getpass,random,ast
if __name__=='__main__': #Directory fix
    os.chdir(os.getcwd().strip('//library'))
    from connectivity import *

else:
    from library.connectivity import *
current_dir = os.getcwd()

demo_dir = current_dir+"//Saved Demos//"

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


def game(win,mode='hardcore',replay_mode=False,replay_file='Default.oled',enable_recording=True):
    game.mode = mode
    game.enablerecording = enable_recording
    game.replaymode=replay_mode
    if replay_mode: game.replayfile=replay_file

    game.player_id=getpass.getuser()
    tile_texture_mapping = {
            "1": "██",  #ON
            "0": "░░",  #OFF
            "00": "XX",  #CORR
            '11': "!!"
        }
    if getattr(game,"replaymode",False):  #<--------------------------Replay mode      
            
        curses.curs_set(0)
        win.nodelay(True)
        win.keypad(True)
        selector = [0, 0]
        tick = 0
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        # initialize_game_map
        map_size = (15, 15)  # create the map
        selector = [8, 8]
        map_data = []
        map_data_temp = []
        for _ in range(map_size[0]):
            map_data_temp += ["0"]
        for _ in range(map_size[1]):
            map_data.append(map_data_temp[:])
        

        ######################################################## <-----------Reads in the demo
        with open(demo_dir+game.replayfile,'r',encoding="utf-8") as demo:
            game.demo = ast.literal_eval(demo.readline())
            game.mode=str(demo.readline())[:-1] #<---Cuts off the \n
            game.player=str(demo.readline())[:-1]
            game.time=str(demo.readline())[:-1]
            game.demostats = ast.literal_eval(demo.readline())
            game.demoscore = game.demostats[0]
        tick=min(game.demo)-1; key='noinput' #Skips to the first tick with data in demo, sets key to default
        #########################################################
        
        powr_tuple = (225, 225) #Safe default states for the playback
        crpt_tuple = (225, 225)
        score = 0
        message = ''

        
        

        while True:
            tick += 1

            try: #<------Matches the tick to see if there's stored data for this frame
                #Format:
                # [key,selector,(map_data),(powr_tuple),(crpt_tuple),score,message,lwst_powr_tuple_rc]
                fetched_stat = game.demo[tick]
                if fetched_stat[0]!=None:
                    key = fetched_stat[0]
                if fetched_stat[1]!=None:
                    selector = fetched_stat[1]
                if fetched_stat[2]!=None:
                    map_data = ast.literal_eval(fetched_stat[2])
                if fetched_stat[3]!=None:
                    powr_tuple = fetched_stat[3]
                if fetched_stat[4]!=None:
                    crpt_tuple = fetched_stat[4]      
                if fetched_stat[5]!=None:
                    score = fetched_stat[5]
                if fetched_stat[6]!=None:
                    message = fetched_stat[6]
                if len(fetched_stat) == 8: #Compatibility for legacy (<0.45) demos
                    if fetched_stat[7]!=None:
                        lwst_powr_tuple_rc = fetched_stat[7]
                else: lwst_powr_tuple_rc =225


            except: 
                pass


            if tick%20==0:  # clears the win buffer
                win.erase()  # erase buffer


            powr_indicator_str = "-"*30; crpt_indicator_str = "-"*30

            map_data_visual = []
            for row in range(len(map_data)):
                map_data_visual.append("".join(tile_texture_mapping[item] for item in map_data[row]))
            ui_elements = [
                f' │ │ {"POWER DRAIN:":<30} │ ',
                f" │ │ {powr_indicator_str:<30} │ ",
                f' │ │ {r"""INTEGRITY INDEX:""":<30} │ ',
                f" │ │ {crpt_indicator_str:<30} │ ",
                f' │ │ {"ENERGY LOSS:":<30} │ ',
                f" │ │ {score:<30} │ ",
                f' │ ├─{" SYSTEM LOG ":─^30}─┤ ',
                f" │ │ {message[0:30]:^30} │ ",
                f" │ │ {message[30:60]:^30} │ ",
                f" │ │ {message[60:90]:^30} │ ",
                f" │ │ {message[90:120]:^30} │ ",
                f" │ │ {message[120:150]:^30} │ ",
                f" │ │ {message[150:180]:^30} │ ",
                f" │ │ {message[180:210]:^30} │ ",
                f" │ │ {message[210:240]:^30} │ ",
            ]
            ######################################################################
            ######################DISPLAY BELOW###################################
            try:
                win.addstr(0, 1, f"{'Pos: '+str(selector)+' |'+' Key: '+str(key):<66}")
                timestamp=f'Replay from {game.time}'
                win.addstr(0, 68-len(timestamp), timestamp)

                __title_element__ = f"{game.player} - {game.mode.capitalize()} [{game.demoscore}]" 
                win.addstr(1, 0, f" {' - - ─  ────────── '+__title_element__+' ──────────  ─ - - ':^67}")
                for y in range(15): #Draws the interface
                    win.addstr(2 + y, 0, " │ ")
                    current_line_rendered = 3
                    for x in range(15): #Map drawn by line
                        tile = tile_texture_mapping[map_data[y][x]]
                        win.addstr(2 + y, current_line_rendered, tile)
                        current_line_rendered += len(tile)
                    ui_elements_split = ui_elements[y][2:] #Draws the UI by line
                    win.addstr(2 + y, current_line_rendered, ui_elements_split)


                ###########################################################################################
                ################################## Colored Elements! ######################################

                    #Colored Cursor
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
                if lwst_powr_tuple_rc==powr_tuple[0] and tick%10 not in range(0,5):     #Flashes if progress made
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
                if tick%10<5 and score<-0: #flashes
                    win.addstr(7, 36, ' '*len(str(score)),curses.color_pair(1))


                if game.mode == 'classic': #Hide irrelevant indicators in classic mode                
                    win.addstr(2, 36,f'{"PROGRESS:":<30}')
                    win.addstr(4, 36, ' '*30)
                    win.addstr(5, 36, ' '*30)

            except:
                pass

    ##########################DISPLAY ABOVE############################################
    ###################################################################################


            if tick>=max(game.demo):    #<--------End-of-replay detection
                game.finalstats = tuple(game.demostats)
                for _ in range(3):  #<--End game flash anis
                    win.erase(); win.refresh()  #Clears the screen
                    flash_safe(win)
                    time.sleep(0.15)
                break           #<---------------------------------------------------------------Breaks main loop
            
            if key == 'n':      #Override Patch
                if not crpt_tuple[0] / crpt_tuple[1] <= 0.45: 
                    time.sleep(0.1);flash_safe(win);flash_safe(win);time.sleep(0.15)

            try: #<-------------------Pause/Skip implementation for replays (it looks for {m}/{k})
                replay_control = win.getkey()
                if replay_control == 'm':  #<-------------Pause the replay 
                    win.addstr(7, 0, '█'*69, curses.color_pair(2))
                    win.addstr(8, 0, f"{' PAUSED  - PRESS ANY KEY TO CONTINUE ':█^69}", curses.color_pair(2))
                    win.addstr(9, 0, '█'*69, curses.color_pair(2))
                    win.noutrefresh(); curses.doupdate()
                    time.sleep(0.25)
                    wait_for_key(win)   #Actually Halts the program
                    """
                    while True: # Also halts the program but while burning your CPU
                        try: 
                            if win.getkey() != 'KEY_RESIZE': break
                        except curses.error: pass   
                    """
                elif replay_control == 'k': #<----------Kills the replay
                    game.finalstats = tuple(game.demostats); game.skipcutscene = True
                    for _ in range(3):  #<--End game flash anis
                        win.erase(); win.refresh() #Clears the screen
                        flash_safe(win)
                        time.sleep(0.15)
                    break         #<---------------------------------------------------------------Breaks main loop

            except curses.error: pass         

            win.noutrefresh() # <------------- show changes
            curses.doupdate() 
            time.sleep(0.1)

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

        # initialize_game_map
        map_size = (15, 15)  # create the map
        selector = [8, 8]
        map_data = []
        map_data_temp = []
        for _ in range(map_size[0]):
            map_data_temp += ["0"]
        for _ in range(map_size[1]):
            map_data.append(map_data_temp[:])


        for _ in range(90): #Basic map generation
            flip(random.randint(0, 14), random.randint(0, 14), map_data)
        per_crpt_score_pen=150
    ###Gamemode
        if not hasattr(game,'mode'): #Safety line. Ensures that there is a gamemode
            game.mode='hardcore'

        if game.mode=='classic': #Mode-specific settings
            powr_loss_rate = 0
            max_per_2s_score_pen = 2 # Basically timer. -150 in 3mins
            per_rem_tile_score_pen = 125 #Allows for a few tiles
        elif game.mode=='standard':
            powr_loss_rate = 2
            max_per_2s_score_pen = 10 # Expected gameplay circa 3mins
            per_rem_tile_score_pen=350
        elif game.mode == 'hardcore':
            for _ in range(6):
                blow(random.randint(0, 14), random.randint(0, 14), map_data)
            powr_loss_rate = 7  #6 blows for hardcore. 
            max_per_2s_score_pen = 15
            per_rem_tile_score_pen=350
        else:  #Fast mode
            for _ in range(15):     #15 for fast
                blow(random.randint(0, 14), random.randint(0, 14), map_data)
            powr_loss_rate = 10 #Higher rate for fast
            max_per_2s_score_pen = 15
            per_rem_tile_score_pen=350

        # main loop
        tick = 0

        ##############################DISPLAY DEPENDENCIES
        

        powr_tuple = (122, 225)
        crpt_tuple = (450, 900)
        score = 0
        message = f"{'Game started ('+game.mode+' mode)':^30}"+' '*30+f"{'Minimize energy loss!':^30}"+f"""{'Eliminate all "■" tiles.':^30}"""+' '*30
        message += f"{r'{m} to pause; {k} to speedrun':^30}"
        message += f"{r'{b} & {n} for flip & override':^30}"+' '*30

        # < -------------------------------------------------------------------------Start of the loop
        while True:
            tick += 1
            if 1:   #Scheduled Messages
                if tick==150 and game.mode!='classic':
                    message = syslog_appended(r"""[!] When your power indicator flashes, the next eliminated  "■" tile guarantees a repair.""", message)
                if tick==450 and game.mode =='classic':
                    message = syslog_appended(r"""[!] Feeling stuck? You can press "k" to finalize your results.""", message)

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
                key_response(key, selector, map_data)
            except IndexError:key="noinput"
            
            MAX_QUEUE = 128 # Safety
            if len(key_queued) > MAX_QUEUE:
                del key_queued[:-MAX_QUEUE]
            #endregion
                        

            #region --------------------------------Game Rules-----------------------------------------
            if crpt_tuple[0] < 1: #Corruption, Corruption Grace, Override non-grace
                #Normal corruption behavior
                score_cache=score
                for _ in range(1,random.randint(2,4)):
                    blow(*locate_random_white_tile(map_data), map_data)
                    score -= per_crpt_score_pen #Corruption Score Penalty
                
                message = syslog_appended(f'{"[!] "+str(int((score - score_cache)/per_crpt_score_pen))+r"""x "■" [-"""+str(score_cache - score)+" ENERGY]"}', message)
                
                
                crpt_tuple=(396,900) #Penalty Burn-in countdown (910,900)
                powr_tuple = (sum (x == '1' for row in map_data[:] for x in row ),225)
                lwst_powr_tuple_rc = powr_tuple[0]

            #Power Indicator & Progress tracking & Gradual corruption
            powr_tuple = (sum (x == '1' for row in map_data[:] for x in row ),225)
            try: #Power tuple
                if powr_tuple[0]<lwst_powr_tuple_rc: #Reward! 
                    change=lwst_powr_tuple_rc-powr_tuple[0]
                    adder=200+round(100*(change/5))
                    lwst_powr_tuple_rc = powr_tuple[0]
                    crpt_tuple=(min(crpt_tuple[0]+adder,900),900)
                else: #Gradual Corruption
                    crpt_tuple = (crpt_tuple[0]-1*int(game.mode != 'classic')-(powr_loss_rate*powr_tuple[0]/powr_tuple[1]),crpt_tuple[1]) #Crank up 19 to reach the ending screen quick
            except: #Probably first few ticks. Bug prevention
                lwst_powr_tuple_rc = powr_tuple[0]
                crpt_tuple=(910,900)

            if tick > 9 and tick%20 == 0: #score drops as time passes
                score -= max(1,int(max_per_2s_score_pen* (powr_tuple[0] / powr_tuple[1])))
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
                f' │ ├─{" SYSTEM LOG ":─^30}─┤ ',
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
                name_element = getattr(game,"player_id",'N/A')
                win.addstr(0, 68-len(name_element), name_element)
                win.addstr(1, 0, f" {' - - ─  ────────── Project OLED - '+game.mode.capitalize()+' ──────────  ─ - - ':^67}")
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
                if lwst_powr_tuple_rc==powr_tuple[0] and tick%10 not in range(0,5):     #Flashing progress indicator
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
                    
                #Energy Loss Indicator
                if score in range(0,-501,-1):                                        
                    win.addstr(7, 36, str(score),curses.color_pair(1)) #Green
                elif score in range(-501,-1001,-1):
                    win.addstr(7, 36, str(score),curses.color_pair(2)) #Yellow
                else:
                    win.addstr(7, 36, str(score),curses.color_pair(3)) #Red
                if tick%10<5 and score<-0: #flashes
                            win.addstr(7, 36, ' '*len(str(score)),curses.color_pair(1))
            #endregion

                if game.mode == 'classic': #Hide irrelevant indicators in classic mode                
                    win.addstr(2, 36,f'{"PROGRESS:":<30}')
                    win.addstr(4, 36, ' '*30)
                    win.addstr(5, 36, ' '*30)




            except:
                pass
            #endregion
            

            #region --------------------------------Demo Cache------------------------------------------
            if getattr(game,"enablerecording", False): #<------------Caches the demo
                try: _ = game.rec
                except: game.rec=dict()
                try: _ = game.last_cached_stats 
                except:  game.last_cached_stats =dict()
                steps = 60
                crpt_tuple_rounded = ((crpt_tuple[1]/steps)*
                                    round(60*crpt_tuple[0]/crpt_tuple[1]),
                                    crpt_tuple[1])
                next_set_of_stats = []
                for id, value in enumerate((key,(selector[:]),str(map_data[:]),(powr_tuple),(crpt_tuple_rounded),score,message,lwst_powr_tuple_rc)):
                    if value not in game.last_cached_stats.values():
                        game.last_cached_stats[id] = value
                        next_set_of_stats.append(value)
                    else:
                        next_set_of_stats.append(None)
                if any(next_set_of_stats):    
                    game.rec[tick]=tuple(next_set_of_stats)
                
                    
                #Should be executed before the game ends to not miss the last tick hence the cache
            #endregion
            #region ------------------- Gameover Detection, Demo Writing, Scoreboard r/w --------------------
            if powr_tuple[0] < 1 or key=='k': #<--------------------End-of-game detection
                if not powr_tuple[0] < 1:   #Penalize quitting
                    score -= per_rem_tile_score_pen * powr_tuple[0] 
                game.finalstats = (score,tick)   #Saves the stats
                for _ in range(3):   #Cool flashes
                    win.erase()
                    win.refresh()
                    flash_safe(win)
                    time.sleep(0.15)
                
                if getattr(game,"enablerecording", False):#<--------------------Stores the demo
                    game.saved_demo_name = (
                    f"{str(getpass.getuser())[0]+str(getpass.getuser())[-1]}_"
                    f"{str(game.mode)[0]}_"
                    f"{time.strftime('%m%d%y_%H%M', time.localtime())}"
                    ".oled"
                    )

                    with open(demo_dir+game.saved_demo_name,'w',encoding="utf-8") as file: 
                        file.write(f"{str(game.rec)}\n")
                        file.write(f"{str(game.mode)}\n")
                        try:    
                            file.write(f"{str(getpass.getuser())}\n")
                            file.write(f'{time.strftime("%m-%d-%Y %H:%M:%S", time.localtime())}\n')
                            file.write(str(game.finalstats))
                        except: file.write("NA\nNA\n")
                #region Scoreboard Related (outputs: game.newhighscore)
                    #read & verify hs; outputs game.newhighscore = True/False
                all_sboard_entries=list()
                for file in os.listdir():
                    if file.endswith(".scoreboard"):
                        with open(file,'r',encoding="utf-8") as scoreboard:
                            all_sboard_entries.extend(
                                ast.literal_eval('['+''.join(scoreboard.readlines())+']')
                                )
                same_mode_sboard_entries = [i for i in all_sboard_entries if i[0] == game.mode]
                same_mode_sboard_entries.sort(key=lambda i:i[4],reverse=True)
                try:
                    if game.finalstats[0] > same_mode_sboard_entries[0][4]: #New highscore for this mode
                        game.newhighscore = True
                except IndexError: #No existing records
                        game.newhighscore = True
                
                scoreboard_new_entry=str(tuple((game.mode,getpass.getuser(),
                                        f'{time.strftime("%m-%d-%Y %H:%M:%S", time.localtime())}',
                                        game.finalstats[1],game.finalstats[0]
                    )))+','
                with open(f'{getpass.getuser()}.scoreboard','a',encoding="utf-8") as scoreboard: #writes to the scoreboard
                    scoreboard.write(scoreboard_new_entry)
                if getattr(game,"cloudconnectivity",False):
                    append_to_scoreboard(scoreboard_new_entry)
                #endregion
                break           #<-----------------------------------------------------------------END HERE
            #endregion
            #region ------------------------------ Pause & Override Button-------------------------------
            elif key=='m':        #Pause functionality
                win.addstr(7, 0, '█'*69, curses.color_pair(2))
                win.addstr(8, 0, f'{" PAUSED  - PRESS ANY KEY TO CONTINUE ":█^69}', curses.color_pair(2))
                win.addstr(9, 0, '█'*69, curses.color_pair(2))
                win.noutrefresh(); curses.doupdate()
                time.sleep(0.25)
                wait_for_key(win)
                """
                while True:
                    try: 
                        if win.getkey() != 'KEY_RESIZE': break
                    except curses.error: pass                
            """
            elif key == 'n':      #Override Patch
                if game.mode!='classic':
                    if game.mode == 'hardcore':
                        if crpt_tuple[0] / crpt_tuple[1] < 0.15: 
                            message = syslog_appended("[!] Insufficient integrity. Can't override.", message)                        
                        elif crpt_tuple[0] / crpt_tuple[1] < 0.45:
                            crpt_tuple=(100,900) #126
                            override(selector[1],selector[0],map_data)
                            message = syslog_appended(f"{'[!] Override completed!'}", message)
                            lwst_powr_tuple_rc = sum (x == '1' for row in map_data[:] for x in row)
                            time.sleep(0.1);flash_safe(win);flash_safe(win);time.sleep(0.15)
                        else:
                            new_value = max((crpt_tuple[0]-500),270)
                            crpt_tuple=(new_value,crpt_tuple[1])
                            override(selector[1],selector[0],map_data)
                            message = syslog_appended(f"{'[!] Override completed!'}", message)
                            lwst_powr_tuple_rc = sum (x == '1' for row in map_data[:] for x in row)
                            time.sleep(0.1);flash_safe(win);flash_safe(win);time.sleep(0.15)


                    else:    
                        if crpt_tuple[0] / crpt_tuple[1] <= 0.45: 
                            message = syslog_appended("[!] Insufficient integrity. Can't override.", message)                        
                        else:
                            crpt_tuple=(126,900)
                            override(selector[1],selector[0],map_data)
                            message = syslog_appended(f"{'[!] Override completed!'}", message)
                            lwst_powr_tuple_rc = sum (x == '1' for row in map_data[:] for x in row)
                            time.sleep(0.1);flash_safe(win);flash_safe(win);time.sleep(0.15)
                else:
                        message = syslog_appended("[!] Override is not enabled in Classic mode.", message)                        
                #endregion



            win.noutrefresh()
            curses.doupdate()  # <- show changes
            time.sleep(0.1)


def flip(y, x, map_data): # executed at {c}: modifies the map data (list) in-place
    map_size = (15, 15)
    flip_list = []
    flip_sequence = ((-1, 0), (1, 0), (0, 0), (0, -1), (0, 1))
    for delta_y, delta_x in flip_sequence:
        if (delta_y + int(y) in range(map_size[0])) and (delta_x + int(x) in range(map_size[1])):
            flip_list.append([y + delta_y, x + delta_x])
    for b, a in flip_list:
        if str(map_data[b][a]) == "1":
            map_data[b][a] = "0"
        elif str(map_data[b][a]) == "0":
            map_data[b][a] = "1"

def blow(y, x, map_data): # Corruption tile generation. Modifies map data in-place
    map_size = (15, 15)
    blow_list = []
    blow_sequence = ((-1, 0), (1, 0), (0, 0), (0, -1), (0, 1))
    for delta_y, delta_x in blow_sequence:
        if (delta_y + int(y) in range(map_size[0])) and (delta_x + int(x) in range(map_size[1])):
            blow_list.append([y + delta_y, x + delta_x])
    for b, a in blow_list:
        map_data[b][a] = "00"

def override(y, x, map_data): # Override. Modifies map data in-place
    map_size = (15, 15)
    override_list = []
    override_sequence = ((0, 0),)
    for delta_y, delta_x in override_sequence:
        if (delta_y + int(y) in range(map_size[0])) and (delta_x + int(x) in range(map_size[1])):
            override_list.append([y + delta_y, x + delta_x])
    for b, a in override_list:
        map_data[b][a] = "11"


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

if __name__ == '__main__':
    curses.wrapper(game)