import lib
import pygame
from pygame import *

from .GIF_Sprites import GIFSprites
from .List_Sprites import ListSprites
from .Show import Show, Surface
from .Sprite import Sprites
from .TextInput import TextInput

screen: Surface = Surface((480, 270))


def init():
    """ initializes all the nessecary functions """
    global screen
    Show.screen, screen = 2 * [display.get_surface()]


# noinspection PyTypeChecker
pygame.Pgs = lib
