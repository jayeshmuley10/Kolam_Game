import pygame, sys, os
from pygame.locals import *

pygame.init()

total_width = 700
width = 600
height = 600
dot_gap = 50
mouse_pressed = 0
last_pressed = (0, 0)
lines = []
image_count = 0
max_image_count = 10
dot_selection_accuracy = 15
color_selected = (0, 0, 0)
color_box = 3
top = 1000
left = 1000
bottom = 0
right = 0
clrs = [(255, 255, 255), (168, 168, 168), (84, 84, 84), (0, 0, 0), (1, 127, 126), (1, 255, 255), (64, 31, 0),
        (128, 64, 0), (0, 73, 126), (0, 148, 254), (128, 0, 1), (254, 0, 0), (0, 18, 128),
        (0, 38, 255), (128, 52, 0), (254, 106, 0), (89, 0, 128), (177, 0, 254), (128, 107, 0), (255, 216, 0),
        (127, 0, 55), (255, 0, 110), (1, 127, 1), (0, 255, 1)]

GAMEWINDOW = pygame.display.set_mode((total_width, height), 0, 32)
pygame.display.set_caption("Practice Kolam Here...")

black = (0, 0, 0)
white = (255, 255, 255)


def terminate():
    pygame.quit()
    sys.exit()


def print_text(text, x, y, size, color):
    obj = pygame.font.Font('freesansbold.ttf', size)
    surf = obj.render(text, True, color)
    GAMEWINDOW.blit(surf, (x, y - 22))


def draw_line(a, b, c, d, size, color):
    global GAMEWINDOW
    pygame.draw.line(GAMEWINDOW, color, (a + 5, b + 3), (c + 5, d + 3), size)


def colors():
    global GAMEWINDOW, clrs
    c = 0
    pygame.draw.rect(GAMEWINDOW, (255, 255, 255), (580, 250, 100, 150))
    for i in range(250, 400, 25):
        for j in range(580, 680, 25):
            pygame.draw.rect(GAMEWINDOW, clrs[c], (j, i, 22, 22))
            if c == color_box:
                pygame.draw.rect(GAMEWINDOW, (52, 45, 145), (j - 1, i - 1, 24, 24), 2)
            c += 1


def capture(display, name, pos, size):
    image = pygame.Surface(size)
    image.blit(display, (0, 0), (pos, size))
    pygame.image.save(image, name)


def min_max(x, y):
    global left, right, top, bottom
    if x < left:
        left = x
    if x > right:
        right = x
    if y < top:
        top = y
    if y > bottom:
        bottom = y


def dots_nxn():
    x = 0
    y = 0

    while x < height:
        y = 0
        while y < width:
            print_text('.', x, y, 35, black)

            y += dot_gap
        x += dot_gap

    pygame.draw.rect(GAMEWINDOW, black, (600, 50, 90, 50), 2)
    print_text('UNDO', 610, 85, 25, black)
    pygame.draw.rect(GAMEWINDOW, black, (600, 150, 90, 50), 2)
    print_text('SAVE', 610, 185, 25, black)
    pygame.draw.rect(GAMEWINDOW, black, (600, 450, 90, 50), 2)
    print_text('Clear All', 605, 485, 18, black)
    pygame.draw.rect(GAMEWINDOW, black, (600, 510, 90, 65), 2)
    print_text('Create', 610, 545, 18, black)
    print_text('Tutorial', 610, 565, 18, black)
    colors()


def undo(x, y):
    global GAMEWINDOW
    if (x > 598 and x < 695 and y > 48 and y < 102):
        if (len(lines)):
            last = lines.pop()
            draw_line(last[0][0], last[0][1], last[1][0], last[1][1], 3, white)
            dots_nxn()


def save_image(x, y):
    global lines, image_count, max_image_count, left, right, top, bottom
    if image_count >= max_image_count:
        print('You have reached the maximum limit for saving images!!')
    elif (x > 598 and x < 695 and y > 148 and y < 202) and len(lines):
        if left < 30:
            left = 30
        if top < 30:
            top = 30
        capture(GAMEWINDOW, 'image' + str(image_count) + '.jpg', (left - 30, top - 30),
                (right - left + 60, bottom - top + 60))
        image_count += 1

    if image_count == max_image_count - 1:
        print('You can save only one more image. Please use your resources carefully!')


