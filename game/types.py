import tkinter as tk
from abc import abstractmethod, ABC
from collections.abc import Callable
from typing import Union, Literal, Any, Optional, Final

import config


class BaseStar(ABC):
    @abstractmethod
    def is_mine(self) -> bool:
        """Касается ли звезда моего корабля"""

    @abstractmethod
    def is_enemy(self) -> bool:
        """Касается ли звезда корабля соперника"""

    @abstractmethod
    def move_randomly(self) -> None:
        """Переместить звезду в произвольное место"""

    @abstractmethod
    def draw(self,
             color: Optional[str] = None,
             outline_color: str = config.outline_color,
             ) -> None:
        """Нарисовать звезду"""

    @abstractmethod
    def contains(self, x: int, y: int) -> bool:
        """Пренадлежит ли звезде точка (x, y)"""

    @abstractmethod
    def touches(self, other: 'BaseStar') -> bool:
        """Касается ли звезда другой звезды"""

    @abstractmethod
    def coordinates(self) -> tuple[int, int]:
        """Координаты центра звезды"""

    @abstractmethod
    def set_coordinates(self, x: int, y: int) -> None:
        """Установить координаты центра звезды"""

    @abstractmethod
    def get_radius(self) -> int:
        """Получить радиус"""


SPACESHIP_IMAGE_STATE: Final = Literal['normal', 'bright']
ANCHOR_TYPE: Final = Union[tk.NW, tk.N, tk.NE, tk.W, tk.CENTER, tk.E, tk.SW, tk.S, tk.SE]


class BaseSpaceship(ABC):
    @abstractmethod
    def draw(self) -> None:
        """Нарисовать корабль"""

    @abstractmethod
    def width(self) -> int:
        """Получить ширину корабля"""

    @abstractmethod
    def height(self) -> int:
        """Получить высоту корабля"""

    @abstractmethod
    def is_bright(self) -> bool:
        """Используется ли более яркая картинка при отрисовке корабля"""

    @abstractmethod
    def set_brightness_status(self, status: SPACESHIP_IMAGE_STATE):
        """Установить яркость корабля"""


class BaseGame(ABC):
    @abstractmethod
    def reinit(self) -> None:
        """Реинициализировать"""

    @abstractmethod
    def for_all(self,
                f: Callable[[int, BaseStar], Union[Literal[True], Any]],
                ) -> None:
        """Выполнить функцию для каждой звезды"""

    @abstractmethod
    def my_spaceship(self) -> BaseSpaceship:
        """Получить мой корабль"""

    @abstractmethod
    def enemy_spaceship(self) -> BaseSpaceship:
        """Получить вражеский корабль"""

    @abstractmethod
    def is_mine(self, x: int, y: int) -> bool:
        """Относится ли точка к моему кораблю"""

    @abstractmethod
    def get_canvas(self) -> tk.Canvas:
        """Получить объект tkinter.Canvas, который относится к данному объекту"""

    @abstractmethod
    def select(self, x: int, y: int) -> None:
        """Выбрать звезду в данной точке, если таковая имеется"""

    @abstractmethod
    def move_selected(self, x: int, y: int) -> None:
        """Переместить выбранную звезду в данную точку"""

    @abstractmethod
    def deselect(self,
                 x: Optional[int] = None,
                 y: Optional[int] = None
                 ) -> None:
        """Убрать выделение с выделенной звезды.
        Если звезда над моим кораблём, то захватить её.
        Если звезда над кораблём соперника, переместить её на начальную позицию"""

    @abstractmethod
    def remove_selected(self) -> None:
        """Удалить выделенную звезду"""

    @abstractmethod
    def nothing_selected(self) -> bool:
        """Возвращает True если ничего не выделено"""

    @abstractmethod
    def taken(self) -> int:
        """Количество захваченных звёзд"""

    @abstractmethod
    def reset_taken(self) -> None:
        """Установить количество захваченных звёзд в ноль"""

    @abstractmethod
    def stars_left(self) -> int:
        """Количество оставшихся незахваченными звёзд"""

    @abstractmethod
    def get_taken_var(self) -> tk.IntVar:
        """Получить объект типа tkinter.IntVar, хранящий информацию о количестве захваченных звёзд"""

    @abstractmethod
    def get_left_var(self) -> tk.IntVar:
        """Получить объект типа tkinter.IntVar, хранящий информацию о количестве оставшихся незахваченными звёзд"""

    @abstractmethod
    def get_turn_var(self) -> tk.IntVar:
        """Получить объект типа tkinter.IntVar, хранящий информацию о номере текущего хода"""

    @abstractmethod
    def enemy_turn(self, take: int, callback: Callable[[], None]) -> None:
        """Визуализировать ход соперника"""
