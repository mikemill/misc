from basicquest.game import Game
from basicquest.gamemap import GameMap
import re


_valid_input = r'|'.join(GameMap.directions)
_directions_regex = re.compile(r'^' + _valid_input + r'$', re.IGNORECASE)


def get_direction():
    while True:
        d = raw_input("\nDirection? ")
        if _directions_regex.match(d):
            return d.lower()
        print("Invalid input")


def print_actions(actions):
    action_methods = {
        'player_move': print_action_player_move,
        'gem': print_action_gem,
        'won': print_action_won,
        'rest': print_action_rest,
        'killed': print_action_killed,
    }

    for action in actions:
        print action_methods[action['action']](action).format(**action)


def print_action_player_move(action):
    msg = "You move to the {direction} door and pull the handle "

    if action['success']:
        msg += "and step into the {room} room."
    else:
        msg += "but it doesn't open."

    if action['target']:
        msg += "\nThere is a glowing dias in the center of the room."

    return msg


def print_action_gem(action):
    msg = ("As you step into the room you find a gem!\nYou now have "
           "{gem_count} gems.")

    if action['goal_reached']:
        msg += "\nYou have enough gems to leave.  You should find the dias"

    return msg


def print_action_won(action):
    return "You put the gems in the dias and safely teleport away"


def print_action_rest(action):
    return "You are tired and need to rest"


def print_action_killed(action):
    msg = "The Grue has found and killed you!  You lost all your gems"
    msg += "\nYou revive in the {room} room"
    return msg


if __name__ == '__main__':
    print "Welcome to BasicQuest!"
    print ("Your goal is to collect %d gems and then find the teleporter" %
           Game.target_gem_count)
    print "Watch out for the Grue!"

    print "Valid directions are: ", ', '.join(GameMap.directions)

    game = Game()
    game.new_game()

    won = False

    print "You are in the {} room".format(game.player.room)

    while not won:
        direction = get_direction()
        actions = game.tick(direction)

        print_actions(actions)

        if game.won():
            break
