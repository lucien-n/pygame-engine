from scengine.entity import Entity
from scengine.vector2 import Vector2
import pygame as pg


class Player(Entity):
    def __init__(self, game, x: int | float = 50, y: int | float = 50) -> None:
        super().__init__(game, x, y)
        self.GAME = game

        self.keys_pressed = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

        self.speed = 220

    def set_key(self, key: str) -> None:
        """Set a key state to pressed

        Args:
            key (str): key name
        """
        self.keys_pressed[key] = True

    def reset_key(self, key: str) -> None:
        """Set a key state to unpressed

        Args:
            key (str): key name
        """
        self.keys_pressed[key] = False

    def get_key(self, key: str) -> None:
        """Returns the state of the key

        Args:
            key (str): key name

        Returns:
            bool: state of the key
        """
        return self.keys_pressed[key]

    def event_handler(self, events: list[pg.event.Event]) -> None:
        """Handle user input events

        Args:
            events (list[pg.event.Event]): list of events
        """
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_LEFT:
                        self.set_key("left")
                    case pg.K_RIGHT:
                        self.set_key("right")
                    case pg.K_UP:
                        self.set_key("up")
                    case pg.K_DOWN:
                        self.set_key("down")

            if event.type == pg.KEYUP:
                match event.key:
                    case pg.K_LEFT:
                        self.reset_key("left")
                    case pg.K_RIGHT:
                        self.reset_key("right")
                    case pg.K_UP:
                        self.reset_key("up")
                    case pg.K_DOWN:
                        self.reset_key("down")

    def update(self) -> None:
        """Updates the player"""
        super().update()

        self.move()
        self.rect.x, self.rect.y = self.position

        self.GAME.HUD.debug(
            f"Player | x: {self.position.x:.2f} y: {self.position.y:.2f}"
        )

    def move(self) -> None:
        """Moves the player according to recorded inputs"""

        speed = self.speed * self.ENGINE.DELTA_TIME
        velocity = Vector2(0, 0)

        if self.get_key("left"):
            velocity.add(Vector2(-speed, 0))
        if self.get_key("right"):
            velocity.add(Vector2(speed, 0))
        if self.get_key("up"):
            velocity.add(Vector2(0, -speed))
        if self.get_key("down"):
            velocity.add(Vector2(0, speed))

        self.position.add(velocity)

    def draw(self) -> None:
        super().draw(self.GAME.CAMERA.scroll)
