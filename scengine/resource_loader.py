import pygame as pg
import os
from typing import TypeVar

TResourceLoader = TypeVar("TResourceLoader", bound="ResourceLoader")


class ResourceLoader:
    def __init__(self, resource_folder) -> None:
        self.resources = {}
        self.textures = {}
        self.resource_folder = resource_folder

    def load_sprites(self) -> dict[str : pg.surface.Surface]:
        sprites = {}
        for file in os.listdir(self.resource_folder / "textures"):
            sprites[str(file).replace(".png", "")] = pg.image.load(
                f"{self.resource_folder}/textures/{file}"
            ).convert()

        return self
