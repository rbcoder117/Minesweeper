from drawable import drawable
import pygame as pg
import random as rand
pg.init()
WIDTH, HEIGHT = 640, 700
win = pg.display.set_mode(size=(WIDTH, HEIGHT))

sheet = pg.image.load("minesweeper-sprites.png")
timer_numbers = [pg.surface.Surface((13, 23)) for x in range(11)]
first = True
for x in range(11):
    timer_numbers[x].blit(sheet, sheet.get_rect(x=-x * 14))
    timer_numbers[x] = drawable(timer_numbers[x], timer_numbers[x].get_rect(y=x * 24))
#/////////////////////////////////////////////////////////////////
faces = [pg.surface.Surface((26, 26)) for x in range(5)]

for x in range(5):
    faces[x].blit(sheet, sheet.get_rect(x=-x*27, y=-24))
    faces[x] = drawable(faces[x], faces[x].get_rect(x=14, y=x*24))
#/////////////////////////////////////////////////////////////////
symbols = [pg.surface.Surface((16, 16)) for x in range(8)]
for x in range(8):
    symbols[x].blit(sheet, sheet.get_rect(x=-x*17, y=-51))
    symbols[x] = drawable(symbols[x], symbols[x].get_rect(x=41, y=x*17))
#//////////////////////////////////////////////////////////////////
numbers = [pg.surface.Surface((16, 16)) for x in range(8)]
for x in range(8):
    numbers[x].blit(sheet, sheet.get_rect(x=-x*17, y=-68))
    numbers[x] = drawable(numbers[x], numbers[x].get_rect(x=58, y=x*17))

def draw(win, *objs):
    for obj in objs:
        win.blit(obj.surface, obj.rect)
    pg.display.update()
Main_grid = [[symbols[0].copy() for y in range(10)] for x in range(10)]
XOFFSET, YOFFSET = WIDTH/2-80, HEIGHT/2-110
I=0
for row in Main_grid:
    J=0
    for spot in row:
        spot.rect.x, spot.rect.y = J*(spot.rect.width+2) + XOFFSET, I*(spot.rect.height+2) + YOFFSET
        J+=1
    I+=1
timer_display = [timer_numbers[0].copy(), timer_numbers[5].copy(), timer_numbers[7].copy()]
flags_display = [timer_numbers[0].copy(), timer_numbers[1].copy(), timer_numbers[0].copy()]
times_ran = 0
for d in flags_display:
    d.rect.x=XOFFSET + times_ran * (d.rect.width+1)
    d.rect.y=YOFFSET -30
    times_ran+=1
times_ran = 2
for d in timer_display:
    d.rect.x=XOFFSET + times_ran * (-d.rect.width+1) + 160
    d.rect.y=YOFFSET -30
    times_ran-=1

flags_left = 10
def translate_timer(time, time_display):#1000 miliseconds = 1 second

    translate(time, time_display)

def translate(num, display):
    if num > 999:
        num= num% 1000
    first_pos = num//100 if num>=0 else -1
    num = abs(num) % 100
    second_pos= num//10
    thrid_pos = num% 10
    spot = (display[0].rect.x, timer_display[0].rect.y)
    display[0]=timer_numbers[first_pos].copy()
    display[0].rect.topleft=spot
    spot = (display[1].rect.x, timer_display[1].rect.y)
    display[1]=timer_numbers[second_pos].copy()
    display[1].rect.topleft = spot
    spot = (display[2].rect.x, timer_display[2].rect.y)
    display[2]=timer_numbers[thrid_pos].copy()
    display[2].rect.topleft = spot
def find_tile(pos):
    #Go throu entire grid and find which tile to return
    for row in Main_grid:
        for box in row:

            if box.rect.collidepoint(pos):
                return box
    return None
def translate_flags(flags_display):
    # Edit flags_display's pictures based on flags_left e.g. flags_left == 21, set f_d[0] = timer_numbers[0], f_d[1] = t_n[2], f_d[2] = t_n[1]
    flags_left=10
    for row in Main_grid:
        for box in row:
            if box.flag:
                flags_left -= 1
    translate(flags_left, flags_display)
first = True
def BoardGen():
    Board = [[0 for i in range(10)] for x in range(10)]
    for b in range(10):
        row = rand.randint(0, 9)
        col = rand.randint(0, 9)
        Board[row][col] = 1
    #bombs have been generated
    row = 0
    col = 0
    for row in range(10):
        for col in range(10):
            Main_grid[row][col].clicked = False
            if Board[row][col] == 1:
                Main_grid[row][col].bomb = True
            else:
                Main_grid[row][col].bomb = False

#www.scratch.mit.edu
smile = faces[0]
smile.rect.x = XOFFSET + 65
smile.rect.y = YOFFSET -30


def temp(pos):
    tile = find_tile(pos)
    if tile != None and not tile.bomb:
        bombcount = 0
        tn = [[-16, 0], [0, -16], [16, 0], [0, 16], [-16, 16], [-16, -16], [16, -16], [16, 16]]
        for mods in tn:
            npos = (pos[0] + mods[0], pos[1] + mods[1])
            neighbor = find_tile(npos)
            if neighbor != None:
                bombcount += 1 if neighbor.bomb else 0
        print(bombcount)
        if bombcount == 0:
            tile.surface = symbols[1].surface.copy()
        else:
            tile.surface = numbers[bombcount - 1].surface.copy()
play=True
while play:
    for e in pg.event.get():
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button==3:
                tile = find_tile(e.pos)
                if tile is not None:
                    if not tile.flag:
                        tile.surface = symbols[2].surface.copy()
                        tile.flag = True
                    elif tile.flag:
                        tile.surface = symbols[0].surface.copy()
                        tile.flag = False
            elif e.button==1:
                tile = find_tile(e.pos)
                if first:
                    BoardGen()
                    first = False
                if tile !=None and tile.bomb and tile.clicked == False:
                    print("U are winning")  #i have no freinds and no life
                    tile.surface = symbols[5].surface.copy()
                    tile.clicked = True
                elif tile !=None and not tile.bomb:
                    bombcount = 0
                    tn = [[-16, 0], [0, -16], [16, 0], [0, 16], [-16, 16], [-16, -16], [16, -16], [16,16]]
                    for mods in tn:
                        npos = (e.pos[0]+mods[0], e.pos[1]+mods[1])
                        neighbor = find_tile(npos)
                        if neighbor != None:
                            bombcount +=1 if neighbor.bomb else 0
                    print(bombcount)
                    if bombcount == 0:
                        tile.surface = symbols[1].surface.copy()
                        for f in tn:
                            temp((e.pos[0]+f[0], e.pos[1]+f[1]))
                    else:
                        tile.surface = numbers[bombcount-1].surface.copy()

        if e.type==pg.QUIT:
            play=False
    time = pg.time.get_ticks()// 1000
    translate_timer(time, timer_display)
    translate_flags(flags_display)
    draw(win, *([item for row in Main_grid for item in row]), *flags_display, smile, *timer_display)


#todo
'''
-if take more than 1000 seconds write imagine bieng slow examaple is in files as check todo
-board generation ✅
-use find_tile(e.pos) to find tile you clicked, and edit e.pos to find tiles adjacent (nearby) it
-
-
-
-
-
-
-
-
-
'''