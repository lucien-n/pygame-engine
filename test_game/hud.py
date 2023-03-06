from typing import TypeVar

THud = TypeVar("THud", bound="Hud")


class Hud:
    def __init__(self, game: object) -> None:
        self.GAME = game
        self.debug_lines = []

    def update(self):
        self.debug_lines.clear()

        self.debug(int(self.GAME.CLOCK.get_fps()))

    def draw(self) -> THud:
        for line in self.debug_lines:
            self.GAME.WINDOW.blit(line["font"], line["pos"])

        return self

    def debug(self, text: str) -> THud:
        self.debug_lines.append(
            {
                "font": self.GAME.font(text),
                "pos": (0, len(self.debug_lines) + len(self.debug_lines) * 20),
            }
        )
        return self