def get_color(x, y):
    global clrs, color_selected, color_box
    if x >= 580 and y >= 250 and y <= 400:
        x = ((x - 580) // 25)
        y = ((y - 250) // 25)
        color_selected = clrs[x + y * 4]
        color_box = x + y * 4
        colors()


def clear_board(x, y):
    global GAMEWINDOW, lines, left, right, top, bottom
    if x >= 595 and x <= 695 and y >= 450 and y <= 500:
        GAMEWINDOW.fill(white)
        dots_nxn()
        lines.clear()
        left = 1000
        right = 0
        top = 1000
        bottom = 0


def create_tutorial(x, y):
    global lines
    if x >= 595 and x <= 695 and y >= 510 and y <= 580:
        with open("Tutorial.py", "w") as f:
            f.write("l = " + str(lines) + '\n')
            f.write(
                'N = len(l)\nprev_N = -1\nprev_N2 = -1\nprev_N3 = -1\ns_x, s_y = l[0][0][0], l[0][0][1]\ncirc_x1, circ_y1 = -1, -1\ncirc_x2, circ_y2 = -1, -1\n\nimport pygame, sys, os\nfrom pygame.locals import*\n\npygame.init()\n\ntotal_width =700\nwidth  = 600\nheight = 600\ndot_gap = 50\nmouse_pressed = 0\nlast_pressed = (0, 0)\nlines = []\nimage_count = 0\nmax_image_count = 10\ndot_selection_accuracy = 15\ncolor_selected = (0,0,0)\ncolor_box = 3\ntop = 1000\nleft = 1000\nbottom = 0\nright = 0\nclrs = [(255,255,255), (168,168,168), (84,84,84), (0,0,0), (1,127,126), (1,255,255), (64,31,0), (128,64,0), (0,73,126), (0,148,254), (128,0,1), (254,0,0), (0,18,128),\n        (0,38,255), (128,52,0), (254,106,0), (89,0,128), (177,0,254), (128,107,0), (255,216,0), (127,0,55), (255,0,110), (1,127,1), (0,255,1)]\n\nGAMEWINDOW = pygame.display.set_mode((total_width, height), 0, 32)\npygame.display.set_caption("Practice Kolam Here...")\n\nblack=( 0, 0, 0)                                  \nwhite = (255, 255, 255)\nred = (255, 0, 0)\ngreen = (0, 255, 0)\n\ndef terminate():\n    pygame.quit()\n    sys.exit()\n    \n\ndef print_text(text, x, y, size, color):\n    obj=pygame.font.Font("freesansbold.ttf",size)\n    surf=obj.render(text,True,color)\n    GAMEWINDOW.blit(surf,(x, y-22))\n\ndef draw_line(a,b,c,d, size, color):\n    global GAMEWINDOW\n    pygame.draw.line(GAMEWINDOW, color, (a+5,b+3), (c+5,d+3), size)\n\ndef colors():\n    global GAMEWINDOW, clrs\n    c = 0\n    pygame.draw.rect(GAMEWINDOW, (255,255,255),(580,250,100,150))\n    for i in range(250, 400, 25):\n        for j in range(580, 680, 25):\n            pygame.draw.rect(GAMEWINDOW, clrs[c],(j,i,22,22))\n            if c == color_box:\n                pygame.draw.rect(GAMEWINDOW, (52, 45, 145),(j-1,i-1,24,24),2)\n            c+=1\n\ndef capture(display,name,pos,size): \n    image = pygame.Surface(size)  \n    image.blit(display,(0,0),(pos,size))  \n    pygame.image.save(image,name)  \n\ndef min_max(x, y):\n    global left, right, top ,bottom\n    if x < left:\n        left = x\n    if x > right:\n        right = x\n    if y < top:\n        top = y\n    if y > bottom:\n        bottom = y\n\ndef dots_nxn():\n    x = 0\n    y = 0\n    \n    while x < height:\n        y = 0\n        while y < width:\n            print_text(".", x, y, 35, black)\n            \n            y+=dot_gap\n        x+=dot_gap\n\n    pygame.draw.rect(GAMEWINDOW, black, (600, 50, 90, 50), 2)\n    print_text("UNDO", 610, 85, 25, black)\n    pygame.draw.rect(GAMEWINDOW, black, (600, 150, 90, 50), 2)\n    print_text("SAVE", 610, 185, 25, black)\n    colors()\n    \ndef undo(x, y):\n    global GAMEWINDOW, l, circ_x1, circ_y1, circ_x2, circ_y2\n    if(x > 598 and x < 695 and y > 48  and y < 102):\n        if(len(lines)):\n            last = lines.pop()\n            draw_line(last[0][0], last[0][1], last[1][0], last[1][1], 3, white)\n            dots_nxn()\n            l.insert(0, last)\n            if len(l)-1:\n                circ_x1, circ_y1 = l[1][0][0], l[1][0][1]\n                circ_x2, circ_y2 = l[1][1][0], l[1][1][1]\n\ndef save_image(x, y):\n    global lines, image_count, max_image_count, left, right, top ,bottom\n    if image_count >=max_image_count:\n        print("You have reached the maximum limit for saving images!!")\n    elif(x > 598 and x < 695 and y > 148  and y < 202) and len(lines):\n        if left < 30:\n            left = 30\n        if top < 30:\n            top = 30\n        capture(GAMEWINDOW, "image" + str(image_count) + ".jpg", (left-30, top-30), (right-left+60, bottom-top+60))\n        image_count += 1\n\n    if image_count == max_image_count-1:\n        print("You can save only one more image. Please use your resources carefully!")\n\ndef get_color(x, y):\n    global clrs, color_selected, color_box\n    if x >=580 and y >= 250 and y <= 400:\n        x = ((x-580)//25)\n        y = ((y-250)//25)\n        color_selected = clrs[x + y*4]\n        color_box = x+y*4\n        colors()\n\ndef clear_board(x, y):\n    global GAMEWINDOW, lines, left, right, top ,bottom\n    if x >=595 and x <=695  and y >= 450 and y <= 500:  \n        GAMEWINDOW.fill(white)\n        dots_nxn()\n        lines.clear()\n        left = 1000\n        right = 0\n        top = 1000\n        bottom = 0\n\ndef start():\n    global N, l, prev_N3\n    if len(l) == N:\n        x, y = l[0][0][0], l[0][0][1]\n        print_text("START HERE!", x-40, y-12, 20, red)\n        pygame.draw.circle(GAMEWINDOW, red, (x+4, y+3), 10, 1)\n    else:\n        if len(l)!=prev_N3:\n            pygame.draw.rect(GAMEWINDOW, white, [s_x-40, s_y-34, 150, 22])\n            draw_lines()\n        prev_N3 = len(l)\n        \ndef next_point():\n    global l, circ_x1, circ_y1, circ_x2, circ_y2, prev_N2\n    if len(l)!=prev_N2:\n        if len(l):\n            if circ_x2 != -1:\n                pygame.draw.circle(GAMEWINDOW, white, (circ_x1+4, circ_y1+3), 10, 1)\n                pygame.draw.circle(GAMEWINDOW, white, (circ_x2+4, circ_y2+3), 10, 1)\n                draw_lines()\n                \n            a, b = l[0][0][0], l[0][0][1]\n            x, y = l[0][1][0], l[0][1][1]\n            pygame.draw.circle(GAMEWINDOW, green, (a+4, b+3), 10, 1)\n            pygame.draw.circle(GAMEWINDOW, green, (x+4, y+3), 10, 1)\n            pygame.draw.rect(GAMEWINDOW, white, (580, 450, 120, 52))    # not completed white box\n            \n\n        else:\n            print("You have completed successfully!!!")\n            pygame.draw.rect(GAMEWINDOW, black, (580, 450, 118, 50), 2)\n            print_text("Completed!!!", 585, 485, 18, red)\n    prev_N2 = len(l)\n\ndef draw_lines():\n    global l, prev_N, color_selected, lines\n    if len(l)!= prev_N:\n        for line in lines:\n            draw_line(line[0][0], line[0][1], line[1][0], line[1][1], 3, color_selected)\n    prev_N = len(l)\n\ndef erase_last():\n    global l, lines, prev_N\n    x1, y1 = l[0][0][0], l[0][0][1]\n    x2, y2 = l[0][1][0], l[0][1][1]\n    pygame.draw.circle(GAMEWINDOW, white, (x1+4, y1+3), 10, 1)\n    pygame.draw.circle(GAMEWINDOW, white, (x2+4, y2+3), 10, 1)\n    prev_N = -1\n    draw_lines()    \n    \ndef mouse():\n    global mouse_pressed, last_pressed, lines, color_selected, l, circ_x1, circ_y1, circ_x2, circ_y2\n    \n    event = pygame.event.wait()\n    if event.type == pygame.QUIT:\n        terminate()\n    \n    xpos,ypos = pygame.mouse.get_pos()\n\n    near_x = int(xpos/50) * 50\n    near_y = int(ypos/50) * 50\n\n    \n    if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:\n        mouse_pressed = 1\n        if abs(near_x - xpos) < dot_selection_accuracy and abs(near_y - ypos) < dot_selection_accuracy and near_x < width:\n            last_pressed = (near_x, near_y)\n        undo(xpos, ypos)\n        save_image(xpos, ypos)\n        get_color(xpos, ypos)\n\n    elif event.type == pygame.MOUSEBUTTONUP and event.button ==1:\n        mouse_pressed = 0\n\n    \n    if mouse_pressed and abs(near_x - xpos) < dot_selection_accuracy and abs(near_y - ypos) < dot_selection_accuracy and near_x < width:\n        if(last_pressed != (near_x, near_y)):\n                if len(l) and [last_pressed, (near_x, near_y)] == l[0]:\n                    min_max(last_pressed[0], last_pressed[1])\n                    min_max(near_x, near_y)\n                    draw_line(last_pressed[0],last_pressed[1], near_x,near_y, 3, color_selected)\n                    lines.append([last_pressed, (near_x, near_y)])\n                    last_pressed = (near_x, near_y)\n                    circ_x1, circ_y1 = l[0][0][0], l[0][0][1]\n                    circ_x2, circ_y2 = l[0][1][0], l[0][1][1]\n                    if len(l) == 1:\n                        erase_last()\n                    l.pop(0)\n                else:\n                    print("Do correctly!")\n            \n            \n\ndef manage_screen():\n    start()\n    mouse()\n    next_point()\n    \ngame = 1\nGAMEWINDOW.fill(white)\ndots_nxn()\nwhile game:\n    manage_screen()\n    pygame.display.update()\n')


def mouse():
    global mouse_pressed, last_pressed, lines, color_selected

    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        terminate()

    xpos, ypos = pygame.mouse.get_pos()

    near_x = int(xpos / 50) * 50
    near_y = int(ypos / 50) * 50

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pressed = 1
        if abs(near_x - xpos) < dot_selection_accuracy and abs(
                near_y - ypos) < dot_selection_accuracy and near_x < width:
            last_pressed = (near_x, near_y)
        undo(xpos, ypos)
        save_image(xpos, ypos)
        get_color(xpos, ypos)
        clear_board(xpos, ypos)
        create_tutorial(xpos, ypos)
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        mouse_pressed = 0

    if mouse_pressed and abs(near_x - xpos) < dot_selection_accuracy and abs(
            near_y - ypos) < dot_selection_accuracy and near_x < width:
        if (last_pressed != (near_x, near_y)):
            draw_line(last_pressed[0], last_pressed[1], near_x, near_y, 3, color_selected)
            min_max(last_pressed[0], last_pressed[1])
            min_max(near_x, near_y)
            lines.append([last_pressed, (near_x, near_y)])
            last_pressed = (near_x, near_y)


def manage_screen():
    mouse()


game = 1
GAMEWINDOW.fill(white)
dots_nxn()
while game:
    manage_screen()
    pygame.display.update()