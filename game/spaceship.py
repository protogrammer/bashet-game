import tkinter as tk

from .types import BaseGame, BaseSpaceship, SPACESHIP_IMAGE_STATE, ANCHOR_TYPE


class Spaceship(BaseSpaceship):
    def __init__(self,
                 game: BaseGame,
                 image: tk.Image,
                 brighter_image: tk.Image,
                 x: int,
                 y: int,
                 anchor: ANCHOR_TYPE):
        self.game: BaseGame = game
        self.image: tk.Image = image
        self.brighter_image: tk.Image = brighter_image
        self.x: int = x
        self.y: int = y
        self.anchor: ANCHOR_TYPE = anchor
        self.activity_status: SPACESHIP_IMAGE_STATE = 'normal'

    def draw(self) -> None:
        self.game.get_canvas().create_image(
            self.x,
            self.y,
            image=self.image if self.activity_status == 'normal' else self.brighter_image,
            anchor=self.anchor,
        )

    def width(self) -> int:
        return self.image.width()

    def height(self) -> int:
        return self.image.height()

    def is_bright(self) -> bool:
        return self.activity_status == 'bright'

    def set_brightness_status(self, status: SPACESHIP_IMAGE_STATE):
        assert(status in SPACESHIP_IMAGE_STATE.__args__)
        self.activity_status = status
