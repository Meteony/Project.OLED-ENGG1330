import time,os,random

def print_clear(): #<--------------------------Universal screen cleariing anywhere(Print() only)
    if os.name == 'nt':
        a=os.system('cls')
    else:
        os.system('clear')


def gameover_cutscene(skip=False,end_score=0,end_ticks=0):
    if not skip:
        print_clear()           #Print anis below


        time.sleep(4)
        print('The operating system was not shut down properly.',end='',flush=True)
        time.sleep(3)
        print('\nLast system uptime: ',end='',flush=True)
        time.sleep(0.5)
        indi = ["|", "/", "-", "\\"]
        for _ in range(3):
            for i in range(4):
                print(f'\rLast system uptime: {indi[i]}',end='',flush=True)
                time.sleep(0.2)
        print('\rLast system uptime:  ',end='',flush=True)
        time.sleep(0.5)
        print('\rLast system uptime: \x1b[91m'+f'{end_ticks}'+'\x1b[0m',end='',flush=True)
        #clear()
        #print('The operating system did not shut down cleanly.\nLast system uptime: ''1392')
        time.sleep(3)


        print('\nGPT header CRC mismatch. ',end='',flush=True)
        time.sleep(2)
        print('Backup LBA points to sector: ',end='',flush=True)


        for _ in range(3):
            for i in range(4):
                print(f'\rGPT header CRC mismatch. Backup LBA points to sector {indi[i]}',end='',flush=True)
                time.sleep(0.2)
        print(f'\rGPT header CRC mismatch. Backup LBA points to sector ',end='',flush=True)
        time.sleep(0.5)
        print('\x1b[91m-'+f'\x1b[0m0x\x1b[91m{str(end_score)[1:]}\x1b[0m...',end='',flush=True)


                
        time.sleep(4)
        print('\n\nAttempting system reboot ',end='',flush=True)
        time.sleep(0.5)
        for _ in range(3):
            for i in range(4):
                print(f'\rAttempting system reboot {indi[i]}',end='',flush=True)
                time.sleep(0.2)

        time.sleep(1.5)
        print(f'\n\nACPI: FADT rev 6 @ 0x000000007FEEA000; DSDT @ 0x000000007FEDC000 (crc=0x{hex(random.randint(114,5141))})',end='',flush=True)
        time.sleep(1)
        print(f'\nACPI: FADT rev 6 @ 0x000000007FEEA000; DSDT @ 0x000000007FEDC000 (crc=0x{hex(random.randint(114,5141))})',end='',flush=True)
        time.sleep(0.4)
        for _ in range(3):
            print(f'\nACPI: FADT rev 6 @ 0x000000007FEEA000; DSDT @ 0x000000007FEDC000 (crc=0x{hex(random.randint(114,5141))})',end='',flush=True)
            time.sleep(0.15)
        for _ in range(7):
            print(f'\nACPI: FADT rev 6 @ 0x000000007FEEA000; DSDT @ 0x000000007FEDC000 (crc=0x{hex(random.randint(114,5141))})',end='',flush=True)
            time.sleep(0.05)
        for _ in range(200):
            print(f'\nACPI: FADT rev 6 @ 0x000000007FEEA000; DSDT @ 0x000000007FEDC000 (crc=0x{hex(random.randint(114,5141))})',end='',flush=True)
            time.sleep(0.01)
        print_clear()
        time.sleep(3)
        print('System halted. Press <ENTER> to enter Recovery.')
        input()
        print_clear()
        time.sleep(2)

if __name__=='__main__':
    gameover_cutscene()