import pygame
import sys

light_gray = (211, 211, 211)
gray = (150, 150, 150)
white = (255, 255, 255)
black = (0, 0, 0,)

border_pl = (0, 128, 0)
player = (50, 205, 50)
background = (113, 204, 0)

sym_to_color = {"0": "",
                "1": "brown",
                "P": "pink",
                "B": "blue",
                "R": "red",
                "E": "black"}

color_dict = {
    "red": [(255, 0, 0), (76, 0, 19)],
    "green": [(0, 255, 0), (0, 178, 0)],
    "blue": [(0, 0, 255), (0, 0, 178)],
    "yellow": [(255, 255, 0), (178, 178, 0)],
    "pink": [(255, 105, 180), (255, 182, 193)],
    "brown": [(160, 82, 45), (222, 184, 135)],
    "black": [(0, 0, 0), (0, 0, 0)]
}

screen = None
SIDE = 50
BORDER = 6
MARGIN = 5
LINE = 2


def __draw_tile(x, y, sym):
    global screen
    color = sym_to_color[sym]
    if color == "":
        return

    center_color, border_color = color_dict[color]

    pygame.draw.rect(screen, border_color, pygame.Rect(MARGIN + y * SIDE, MARGIN + x * SIDE, SIDE, SIDE))
    pygame.draw.rect(screen, center_color, pygame.Rect(MARGIN + y * SIDE + LINE, MARGIN + x * SIDE + LINE,
                                                     SIDE - 2 * LINE, SIDE - 2 * LINE))


def __draw_entity(e, sym):
    global screen
    color = sym_to_color[sym]
    if color == "":
        return

    x, y = e['position']
    center_color, border_color = color_dict[color]
    if "direction" not in e:
        pygame.draw.circle(screen, center_color, [MARGIN + y * SIDE + SIDE//2, MARGIN + x * SIDE + SIDE//2], SIDE//2)
    else:
        dir = e['direction']
        point_list = [(0, 0),
                      (SIDE, 0),
                      (SIDE//2, SIDE)]

        ent = pygame.Surface([SIDE, SIDE], pygame.SRCALPHA, 32)
        pygame.draw.polygon(ent, center_color, point_list)
        screen.blit(pygame.transform.rotate(ent, -90*dir), pygame.Rect(MARGIN + y * SIDE, MARGIN + x * SIDE, SIDE, SIDE))


def reset_screen():
    global screen
    screen = None


def render(obs, entities):
    k, h = obs.shape

    global screen
    if screen is None:
        pygame.init()
        screen = pygame.display.set_mode((2 * MARGIN + h * SIDE, 2 * MARGIN + k * SIDE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)

    screen.fill(background)

    # first we draw the background
    for x in range(0, k):
        for y in range(0, h):
            # Draw the background with the grid pattern
            if obs[x, y] == '1' or obs[x, y] == 'E':
                __draw_tile(x, y, obs[x, y])

    for e in entities:
        x, y = e['position']
        __draw_entity(e, obs[x, y])

    pygame.display.update()


def get_action():
    action = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action = 2
            elif event.key == pygame.K_RIGHT:
                action = 3
            elif event.key == pygame.K_UP:
                action = 0
            elif event.key == pygame.K_DOWN:
                action = 1

    return action
