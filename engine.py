import tcod as libtcod

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all


def main():
    screen_width = 80
    screen_height = 50

    # Size of the Map
    map_width = 80
    map_height = 45

    # Some variables for the rooms in the map
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    player = Entity(int(screen_width/2), int(screen_height/2), '@', libtcod.white)
    npc = Entity(int(screen_width/2 -5), int(screen_height /2), '@', libtcod.yellow)
    entities = [npc,player]

    libtcod.console_set_custom_font('arial10X10.png', libtcod.FONT_TYPE_GREYSCALE|libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width,screen_height, 'Jason\'s rogue-like', False,
                              renderer=libtcod.RENDERER_SDL2, order='F', vsync=False)

    con = libtcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while libtcod.console_is_window_closed:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        game_exit = action.get('exit')
        full_screen = action.get('full_screen')

        if move:
            dx, dy = move

            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx,dy)

                fov_recompute = True

        if game_exit:
            return True

        if full_screen:
            libtcod.console_set_fullscreen(not lib.console_is_fullscreen())


if __name__ == '__main__':
    main()

