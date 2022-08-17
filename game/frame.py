import tkinter as tk
import random
import time
from collections.abc import Callable

import config
from .game import Game
from utils import grid_buttons, configure_row_minsize


def computer_response(left: int, m: int) -> int:
    rest = left % (m + 1)
    if rest == 0:
        return random.randint(1, m)
    return rest


def create(widget: tk.Tk,
           get_config_frame: Callable[[], tk.Frame],
           n_var: tk.IntVar,
           m_var: tk.IntVar,
           ) -> tuple[tk.Frame, Callable[[], None]]:
    frame = tk.Frame(widget)

    n_m_info_labels = [
        tk.Label(frame, text='N:', font=config.big_font),
        tk.Label(frame, textvariable=n_var, font=config.big_font),
        tk.Label(frame, text='M:', font=config.big_font),
        tk.Label(frame, textvariable=m_var, font=config.big_font),
    ]

    canvas = tk.Canvas(
        frame,
        bg=config.canvas_background_color,
        width=config.canvas_width,
        height=config.canvas_height,
    )

    resign_button = tk.Button(frame)
    try_again_button = tk.Button(frame)
    next_turn_button = tk.Button(frame)

    game = Game(canvas, n_var, m_var, next_turn_button)

    n_m_info_labels.extend([
        tk.Label(frame, text='Взято:', font=config.big_font),
        tk.Label(frame, textvariable=game.get_taken_var(), font=config.big_font),
        tk.Label(frame, text='Осталось:', font=config.big_font),
        tk.Label(frame, textvariable=game.get_left_var(), font=config.big_font),
        tk.Label(frame, text='Ход:', font=config.big_font),
        tk.Label(frame, textvariable=game.get_turn_var(), font=config.big_font),
    ])

    enemy_turn: bool = False

    def mouse_down(event: tk.Event) -> None:
        if enemy_turn:
            return
        game.select(event.x, event.y)

    def mouse_up(event: tk.Event) -> None:
        if enemy_turn:
            return
        game.deselect(event.x, event.y)

    def mouse_move(event: tk.Event) -> None:
        if enemy_turn:
            return
        game.move_selected(event.x, event.y)

    canvas.bind('<Button-1>', mouse_down)
    canvas.bind('<ButtonRelease-1>', mouse_up)
    canvas.bind('<B1-Motion>', mouse_move)

    def switch_to_config() -> None:
        frame.pack_forget()
        get_config_frame().pack()

    buttons = [
        resign_button,
        try_again_button,
        next_turn_button,
    ]

    def next_turn() -> None:
        game.reset_taken()
        if game.stars_left() == 0:
            time.sleep(config.game_result_sleep_sec)
            canvas.create_text(
                config.canvas_width // 2,
                config.canvas_height // 2,
                text='ПОБЕДА',
                fill=config.victory_text_color,
                font=config.game_result_font,
                anchor=tk.CENTER,
            )
            resign_button.config(text='Назад')
            next_turn_button.config(state=tk.DISABLED)
            return

        nonlocal enemy_turn
        enemy_turn = True
        for button in buttons:
            button.config(state=tk.DISABLED)

        def callback() -> None:
            game.reset_taken()
            nonlocal enemy_turn
            enemy_turn = False
            for button in buttons[:2]:
                button.config(state=tk.NORMAL)
            if game.stars_left() == 0:
                time.sleep(config.game_result_sleep_sec)
                canvas.create_text(
                    config.canvas_width // 2,
                    config.canvas_height // 2,
                    text='ПОРАЖЕНИЕ!',
                    fill=config.defeat_text_color,
                    font=config.game_result_font,
                    anchor=tk.CENTER,
                )
                resign_button.config(text='Назад')
                return
            next_turn_button.config(text='Следующий ход')
            turn = game.get_turn_var()
            turn.set(turn.get() + 1)

        response = computer_response(game.stars_left(), m_var.get())
        game.enemy_turn(response, callback)

    def init_buttons() -> None:
        def init() -> None:
            init_buttons()
            game.reinit()
        resign_button.config(text='Сдаться', command=switch_to_config, state=tk.NORMAL)
        try_again_button.config(text='Заново', command=init, state=tk.NORMAL)
        next_turn_button.config(text='Передать очередь хода', command=next_turn, state=tk.NORMAL)

    init_buttons()

    col_num = max(len(n_m_info_labels), len(buttons))
    row_num = 0

    for i, label in enumerate(n_m_info_labels):
        label.grid(row=row_num, column=i)
    row_num += 1

    canvas.grid(row=row_num, column=0, columnspan=col_num)
    row_num += 1

    grid_buttons(buttons[:2], row_num, 3)
    next_turn_button.grid(row=row_num, column=2*3, columnspan=4)
    row_num += 1

    configure_row_minsize(frame, row_num, config.game_row_min_size)

    def reinit() -> None:
        init_buttons()
        game.reinit()

    return frame, reinit
