from basicquest.game import Game
from basicquest.gamemap import GameMap
import re
from flask import Flask, render_template, jsonify
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter


@app.route('/')
def index():
    params = {
        'num_gems': app.game.target_gem_count,
        'current_room': app.game.player.room,
        'directions': app.game.map.directions,
        'num_gems': app.game.player.gems,
    }
    return render_template('index.html', **params)


@app.route('/move/<regex("north|south|east|west"):direction>',
           methods=['POST'])
def player_move(direction):
    actions = app.game.tick(direction)
    return jsonify(actions=actions)


if __name__ == '__main__':
    game = Game()
    game.new_game()
    app.game = game

    app.run(debug=True)
