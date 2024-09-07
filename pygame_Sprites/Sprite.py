from typing import Callable, Any

from pygame import image, transform, mask, mouse

from .Show import Show, Surface


class Sprites:
    mouse_sprite: mask.Mask = mask.Mask((1, 1))

    def __init__(self, filename: str | Surface, size: tuple[float | int, ...], pos: tuple[int | float, ...]) -> None:
        sprite_surface: Surface = mask.Mask((1, 1)).to_surface()
        if isinstance(filename, str):
            self.img_path, sprite_surface = [filename, image.load(filename)]
        sprite_surface = transform.scale(sprite_surface, size)
        self.size, self.x, self.y, self.surface = [list(size), pos[0], pos[1], sprite_surface]
        self.side_set: dict = {"top": {"_mask": mask.Mask((self.size[0] / 2, 1)),
                                       "_pos": [self.x, self.y - self.size[1] / 2]},
                               "right": {"_mask": mask.Mask((1, self.size[1] / 2)),
                                         "_pos": [self.x + self.size[0] / 2, self.y]},
                               "bottom": {"_mask": mask.Mask((self.size[0] / 2, 1)),
                                          "_pos": [self.x, self.y + self.size[1] / 2]},
                               "left": {"_mask": mask.Mask((1, self.size[1] / 2)),
                                        "_pos": [self.x - self.size[0] / 2, self.y]},
                               "center": {"_mask": mask.Mask((self.size[0] / 2, self.size[1] / 2)),
                                          "_pos": [self.x, self.y]},
                               "left to right": {"_mask": mask.Mask((self.size[0], self.size[1] / 2)),
                                                 "_pos": [self.x, self.y]},
                               "top to bottom": {"_mask": mask.Mask((self.size[0] / 2, self.size[1])),
                                                 "_pos": [self.x, self.y]}
                               }

    def show(self, pos: tuple[int, ...] = (None, None), size: tuple[float | int, ...] = (),
             flip: tuple[bool, ...] = (False, False), tf: bool = True, part: tuple[int, ...] = ()) -> None:
        x, y = pos
        if not x: x = self.x - self.size[0] / 2
        if not y: y = self.y - self.size[1] / 2
        if not size: size = tuple(self.size)
        img = transform.scale(transform.flip(self.surface, flip[0], flip[1]), size)
        Show.object(img, x, y, tf, part)

    def rotate(self, angle):
        orig_rect, rot_image = [self.surface.get_rect(), transform.rotate(self.surface, angle)]
        rot_rect, rot_rect.center = [rot_image.get_rect().center, orig_rect]
        rot_image, self.surface = [rot_image.subsurface(rot_rect), rot_image]

    def collision(self, other_sprite, offset: tuple[int | float, ...] = (None, None)) -> None | tuple[int, ...]:
        ofst: tuple[int | float, ...]
        if offset == (None, None):
            ofst = (self.x + self.size[0] / 2 - (other_sprite.x + other_sprite.size[0] / 2),
                    self.y + self.size[1] / 2 - (other_sprite.y + other_sprite.size[1] / 2))
        else:
            ofst = offset
        if isinstance(other_sprite, Sprites):
            return mask.from_surface(self.surface).overlap(mask.from_surface(other_sprite.surface), ofst)
        elif isinstance(other_sprite, Surface):
            return mask.from_surface(self.surface).overlap(mask.from_surface(other_sprite), ofst)

    def when_collision(self, other_sprite) -> Callable[..., Any]:
        def decoretor(func: Callable[..., Any]) -> Callable[..., Any]:
            def wrap(*args, **kwargs) -> None: func(self.collision(other_sprite), *args, **kwargs)

            return wrap

        return decoretor

    def is_hovered(self) -> None:
        ofst: tuple[int | float, ...] = (self.x + self.size[0] / 2 - (mouse.get_pos()[0]),
                                         self.y + self.size[1] / 2 - (mouse.get_pos()[1]))
        return self.collision(Sprites.mouse_sprite.to_surface(), ofst)

    def is_clicked(self) -> None:
        return self.is_hovered() and mouse.get_pressed()[0]

    def when_hovered(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrap(*args, **kwargs) -> None: func(self.is_hovered(), *args, **kwargs)

        return wrap

    def when_clicked(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrap(*args, **kwargs) -> None: func(self.is_clicked(), *args, **kwargs)

        return wrap

    def side_update(self) -> None:
        self.side_set = {"top": {"_mask": mask.Mask((self.size[0] / 2, 1)),
                                 "_pos": [self.x, self.y - self.size[1] / 2]},
                         "right": {"_mask": mask.Mask((1, self.size[1] / 2)),
                                   "_pos": [self.x + self.size[0] / 2, self.y]},
                         "bottom": {"_mask": mask.Mask((self.size[0] / 2, 1)),
                                    "_pos": [self.x, self.y + self.size[1] / 2]},
                         "left": {"_mask": mask.Mask((1, self.size[1] / 2)),
                                  "_pos": [self.x - self.size[0] / 2, self.y]},
                         "center": {"_mask": mask.Mask((self.size[0] / 2, self.size[1] / 2)),
                                    "_pos": [self.x, self.y]},
                         "left to right": {"_mask": mask.Mask((self.size[0], self.size[1] / 2)),
                                           "_pos": [self.x, self.y - self.size[1] * 0 / 4]},
                         "top to bottom": {"_mask": mask.Mask((self.size[0] / 2, self.size[1])),
                                           "_pos": [self.x, self.y]}
                         }

    def __eq__(self, other):
        if len(self.__dict__) == len(other.__dict__):
            for i in self.__dict__:
                if not (["surface", "side_set"].__contains__(i)):
                    if other.__dict__.__contains__(i):
                        if not other.__dict__[i] == self.__dict__[i]: return False
                    else:
                        return False
                elif i == "side_set":
                    for j in self.side_set:
                        if not self.side_set[j]["_mask"].get_size() == other.side_set[j][
                            "_mask"].get_size(): return False
        else:
            return False
        return True
