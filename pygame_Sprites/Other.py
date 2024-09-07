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
