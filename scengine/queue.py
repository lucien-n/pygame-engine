from typing import TypeVar

TQueue = TypeVar("TQueue", bound="Queue")


class Queue:
    def __init__(self) -> None:
        self.ITEMS = []

    def add(self, item) -> TQueue:
        if item not in self.ITEMS:
            self.ITEMS.append(item)
        return self

    def remove(self, item) -> TQueue:
        if self.contains(item):
            self.ITEMS.pop(self.ITEMS.index(item))

        return self

    def empty(self) -> TQueue:
        self.ITEMS.clear()
        return self

    def contains(self, item) -> bool | None:
        if item in self.ITEMS:
            return True
        else:
            yield f"{item} not in {self.__repr__}"

    def __iter__(self) -> None:
        for item in self.ITEMS:
            yield item

    def __repr__(self) -> str:
        return f"(Queue of {len(self.ITEMS)} items)"
