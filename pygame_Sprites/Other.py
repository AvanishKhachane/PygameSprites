from types import FunctionType
from typing import Sized, Iterable, Callable, Any


class Ig:
    def __init__(self, i: Sized | Iterable, func: Callable[..., Any]) -> None:
        self.e, self.i, self.len, self.func = [0, i, len(i), func]

    def __next__(self) -> Any:
        self.e %= self.len
        if isinstance(self.i, dict):
            r: Any = list(self.i.keys())[self.e]
        else:
            r: Any = list(self.i)[self.e]
        self.e += 1
        return self.func(r)

    def __iter__(self) -> Any:
        return Ig(self.i, self.func)

    def __len__(self):
        return len(self.i)


def whencall(class_type):
    class_type: type = class_type

    def deco(met: FunctionType):
        def wrap(*args, **kwargs):
            met(*args, **kwargs)
            print(f"{met.__name__} was called")

        return wrap

    for i in dir(class_type):
        if isinstance(getattr(class_type, i), FunctionType) and i != "__init__":
            setattr(class_type, i, deco(getattr(class_type, i)))
    return class_type
