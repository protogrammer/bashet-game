from typing import Final
from os.path import join

widget_width: Final = 800
widget_height: Final = 450

standard_font: Final = 'courier 14 bold'
big_font: Final = 'courier 28 bold'

game_row_min_size: Final = 70
game_config_row_min_size: Final = 120

scale_text_offset: Final = 9
scale_length: Final = widget_width - 10

canvas_width: Final = widget_width - 30
canvas_height: Final = 2 * canvas_width // 5
outline_color: Final = 'lightblue'
canvas_background_color: Final = 'black'

max_n: Final = 100

star_min_radius: Final = 5
star_max_radius: Final = 25

enemy_turn_time_ms: Final = 3000
enemy_bright_proportion: Final = 0.6

__image_directory = 'imgs'
bashet_game_icon: Final = join(__image_directory, 'bashet-game.ico')
my_spaceship_image: Final = join(__image_directory, 'spaceship.gif')
my_spaceship_brighter_image: Final = join(__image_directory, 'bright-spaceship.gif')
enemy_spaceship_image: Final = join(__image_directory, 'enemy-spaceship.gif')
enemy_spaceship_brighter_image: Final = join(__image_directory, 'bright-enemy-spaceship.gif')

game_result_font: Final = 'courier 40 bold'
victory_text_color: Final = 'green'
defeat_text_color: Final = 'red'

game_result_sleep_sec: Final = 0.3
