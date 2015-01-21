from collections import deque
from itertools import product
import json
import random

from pprint import pprint


class GameMap(object):
    directions = ['north', 'east', 'south', 'west']

    def __init__(self):
        with open('rooms.json') as f:
            self.rooms = json.load(f)

        for room, connections in self.rooms.iteritems():
            for direction in self.directions:
                if direction not in connections:
                    connections[direction] = None

        self.target = random.choice(self.rooms.keys())

        self.find_shortest_paths()

    def __getitem__(self, index):
        return self.rooms[index]

    def move(self, current, direction):
        return self.rooms[current][direction]

    def random_room(self, exclude=None):
        return random.choice([r for r in self.rooms.keys() if r != exclude])

    def is_target(self, room):
        return room == self.target

    def random_direction(self):
        random.shuffle(self.directions)
        for direction in self.directions:
            yield direction

    def find_shortest_paths(self):
        """Pre-calculate the direction Grue needs to move to a target room"""
        paths = {
            from_room: {
                to_room: None
                for to_room in self.rooms
                if from_room != to_room
            }
            for from_room in self.rooms
        }

        queue = deque()
        rooms = self.rooms

        # For each room mark all the adjucent rooms and queue them up
        for room, direction in product(self.rooms, self.directions):
            adj_room = rooms[room][direction]
            if adj_room:
                paths[room][adj_room] = direction
                queue.append((adj_room, room, direction))

        while queue:
            name, origin, origin_dir = queue.popleft()
            room = rooms[name]

            for direction in self.directions:
                if room[direction]:
                    target = room[direction]

                    if target == origin:
                        continue

                    if not paths[origin][target]:
                        paths[origin][target] = origin_dir
                        queue.append((target, origin, origin_dir))

        self.shortest_paths = paths


if __name__ == '__main__':
    m = GameMap()
    pprint(m.shortest_paths)
