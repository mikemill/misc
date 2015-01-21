from gamemap import GameMap
from player import Player
from grue import Grue


class Game(object):
    target_gem_count = 5

    def __init__(self):
        self.map = GameMap()
        self.player = None
        self.grue = None
        self.turn = 0

    def new_game(self):
        self.player = Player(self.map)
        self.grue = Grue(self.map, self.player)
        self.turn = 0

    def tick(self, player_direction):
        actions = []

        new_room = self.player.move(player_direction)
        actions.append({
            'action': 'player_move',
            'success': new_room is not None,
            'room': new_room,
            'target': self.map.is_target(self.player.room),
            'direction': player_direction,
        })

        if self.player.room == self.grue.room:
            self.grue.flee()
            self.player.gems += 1
            actions.append({
                'action': 'gem',
                'gem_count': self.player.gems,
                'goal_reached': self.player.gems == self.target_gem_count,
                'room': self.grue.room,
            })

        self.turn += 1

        if self.won():
            actions.append({
                'action': 'won',
            })
        elif self.turn == 3:
            self.turn = 0
            actions.append({
                'action': 'rest',
            })

            self.grue.move()

            if self.grue.room == self.player.room:
                self.player.killed()
                actions.append({
                    'action': 'killed',
                    'room': self.player.room,
                })

        return actions

    def won(self):
        return (self.map.is_target(self.player.room)
                and self.player.gems == self.target_gem_count)
