from pygame import image, Rect, font

from .Sprite import Sprites, Show, Surface, transform


class TextInput(Sprites):
    def __init__(self, filename: str, font_file: str, font_size: int, dis: tuple[Rect, ...],
                 font_offset: tuple[int, ...] = (0, 0), size: tuple[float | int, ...] = (0, 0), x: int = 0, y: int = 0):
        self.ref_image: Surface = transform.scale(image.load(filename), size)
        self.start_part: Surface = self.ref_image.subsurface(dis[0])
        self.middle_part: Surface = self.ref_image.subsurface(dis[1])
        self.end_part: Surface = self.ref_image.subsurface(dis[2])
        self.x, self.y, self.font, self.font_size, self.text, self.entered_text = [x, y, font_file, font_size, "", ""]
        self.proccessed_font, self.font_offset = [font.Font(self.font, self.font_size), font_offset]
        self.sprite: Sprites = Sprites(filename, size, (x - size[0] / 2, y - size[0] / 2))
        Sprites.__init__(self, filename, size, (x, y))

    def box_config(self):
        font_width = font.Font.size(font.Font(self.font, self.font_size), self.text)[0]
        if font_width < 16: font_width = 16
        self.middle_part = transform.scale(self.middle_part, (font_width, self.middle_part.get_size()[1]))
        Show.object(self.start_part, self.x, self.y)
        Show.object(self.middle_part, self.x + self.start_part.get_size()[0], self.y)
        Show.object(self.end_part, self.x + self.start_part.get_size()[0] + self.middle_part.get_size()[0], self.y)

    def typeing(self, key: int):
        if key == 8:
            self.text = self.text[:-1]
        elif key == 13:
            self.entered_text = self.text
        elif 32 <= key <= 126:
            self.text += chr(key)

    def show(self, pos: tuple[int, ...] = (None, None), size: tuple[float | int, ...] = (),
             flip: tuple[bool, ...] = (False, False), tf: bool = True, rgb: tuple[int, ...] = (0, 0, 0),
             part: tuple[int, ...] = ()) -> None:
        x, y = pos
        if not x: x = self.x - self.size[0] / 2
        if not y: y = self.y - self.size[1] / 2
        self.box_config()
        Show.text(self.font, self.font_size, self.text, x + self.font_offset[0], y + self.font_offset[1], tf, rgb, -1)

    def __getitem__(self, item: int) -> str:
        return self.text[item]

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)

    def __bool__(self):
        return bool(len(self.text))
