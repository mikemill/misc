class Player(object):
    def __init__(self, game_map):
        self.room = None
        self.game_map = game_map
        self.gems = 0

        self.spawn()

    def move(self, direction):
        new_room = self.game_map.move(self.room, direction)
        if new_room:
            self.room = new_room

        return new_room

    def spawn(self):
        self.room = self.game_map.random_room(self.room)
        return self.room

    def killed(self):
        self.gems = 0
        self.spawn()
