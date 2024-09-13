import pygame
from pygame import *

from .GIF_Sprites import GIFSprites
from .List_Sprites import ListSprites
from .Show import Show
from .Sprite import Sprites
from .Text_Input import TextInput


class Pgs:
    @staticmethod
    def init():
        Show.screen = display.get_surface()
        if not Show.screen: Show.screen = pygame.Surface((480, 270))
