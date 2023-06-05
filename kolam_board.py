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