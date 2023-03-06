import pygame as pg
from .vector2 import Vector2
from typing import TypeVar

TCamera = TypeVar("TCamera", bound="Camera")


class Camera:
    def __init__(self, game: object) -> None:
        self.GAME = game

        self.followed = None
        self.scroll = Vector2(0, 0)
        self.scroll_smoothness = self.GAME.SETTINGS["video"]["camera_scroll_smoothness"]

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
        if (
            self.followed.position.x - self.scroll.x
            != self.GAME.DRAWING_SURFACE.get_width() / 2
        ):
            self.scroll.x += (
                self.followed.position.x
                - (self.scroll.x + self.GAME.DRAWING_SURFACE.get_width() / 2)
            ) / self.scroll_smoothness

        if (
            self.followed.position.y - self.scroll.y
            != self.GAME.DRAWING_SURFACE.get_height() / 2
        ):
            self.scroll.y += (
                self.followed.position.y
                - (self.scroll.y + self.GAME.DRAWING_SURFACE.get_height() / 2)
            ) / self.scroll_smoothness

        return self
