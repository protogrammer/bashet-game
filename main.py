import tkinter as tk
import random
import time

import config
import game.frame
import frame


def main() -> None:
    random.seed(time.time())

    widget = tk.Tk()

    widget.title('Игра Баше')
    widget.geometry(f'{config.widget_width}x{config.widget_height}')
    widget.resizable(width=False, height=False)
    widget.iconbitmap(config.bashet_game_icon)

    n = tk.IntVar(value=15)
    m = tk.IntVar(value=3)

    game_frame, init_game = game.frame.create(widget, lambda: config_frame.pack(), n, m)
    config_frame = frame.create(widget, game_frame.pack, n, m, init_game)

    config_frame.pack()

    widget.mainloop()


if __name__ == '__main__':
    main()
