import pygame as pg
import pygame.freetype
import time
from pathlib import Path

path = Path(__file__).parent

from .loader import ResourceLoader, SettingsLoader
from .colors import Colors
from .queue import Queue


class Engine:
    pg.init()

    def __init__(
        self,
        title: str = "SCEngine",
        size: tuple[int] = (1280, 720),
        background_color: pg.Color = Colors.background,
        resource_folder: str = path / "resources",
    ) -> None:
        self.TITLE = title
        self.SIZE = self.WIDTH, self.HEIGHT = size

        self.WINDOW = pg.display.set_mode(self.SIZE, True)

        self.CLOCK = pg.time.Clock()

        self.FONT = pygame.freetype.Font(
            rf"{resource_folder}/fonts/default.otf", 12, False, False
        )
        self.FONT.antialiased = False

        self.RESOURCE_LOADER = ResourceLoader(resource_folder)
        self.RESOURCE_LOADER.load_sprites()
        self.SPRITES = self.RESOURCE_LOADER.sprites

        self.SETTINGS_LOADER = SettingsLoader(resource_folder / "settings.yaml")
        self.SETTINGS = self.SETTINGS_LOADER.load_settings()

        self.BACKGROUND_COLOR = background_color

        self.DELTA_TIME = None
        self.prev_time = time.time()
        self.now = 0

        self.EVENT_HANDLER_Q = Queue()
        self.UPDATE_Q = Queue()
        self.DRAW_Q = Queue()

        self.DRAW_ACCORDING_TO_CAMERA_SCROLL = True

        self.DRAWING_SURFACE = self.WINDOW

        self.RUNNING = False

    def event_handler(self) -> None:
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                self.RUNNING = False

        [item.event_handler(events) for item in self.EVENT_HANDLER_Q]

    def update(self) -> None:
        [item.update() for item in self.UPDATE_Q]

    def draw(self) -> None:
        self.WINDOW.fill(self.BACKGROUND_COLOR)
        [item.draw() for item in self.DRAW_Q]

    def run(self):
        self.RUNNING = True

        while self.RUNNING:
            self.now = time.time()
            self.DELTA_TIME = self.now - self.prev_time
            self.prev_time = self.now

            self.event_handler()
            self.update()
            self.draw()

            if not self.RUNNING:
                exit(0)

    def font(
        self,
        content: str = "Placeholder",
        size: int = 20,
        color: tuple = Colors.white,
        bgcolor: tuple = None,
        padding: int = 4,
    ) -> pg.surface.Surface:
        """Renders text with given arguments

        Args:
            content (str, optional): Displayed text. Defaults to "Placeholder".
            size (int, optional): Text's size. Defaults to 24.
            color (tuple, optional): Text's color. Defaults to Colors.white.
            bgcolor (tuple, optional): Text's background color. Defaults to None.
            padding (int, optional): Text's padding. Defaults to 4.

        Returns:
            pygame.Surface: Rendered text surface
        """
        rendered_text = self.FONT.render(
            str(content), color, None, pygame.freetype.STYLE_DEFAULT, 0, size
        )[0]

        padded_rendered_text = pygame.Surface(
            (
                rendered_text.get_width() + padding * 2,
                rendered_text.get_height() + padding * 2,
            )
        )
        padded_rendered_text.convert_alpha()

        if bgcolor:
            padded_rendered_text.fill(bgcolor)

        padded_rendered_text.blit(rendered_text, (padding, padding))

        return padded_rendered_text

    def surf2arr(self, *args: list | dict | pg.surface.Surface) -> list | dict:
        if type(args[0]) == list:
            return [pg.surfarray.array3d(surface) for surface in args[0]]
        elif type(args[0]) == dict:
            return {key: pg.surfarray.array3d(value) for key, value in args[0].items()}
        else:
            return pg.surfarray.array3d(args[0])

    def arr2surf(self, *args: list | dict) -> list | dict:
        if len(args) > 1 and type(args[0]) == list:
            return [pg.surfarray.make_surface(array) for array in args[0]]
        elif type(args[0]) == dict:
            return {
                key: pg.surfarray.make_surface(value) for key, value in args[0].items()
            }
        else:
            return pg.surfarray.make_surface(args[0])
