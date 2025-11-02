import os,curses,ast
if __name__=='__main__':
    os.chdir(os.getcwd().strip('//library'))
    from connectivity import *
else:
    from library.connectivity import *

def highscore_browser(win,max_entries=7,enableconnectivity=True):
    page = 0
    sboard_entries_full=list()
    for file in os.listdir():
        if file.endswith(".scoreboard"):
            with open(file,'r',encoding="utf-8") as scoreboard:
                sboard_entries_full.extend(
                    ast.literal_eval('['+''.join(scoreboard.readlines())+']')
                    )
    if enableconnectivity: # cloud highscores
        try:
            cloud_entries=read_scoreboard_as_string()
            cloud_list = ast.literal_eval('['+cloud_entries+']')
            for item in cloud_list:
                if item not in sboard_entries_full:
                    sboard_entries_full.append(item)
        except: pass
    if len(sboard_entries_full)!=0: #sort by date
        sboard_entries_full.sort(key=lambda i:i[2],reverse=True)
    highscores=list()
    for mode in ('classic','standard','hardcore','fast'):
        mode_specific_entries = list(i for i in sboard_entries_full if i[0] == mode)
        try:
            highscore=sorted(mode_specific_entries,key=lambda i:i[4],reverse=True)[0]
        except IndexError: highscore = (mode,'N/A','N/A',0,0)
        highscores.append(highscore)
    for item in highscores: #rm duplicates
        if item in sboard_entries_full:
            del sboard_entries_full[sboard_entries_full.index(item)]
    win.erase()
    curses.curs_set(0)
    win.nodelay(False)  
    win.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    while True:
        win.erase()
        __title_element__ = "Highscores" 
        win.addstr(1, 0, f" {' '+__title_element__+' ':─^67} ")
        __title_element__ = "  - ─ ───── Highscores ───── ─ -  " 
        win.addstr(1,17,__title_element__,curses.color_pair(2))
        __title_element__ = "History" 
        win.addstr(6, 0, f" {' '+__title_element__+' ':─^67} ")
        sboard_entries_truncated = sboard_entries_full[max_entries*page:max_entries*(page+1)]
        win.addstr(0,0,r""" Project OLED" Beta                                     A11 Software""")

        for line,entry in list(enumerate(highscores))+list(enumerate(sboard_entries_truncated,start=5)):
            mode_truncated = '['+entry[0][0].upper()+']' #mode
            name_truncated = f'{entry[1][:10]:<10}' #name
            score_truncated = f"{str(entry[4])[:8]:<8}"
            interval_truncated = f"{str(int(entry[3])//10)[:6]+'s':<7}"
            time_truncated=f"{entry[2][:-3]:<17}"
            if int(entry[4]) in range(0,-501,-1):
                score_color = curses.color_pair(1) #Green
                rating = 'PERFECT'
            elif int(entry[4]) in range(-501,-1001,-1):
                score_color = curses.color_pair(2) #Yellow
                rating = 'GOOD'
            else:
                score_color = curses.color_pair(3) #Red
                rating = 'SUBOPTIMAL'
            win.addstr(2+line,0,f' {mode_truncated} {name_truncated}│         │ {rating[:12]:<12}│ {interval_truncated}│ {time_truncated}│')
            win.addstr(2+line,17,str(score_truncated),score_color)

        win.addstr(15,1,'─'*67)
        if len(sboard_entries_full[:max_entries*(page)]) != 0: 
            win.addstr(14,1,"[a] Last page")
        if len(sboard_entries_full[max_entries*(page+1):]) != 0: 
            win.addstr(14,55,'[d] Next page')
        win.addstr(16,1,'[x] Previous menu')
        key = win.getkey()     
        if key in ('x','KEY_BACKSPACE','\b','\x7f'):
            win.nodelay(True)
            return 0
        elif key in ('a','KEY_LEFT'): 
            if len(sboard_entries_full[:max_entries*(page)]) != 0: page-=1
        elif key in ('d','KEY_RIGHT'): 
            if len(sboard_entries_full[max_entries*(page+1):]) != 0: page+=1
        win.noutrefresh()
        curses.doupdate()  # <- show changes



if __name__=='__main__':
    curses.wrapper(highscore_browser)