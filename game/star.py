import random
from typing import Optional
import math

import config
from utils import rand_color
from .types import BaseStar, BaseGame


class Star(BaseStar):
    def __init__(self, parent: BaseGame):
        self.parent: BaseGame = parent
        self.radius: int = random.randint(config.star_min_radius, config.star_max_radius)
        self.x: int = 0
        self.y: int = 0
        self.move_randomly()
        self.color: str = rand_color()

    def is_mine(self) -> bool:
        return self.x <= self.radius + self.parent.my_spaceship().width() \
               and self.y <= self.radius + self.parent.my_spaceship().height()

    def is_enemy(self) -> bool:
        return self.x + self.radius >= config.canvas_width - self.parent.enemy_spaceship().width() \
               and self.y + self.radius >= config.canvas_height - self.parent.enemy_spaceship().height()

    def move_randomly(self) -> None:
        while True:
            self.x = random.randint(self.radius, config.canvas_width - self.radius)
            self.y = random.randint(self.radius, config.canvas_height - self.radius)
            if not (self.is_mine() or self.is_enemy()):
                return

    def draw(self,
             color: Optional[str] = None,
             outline_color: str = config.outline_color,
             ) -> None:
        if color is None:
            color = self.color
        self.parent.get_canvas().create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            outline=outline_color,
            fill=color,
        )

    def contains(self, x: int, y: int) -> bool:
        diff_x = abs(x - self.x)
        diff_y = abs(y - self.y)
        return math.ceil(math.sqrt(diff_x**2 + diff_y**2)) <= self.radius

    def touches(self, other: BaseStar) -> bool:
        x, y = other.coordinates()
        diff_x = abs(x - self.x)
        diff_y = abs(y - self.y)
        return math.ceil(math.sqrt(diff_x**2 + diff_y**2)) <= self.radius + other.get_radius()

    def coordinates(self) -> tuple[int, int]:
        return self.x, self.y

    def set_coordinates(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_radius(self) -> int:
        return self.radius
