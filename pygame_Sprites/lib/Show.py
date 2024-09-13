from pygame import Surface, font

from .Other import whencall


@whencall
class Show:
    screen: Surface

    @classmethod
    def object(cls, obj, x: int | float, y: int | float, tf: bool = None, part: tuple[int, ...] = None) -> None:
        if tf or tf is None:
            if part:
                if type(part) == tuple:
                    cls.screen.blit(obj, (x, y), part)
                elif type(part) == bool:
                    cls.screen.blit(obj, (x, y))
            else:
                cls.screen.blit(obj, (x, y))

    @classmethod
    def text(cls, filename: str, font_size: int, text: str, x: int | float, y: int | float, tf: bool = None,
             rgb: tuple[int, ...] = None, axis: int = 0) -> None:
        font_family = filename
        if tf is None: tf = True
        if rgb is None: rgb = (0, 0, 0)
        proccessd_font: font.Font = font.Font(font_family, font_size)
        rendered_font = proccessd_font.render(str(text), tf, rgb)
        offset: int | float = 0
        if [0, 1].__contains__(axis): offset = font.Font.size(proccessd_font, text)[0] / (2 - axis)
        if tf: cls.screen.blit(rendered_font, (x - offset, y))
