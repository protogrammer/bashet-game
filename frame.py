import tkinter as tk
from tkinter import messagebox
from collections.abc import Callable
from typing import Union, Final
import random
import sys

import config
from utils import grid_buttons, configure_row_minsize

about_the_game: Final = '''Баше — математическая игра, в которой два игрока из кучки, содержащей первоначально N предметов.
Игроки по очереди берут не менее одного и не более М предметов.
Проигравшим считается тот, кому нечего брать.'''


def create(widget: tk.Tk,
           get_game_frame: Callable[[], tk.Frame],
           n_var: tk.IntVar,
           m_var: tk.IntVar,
           game_init: Callable[[], None],
           ) -> tk.Frame:
    frame = tk.Frame(widget, width=config.widget_width, height=config.widget_height)

    text_label = tk.Label(frame, text=about_the_game + '\nВыбери N и M.', justify=tk.LEFT, font=config.standard_font)

    m_scale = tk.Scale(
        frame,
        label='M',
        orient=tk.HORIZONTAL,
        length=config.scale_length,
        from_=1,
        to=n_var.get(),
        variable=m_var,
    )

    def m_scale_resize(arg: Union[str, int]) -> None:
        v = int(arg)
        if m_var.get() > v:
            m_var.set(v)
        m_scale.config(to=v)

    n_scale = tk.Scale(
        frame,
        label='N',
        orient=tk.HORIZONTAL,
        length=config.scale_length,
        from_=1,
        to=config.max_n,
        variable=n_var,
        command=m_scale_resize,
    )

    def switch_to_game() -> None:
        frame.pack_forget()
        game_init()
        get_game_frame().pack()

    def randomize_and_switch_to_game() -> None:
        n_var.set(random.randint(1, config.max_n))
        m_scale_resize(n_var.get())
        m_var.set(random.randint(1, n_var.get()))
        switch_to_game()

    def exit_program() -> None:
        if not messagebox.askokcancel('Выход из игры', 'Хочешь выйти?'):
            return
        widget.quit()
        sys.exit()

    buttons = [
        tk.Button(frame, text='Играть', command=switch_to_game),
        tk.Button(frame, text='Рандом', command=randomize_and_switch_to_game),
        tk.Button(frame, text='Выход', command=exit_program),
    ]

    col_num = len(buttons)
    row_num = 0

    text_label.grid(row=row_num, column=0, columnspan=col_num)
    row_num += 1

    n_scale.grid(row=row_num, column=0, columnspan=col_num)
    row_num += 1

    m_scale.grid(row=row_num, column=0, columnspan=col_num)
    row_num += 1

    row_num = grid_buttons(buttons, row_num)

    configure_row_minsize(frame, row_num, config.game_config_row_min_size)

    return frame
