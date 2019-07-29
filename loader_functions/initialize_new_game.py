import tcod as libtcod


def get_constants():
    window_tile = 'Jason\'s Roguelike'

    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height- panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2