import random
import tkinter as tk


def rand_color() -> str:
    return '#' + ''.join('0123456789abcdef'[random.randrange(0, 16)] for _ in range(9))


def grid_buttons(buttons: list[tk.Button], row_num: int, column_span: int = 1) -> int:
    for i, button in enumerate(buttons):
        button.grid(row=row_num, column=i*column_span, columnspan=column_span)
    row_num += 1
    return row_num


def configure_row_minsize(frame: tk.Frame, row_num: int, min_size: int) -> None:
    for i in range(row_num):
        frame.rowconfigure(i, minsize=min_size)
