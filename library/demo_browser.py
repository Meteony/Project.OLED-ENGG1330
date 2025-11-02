import os,curses,ast

if __name__=='__main__':
    os.chdir(os.getcwd().strip('//library'))
    current_dir = os.getcwd()
    demo_dir = current_dir+"//Saved Demos//"




def demo_browser(win,max_entries=12,demo_directory=os.getcwd()):
    page = 0
    demo_dir = demo_directory
    demo_dict=dict()
    for file in os.listdir(demo_dir):
        if file.endswith(".oled"):
            with open(demo_dir+file,'r',encoding="utf-8") as demo:
                next(demo)
                demo_dict[file]=(list((line,line[:-1])[line.endswith('\n')] for line in demo.readlines()))
    demo_list_full = list(demo_dict.keys())
    win.erase()
    curses.curs_set(0)
    win.nodelay(False)  
    win.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    cursor_position = 0
    while True:
        win.erase()
        win.addstr(0,0,r""" Project OLED" Beta                                     A11 Software""")
        __title_element__ = "Demo Browser" 
        win.addstr(1, 0, f" {' '+__title_element__+' ':─^67} ")
        demo_list_truncated = demo_list_full[max_entries*page:max_entries*(page+1)]
        cursor_position = max(0,min(cursor_position,len(demo_list_truncated)-1))

        for index,name in enumerate(demo_list_truncated):
            manifest = demo_dict[name]
            file_name_truncated = f"{name[:14]:<14}"
            game_mode_initial = f"{manifest[0][0].upper()}"
            player_name_truncated = f'{manifest[1][:9]:<9}'
            time_truncated = f"{manifest[2][:-3]:<17}"
            score_plus_interval = ast.literal_eval(manifest[3])
            score = int(score_plus_interval[0])
            interval_truncated = f"{str(int(score_plus_interval[1])//10)[:5]+'s':<5}"
            content = f' □ {file_name_truncated}│ {game_mode_initial} │ {player_name_truncated}│ {time_truncated}│        │ {interval_truncated}│'
            win.addstr(2+index,0,content)
            if int(score_plus_interval[0]) in range(0,-501,-1):
                score_color = curses.color_pair(1) #Green
            elif int(score_plus_interval[0]) in range(-501,-1001,-1):
                score_color = curses.color_pair(2) #Yellow
            else:
                score_color = curses.color_pair(3) #Red
            win.addstr(2+index,53,str(score),score_color)
            if cursor_position == index:
                win.addstr(2+index,1,'■',curses.color_pair(1))
        win.addstr(15,1,'─'*67)
        win.addstr(16,1,f"{'[w]/[s] Up/Down':^67}")
        if len(demo_list_full[:max_entries*(page)]) != 0: 
            win.addstr(14,1,"[a] Last page")
        if len(demo_list_full[max_entries*(page+1):]) != 0: 
            win.addstr(14,55,'[d] Next page')
        win.addstr(16,1,'[x] Previous menu')
        select_helper='[c]/[⏎] Select'
        win.addstr(16,68-len(select_helper),select_helper)
        key = win.getkey()     
        if key in ('x','KEY_BACKSPACE','\b','\x7f'):
            win.nodelay(True)
            return 0
        elif key in ('a','KEY_LEFT'): 
            if len(demo_list_full[:max_entries*(page)]) != 0: page-=1
        elif key in ('d','KEY_RIGHT'): 
            if len(demo_list_full[max_entries*(page+1):]) != 0: page+=1
        elif key in ('w','KEY_UP'):
            cursor_position = max(0,min(cursor_position-1,len(demo_list_truncated)-1))
        elif key in ('s','KEY_DOWN'):
            cursor_position = max(0,min(cursor_position+1,len(demo_list_truncated)-1))

        elif key in ('b','c','\n','\r','KEY_ENTER'):
            return demo_list_truncated[cursor_position]
        win.noutrefresh()
        curses.doupdate()  # <- show changes

if __name__=='__main__':
    def pseudomain(win):
        return demo_browser(win=win,demo_directory=demo_dir)
    print(curses.wrapper(pseudomain))