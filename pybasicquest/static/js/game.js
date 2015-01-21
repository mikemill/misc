$(function() {
    var room_field = $('#current_room');
    var gem_field = $('#num_gems');
    var log_field = $('#log');

    console.log(room_field);
    console.log(gem_field);

    var action_mapping = {
        'player_move': print_action_player_move,
        'gem': print_action_gem,
        'won': print_action_won,
        'rest': print_action_rest,
        'killed': print_action_killed
    };

    $("#move_direction button").click(function() {
        var direction = $(this).data('direction');

        $.post('/move/' + direction, function(data) {
            var len = data.actions.length;
            for (var i=0; i < len; i++) {
                var action = data.actions[i];
                action_mapping[action.action](action);
            }
        });
        return false;
    });

    function print_action_player_move(action) {
        var msg = "You move to the " + action.direction + " door and pull the handle ";

        if (action.success) {
            msg += "and step into the " + action.room + " room.";
            set_room(action.room);
        } else {
            msg += "but it doesn't open.";
        }

        add_log(msg);

        if (action.target) {
            add_log("There is a glowing dias in the center of the room.");
        }
    }

    function print_action_gem(action) {
        add_log("As you step into the room you find a gem!");
        add_log("You now have " + action.gem_count + " gems.");

        if (action.goal_reached) {
            add_log("You have enough gems to leave.  You should find the dias");
        }

        set_gems(action.gem_count);
    }

    function print_action_won(action) {
        add_log("You put the gems in the dias and safely teleport away.");
    }

    function print_action_rest(action) {
        add_log("You are tired and need to rest.");
    }

    function print_action_killed(action) {
        add_log("The Grue has found and killed you!  You lost all your gems.");
        add_log("You revive in the " + action.room + " room.");
        set_room(action.room);
        set_gems(0);
    }

    function add_log(str) {
        log_field.append(str + "\n");
        log_field.scrollTop(log_field[0].scrollHeight - log_field.height());
    }

    function set_room(room) {
        console.log("set_room to: " + room);
        room_field.text(room);
    }

    function set_gems(gems) {
        console.log("set_gems to: " + gems);
        gem_field.text(gems);
    }
});
