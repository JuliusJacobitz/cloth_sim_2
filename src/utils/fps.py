import pygame


def render(screen, fnt, what, color, where):
    "Renders the fonts as passed from display_fps"
    text_to_show = fnt.render(what, 0, pygame.Color(color))
    screen.blit(text_to_show, where)


def display_fps(fonts, clock, screen):
    "Data that will be rendered and blitted in _display"
    render(
        screen,
        fonts[2],
        what="FPS: " + str(int(clock.get_fps())),
        color="red",
        where=(0, 0),
    )
