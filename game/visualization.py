import tkinter as tk
import random
from collections.abc import Callable
from typing import Any, Union, Literal, Final, Optional

import config
from .star import Star
from .spaceship import Spaceship
from .types import BaseStar, BaseGame, BaseSpaceship


def _update_vars(f: Callable[[BaseGame, ...], Any]) -> Any:
    def inner(self: BaseGame, *args, **kwargs) -> Any:
        try:
            return f(self, *args, **kwargs)
        finally:
            self.get_taken_var().set(self.taken())
            self.get_left_var().set(self.stars_left())

    return inner


class Game(BaseGame):
    def __init__(self,
                 canvas: tk.Canvas,
                 n_var: tk.IntVar,
                 m_var: tk.IntVar,
                 next_turn_button: tk.Button):
        self.canvas: Final[tk.Canvas] = canvas
        self.n_var: Final[tk.IntVar] = n_var
        self.m_var: Final[tk.IntVar] = m_var
        self.next_turn_button: Final[tk.Button] = next_turn_button
        self.me: Final[BaseSpaceship] = Spaceship(
            self,
            tk.PhotoImage(file=config.my_spaceship_image),
            tk.PhotoImage(file=config.my_spaceship_brighter_image),
            0,
            0,
            tk.NW,
        )
        self.enemy: Final[BaseSpaceship] = Spaceship(
            self,
            tk.PhotoImage(file=config.enemy_spaceship_image),
            tk.PhotoImage(file=config.enemy_spaceship_brighter_image),
            config.canvas_width,
            config.canvas_height,
            tk.SE,
        )
        self.turn: Final[tk.IntVar] = tk.IntVar(value=1)
        self.stars: list[BaseStar] = []
        self.selected: int = -1
        self.selected_initial_pos: tuple[int, int] = (0, 0)
        self.im_selected: bool = False
        self.taken_stars: list[BaseStar] = []
        self.taken_var: Final[tk.IntVar] = tk.IntVar(value=0)
        self.left_var: Final[tk.IntVar] = tk.IntVar(value=n_var.get())

    @_update_vars
    def reinit(self) -> None:
        self.turn.set(1)
        self.taken_var.set(0)
        self.left_var.set(self.n_var.get())
        self.stars = [Star(self) for _ in range(self.n_var.get())]
        self.selected = -1
        self.im_selected = False
        self.taken_stars = []
        self.canvas.create_rectangle(
            0,
            0,
            config.canvas_width,
            config.canvas_height,
            outline=config.canvas_background_color,
            fill=config.canvas_background_color,
        )
        self.me.draw()
        self.enemy.draw()
        self.for_all(lambda _, star: star.draw())

    def for_all(self,
                f: Callable[[int, BaseStar], Union[Literal[True], Any]],
                ) -> None:
        for i, star in enumerate(self.stars):
            if f(i, star) is True:
                return

    def my_spaceship(self) -> BaseSpaceship:
        return self.me

    def enemy_spaceship(self) -> BaseSpaceship:
        return self.enemy

    def is_mine(self, x: int, y: int) -> bool:
        return x < self.me.width() and y < self.me.height()

    def get_canvas(self) -> tk.Canvas:
        return self.canvas

    def _activate_me(self):
        self.im_selected = True
        self.me.set_brightness_status('bright')
        self.me.draw()

    def _deactivate_me(self):
        self.im_selected = False
        self.me.set_brightness_status('normal')
        self.me.draw()

    @_update_vars
    def select(self, x: int, y: int) -> None:
        def do(i: int, star: BaseStar) -> None:
            if star.contains(x, y):
                self.selected = i
                self.selected_initial_pos = star.coordinates()
        self.selected = -1
        self.for_all(do)
        if self.nothing_selected():
            if self.taken_stars and self.is_mine(x, y):
                self._activate_me()
        else:
            self.stars[self.selected].draw()

    def _erase_selected(self) -> None:
        if self.nothing_selected():
            return
        selected_star = self.stars[self.selected]

        bg = config.canvas_background_color
        selected_star.draw(bg, bg)

        def do(i: int, star: BaseStar) -> None:
            if i != self.selected and selected_star.touches(star):
                star.draw()

        self.for_all(do)

        if selected_star.is_mine():
            self.me.draw()
        if selected_star.is_enemy():
            self.enemy.draw()

    @_update_vars
    def move_selected(self, x: int, y: int) -> None:
        if self.nothing_selected():
            if self.im_selected:
                if not self.is_mine(x, y):
                    self._deactivate_me()
            elif self.taken_stars and self.is_mine(x, y):
                self._activate_me()
            return
        selected_star = self.stars[self.selected]
        r = selected_star.get_radius()
        if min(x, y, config.canvas_width - x, config.canvas_height - y) < r:
            return
        self._erase_selected()
        selected_star.set_coordinates(x, y)
        if self.taken() < self.m_var.get() and selected_star.is_mine():
            if not self.me.is_bright():
                self._activate_me()
        elif self.me.is_bright():
            self._deactivate_me()
        selected_star.draw()

    @_update_vars
    def deselect(self,
                 x: Optional[int] = None,
                 y: Optional[int] = None,
                 ) -> None:
        if self.nothing_selected():
            if self.im_selected:
                self._deactivate_me()
            else:
                return
            if x is not None and y is not None and self.taken_stars and self.is_mine(x, y):
                star = self.taken_stars.pop()
                self.stars.append(star)
                star.move_randomly()
                star.draw()
                if self.taken_stars:
                    return
                if self.turn.get() == 1:
                    self.next_turn_button.config(text='Передать очередь хода', state=tk.NORMAL)
                else:
                    self.next_turn_button.config(state=tk.DISABLED)
            return
        selected_star = self.stars[self.selected]
        if selected_star.is_mine():
            if self.taken() < self.m_var.get():
                if not self.taken_stars:
                    self.next_turn_button.config(text='Следующий ход', state=tk.NORMAL)
                self._erase_selected()
                self.remove_selected()
                self.me.set_brightness_status('normal')
                self.me.draw()
            else:
                self.move_selected(*self.selected_initial_pos)
        if selected_star.is_enemy():
            self.move_selected(*self.selected_initial_pos)
        self.selected = -1

    def remove_selected(self) -> None:
        if self.nothing_selected():
            return
        self.taken_stars.append(self.stars[self.selected])
        del self.stars[self.selected]
        self.selected = -1

    def nothing_selected(self) -> bool:
        return self.selected == -1

    def taken(self) -> int:
        return len(self.taken_stars)

    @_update_vars
    def reset_taken(self) -> None:
        self.taken_stars = []

    def stars_left(self) -> int:
        return len(self.stars)

    def get_taken_var(self) -> tk.IntVar:
        return self.taken_var

    def get_left_var(self) -> tk.IntVar:
        return self.left_var

    def get_turn_var(self) -> tk.IntVar:
        return self.turn

    def _select_random(self) -> None:
        if not self.stars:
            raise Exception('Game._select_random: self.stars is empty')
        self.selected = random.randrange(len(self.stars))
        self.selected_initial_pos = self.stars[self.selected].coordinates()

    @_update_vars
    def _enemy_gets_the_star(self,
                             take_time_ms: int,
                             bright_time_ms: int,
                             times: int,
                             callback: Callable[[], None],
                             ) -> None:
        if times == 0:
            callback()
            return

        self._select_random()

        def after1():
            self.enemy.set_brightness_status('bright')
            self.enemy.draw()

            def after2():
                self._erase_selected()
                self.remove_selected()

                def after3():
                    self.enemy.set_brightness_status('normal')
                    self.enemy.draw()
                    self._enemy_gets_the_star(take_time_ms, bright_time_ms, times-1, callback)

                self.canvas.after(bright_time_ms // 2, after3)

            self.canvas.after(bright_time_ms // 2, after2)

        self.canvas.after(take_time_ms, after1)

    @_update_vars
    def enemy_turn(self, take: int, callback: Callable[[], None]) -> None:
        once = config.enemy_turn_time_ms / take
        bright_time_ms = round(once*config.enemy_bright_proportion)
        take_time_ms = round(once*(1-config.enemy_bright_proportion))
        self._enemy_gets_the_star(bright_time_ms, take_time_ms, take, callback)
