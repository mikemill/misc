class Grue(object):
    def __init__(self, game_map, player):
        self.game_map = game_map
        self.player = player
        self.room = None

        self.spawn()

    def spawn(self):
        """Spawn Grue at the furthest point from the player"""
        self.room = self.game_map[self.player.room]['spawn']

    def move(self):
        """Move grue closer to the player using the shortest path"""
        direction = self.game_map.shortest_paths[self.room][self.player.room]
        self.room = self.game_map.move(self.room, direction)

    def flee(self):
        """Grue flees from the player in a random direction"""
        for direction in self.game_map.random_direction():
            new_room = self.game_map.move(self.room, direction)
            if new_room:
                self.room = new_room
                break
