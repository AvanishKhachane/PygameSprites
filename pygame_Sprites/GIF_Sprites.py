import time
from os import remove

from PIL import Image

from .Other import Ig
from .Sprite import Sprites, Show, Surface, transform, image


class GIFSprites(Sprites):
    def return_surface(self, index):
        return self.imgs[index]

    def __init__(self, filename: str, fps: int, size: tuple[int, ...], pos: tuple[int, ...] = (None, None)):
        self.fps, self.size, imgs = [fps, size, {}]
        with Image.open(filename) as images:
            for i in range(images.n_frames):
                images.seek(i), images.save(f"{i}.png")
                img_d = image.load(f"{i}.png")
                Surface.set_colorkey(img_d, (234, 234, 234))
                imgs[str(i)] = transform.scale(img_d, tuple(self.size))
                remove(f"{i}.png")
        self.x, self.y, self.imgs = pos[0], pos[1], imgs
        self.img_generetor = Ig(self.imgs, self.return_surface)
        Sprites.__init__(self, self.imgs["0"], self.size, (self.x, self.y))

    def show_gif(self, pos: tuple[int, ...] = (None, None), tf: bool = True, part: tuple[int, ...] = ()):
        x, y = pos
        if tf:
            if not part: part = (0, 0, self.size[0], self.size[1])
            if x is None: x = self.x - self.size[0] / 2
            if y is None: y = self.y - self.size[1] / 2
            time.sleep(1 / self.fps)
            Show.object(next(self.img_generetor), x, y, True, part)
