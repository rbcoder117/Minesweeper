from drawable import drawable
import pygame as pg
pg.init()
WIDTH, HEIGHT = 640, 700
win = pg.display.set_mode(size=(WIDTH, HEIGHT))

sheet = pg.image.load("minesweeper-sprites.png")
timer_numbers = [pg.surface.Surface((13, 23)) for x in range(11)]

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

def BoardGen():
    Board = [[] for x in range(10)]
#www.scratch.mit.edu
smile = faces[0]
smile.rect.x = XOFFSET + 65
smile.rect.y = YOFFSET -30


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
        if e.type==pg.QUIT:
            play=False
    time = pg.time.get_ticks()// 1000
    translate_timer(time, timer_display)
    translate_flags(flags_display)
    draw(win, *([item for row in Main_grid for item in row]), *flags_display, smile, *timer_display)
#todo
'''
-if take more than 1000 seconds write imagine bieng slow examaple is in files as check todo
-board generation
-no bomb at start
-
-
-
-
-
-
'''