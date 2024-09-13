from .Sprite import Sprites, Callable, Any


class ListSprites(Sprites):
    def __init__(self, pos: list, filename: str, size: tuple[float | int, ...]) -> None:
        self.object_list, self.pos, self.img, self.size = [[], pos, filename, size]
        for e, o in enumerate(self.pos):
            self.pos[e] = [o[0], o[1]]
            self.object_list.insert(e, Sprites(self.img, self.size, (o[0], o[1])))
        self.object_list: list[Sprites]
        Sprites.__init__(self, self.img, self.size, (0, 0))

    def show_list(self, pos: tuple[int, ...] = (None, None), size: tuple[float | int, ...] = (),
                  flip: tuple[bool, ...] = (False, False), tf: bool = True, part: tuple[int, ...] = (),
                  index: int = None, common: bool = False) -> None:
        x, y = pos
        if common:
            for i in self.object_list: i.show((x, y), size, flip, tf, part)
        else:
            self.object_list[index].show((x, y), size, flip, tf, part)

    def collision_list(self, other_sprite, offset: tuple[int | float, ...] = (None, None), index: int = None,
                       common: bool = False) -> None | tuple[int, ...] | list[list[int, ...]]:
        if common:
            il: list = []
            for e, i in enumerate(self.object_list):
                if i.collision(other_sprite, offset): il.append([e, i.collision(other_sprite, offset)])
            return il
        else:
            return self.object_list[index].collision(other_sprite, offset)

    def is_hovered_list(self, index: int, common: bool = False) -> None | bool | list[list[int, ...]]:
        if common:
            il: list = []
            for e, i in enumerate(self.object_list):
                if i.is_hovered(): il.append([e, i.is_hovered()])
            return il
        else:
            return self.object_list[index].is_hovered()

    def is_clicked_list(self, index: int, common: bool = False) -> None | bool | list[list[int, ...]]:
        if common:
            il: list = []
            for e, i in enumerate(self.object_list):
                if i.is_clicked(): il.append([e, i.is_clicked()])
            return il
        else:
            return self.object_list[index].is_clicked()

    def when_collision(self, other_sprite: Sprites, index: int = None, common: bool = False) -> Callable[..., Any]:
        def decoretor(func: Callable[..., Any]) -> Callable[..., Any]:
            if common:
                def wrap(*args, **kwargs) -> None:
                    for e, obj in enumerate(self.object_list): func(obj.collision(other_sprite), e, *args, **kwargs)

            else:
                def wrap(*args, **kwargs) -> None:
                    func(self.object_list[index].collision(other_sprite), index, *args, **kwargs)

            return wrap

        return decoretor

    def when_hovered(self, index: int = None, common: int = False) -> Callable[..., Any]:
        def decoretor(func: Callable[..., Any]) -> Callable[..., Any]:
            if common:
                def wrap(*args, **kwargs) -> None:
                    for e, obj in enumerate(self.object_list): func(obj.is_hovered(), e, *args, **kwargs)
            else:
                def wrap(*args, **kwargs) -> None:
                    func(self.object_list[index].is_hovered(), index, *args, **kwargs)

            return wrap

        return decoretor

    def when_clicked(self, index: int = None, common: bool = False) -> Callable[..., Any]:
        def decoretor(func: Callable[..., Any]) -> Callable[..., Any]:
            if common:
                def wrap(*args, **kwargs) -> None:
                    for e, obj in enumerate(self.object_list): func(obj.is_clicked(), e, *args, **kwargs)
            else:
                def wrap(*args, **kwargs) -> None:
                    func(self.object_list[index].is_clicked(), index, *args, **kwargs)

            return wrap

        return decoretor

    def __eq__(self, other) -> bool:
        if len(self.__dict__) == len(other.__dict__):
            for i in self.__dict__:
                if not self.__dict__[i] == other.__dict__[i]: return False
        else:
            return False
        return True

    def __getitem__(self, item: int) -> Sprites | None:
        if len(self.object_list) - 1 >= item:
            return self.object_list[item]
        else:
            return None
