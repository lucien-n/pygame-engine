import pygame as pg
from .vector2 import Vector2
from typing import TypeVar

TCamera = TypeVar("TCamera", bound="Camera")


class Camera:
    def __init__(self, display: pg.surface.Surface) -> None:
        self.display = display

        self.followed = None
        self.scroll = Vector2(0, 0)
        self.scroll_smoothness = 10

    def follow(self, object: object) -> TCamera:
        """Changes the camera followed object

        Args:
            object (object): An object with an x and y position

        Returns:
            Camera: self
        """
        self.followed = object

        return self

    def update(self) -> TCamera:
        """Updates the camera scroll

        Returns:
            Camera: self
        """
        if self.follow.x - self.scroll.x != self.display.get_width() / 2:
            self.scroll.x += (
                self.follow.x - (self.scroll.x + self.display.get_width() / 2)
            ) / self.scroll_smoothness
        if self.follow.y - self.follow.y != self.display.get_height() / 2:
            self.scroll.y += (
                self.follow.y - (self.scroll.y + self.display.get_height() / 2)
            ) / self.scroll_smoothness

        self.scroll = Vector2(int(self.scroll.x), int(self.scroll.y))

        return self
