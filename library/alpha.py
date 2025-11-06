"""
The game goes through 10 ticks per second
"""
import time
import curses
import random
import os

if __name__=='__main__':
    os.chdir(os.getcwd().strip('//library'))



def alpha(win):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    win.nodelay(True)      # set once, not every loop
    win.keypad(True)
    selector=[0,0]
    tick = 0


#initialize_game_map
    map_size=(10,10)      # create the map
    selector=[int(map_size[0]/2),int(map_size[1]/2)]
    map_data_list = []
    map_data_list_temp=[]
    for _ in range(map_size[0]):
        map_data_list_temp+=['0']
    for _ in range(map_size[1]):
        map_data_list.append(map_data_list_temp[:])
    for _ in range(random.randint(5,35)):
        flip_alpha(random.randint(0,9),random.randint(0,9),map_data_list)
    #print(map_data_list)
#main loop 
    tick=0
    while True:
        tick += 1
        #win.erase()        # clear FIRST



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
            handle_movement_alpha(key, selector, map_data_list)
        except IndexError:key="noinput"
        
        MAX_QUEUE = 128 # Safety
        if len(key_queued) > MAX_QUEUE:
            del key_queued[:-MAX_QUEUE]


        if tick%20==0:  # screen erases every 2s
            win.erase()  

        if key == 'k' or sum(tile == '1' for line in map_data_list for tile in line) == 0:
            return 0
        try:   
            win.addstr(0, 0, f'Tick: {tick}'+'\n')
            win.addstr(1, 0, f'Key: {key:<10}')
            win.addstr(2, 0, f'Pos: {selector}')
            for y in range(len(map_data_list)):
                text=str(map_data_list[y])
                text=text.replace("""'""",' ').replace(',',' ')
                for x,chr in enumerate(text):
                    if chr not in '10' and chr != ' ':    
                        win.addstr(3+y, 0+x, chr)
                    elif chr=='0':
                        win.addstr(3+y, 0+x-1, ' '+chr+' ')
                    elif chr=='1':
                        win.addstr(3+y, 0+x-1, ' '+chr+' ',curses.A_REVERSE)
            tile_sel = str(map_data_list[selector[1]][selector[0]])
            if tile_sel!='1':
                win.addstr(3+selector[1],2+5*selector[0],tile_sel,curses.color_pair(1))
            else:
                win.addstr(3+selector[1],2+5*selector[0]-1,' '+tile_sel+' ',curses.color_pair(1)|curses.A_REVERSE)

            win.addstr(4+len(map_data_list),0,f'{r"Press {k} to exit":^50}')
        except:
            return 0
        win.refresh()      # <- show changes
        time.sleep(0.1)
      


def flip_alpha(x,y,map_data_list):
    map_size=(10,10)
    flip_list=[]
    flip_sequence=((-1,0),(1,0),(0,0),(0,-1),(0,1))
    for sq_x,sq_y in flip_sequence:
        if (sq_x+int(x) in range(map_size[0]))and(sq_y+int(y) in range(map_size[1])):
            flip_list.append([x+sq_x,y+sq_y])
    for a,b in flip_list:
         if str(map_data_list[a][b])[0]=='1':
             map_data_list[a][b]='0'
         else:
             map_data_list[a][b]='1'


def handle_movement_alpha(key,selector,map_data_list):
     if key=='w':
         selector[1]=max(0,selector[1]-1)
     if key=='s':
         selector[1]=min(9,selector[1]+1)
     if key=='d':
         selector[0]=min(9,selector[0]+1)
     if key=='a':
         selector[0]=max(0,selector[0]-1)
     if key=='b':            #flip
         flip_alpha(selector[1],selector[0],map_data_list)

            

if __name__=='__main__':
    curses.wrapper(alpha)



