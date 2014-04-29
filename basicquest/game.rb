#!/usr/bin/env ruby
require 'json'
require 'highline/import'

class Map
    # Map of the rooms and their interconnection

    @@directions = ['north', 'east', 'south', 'west']

    attr_reader :rooms, :target, :shortest_paths

    def initialize
        # Load the rooms from the config file and choose a target
        rooms = JSON.load(File.open('rooms.json'))

        rooms.each do |room, connections|
            @@directions.each do |dir|
                if not connections.key? dir
                    connections[dir] = nil
                end
            end
        end

        @rooms = rooms
        @target = rooms.keys.sample

        findShortPaths
    end

    def move (current_room, direction)
        # Move in a particular direction and return the new room (or nil if unable to move)
        room = @rooms[current_room]
        if room[direction]
            return room[direction]
        else
            return nil
        end
    end

    def randomRoom (exclude=nil)
        # Pick a random room excluding the one the actor is in
        return @rooms.keys.reject{|r| r == exclude}.sample
    end

    def enterRoom (room)
        # Enter a room and display a message about anything special in there
        if room == @target
            puts "There is a glowing dias in the center of the room"
        end
    end

    def directions
        @@directions
    end

    def findShortPaths
        # Pre-calculate the direction Grue needs to move from any room to a target room
        paths = Hash[rooms.keys.collect{|v| [v, {}]}]

        queue = []
        @rooms.each do |name, room|
            @@directions.each do |dir|
                if room[dir]
                    queue.push([room[dir], name, dir])
                    paths[name][room[dir]] = dir
                end
            end
        end

        # This is essentially a breadth-first search
        while queue.length > 0
            name, origin, origin_dir = queue.shift
            room = @rooms[name]

            @@directions.each do |dir|
                if room[dir]
                    target = room[dir]
                    next if target == origin
                    if not paths[origin][target]
                        paths[origin][target] = origin_dir
                        queue.push([target, origin,  origin_dir])
                    end
                end
            end
        end

        @shortest_paths = paths
    end
end

class Player
    attr_reader :room
    attr_accessor :gems

    def initialize (map)
        @map = map
        @gems = 0
        @room = nil
        spawn
    end

    def spawn
        # Spawn the player in a room that they aren't currently in
        @room = @map.randomRoom @room
        print "You have spawned in the ", @room, " room\n"
    end

    def move (direction)
        new_room = @map.move(@room, direction)
        if new_room
            @room = new_room
            print "You open the door and step into the ", new_room, " room\n"
            @map.enterRoom @room
        else
            puts "You try to step through but the door won't open"
        end
    end
end

class Grue
    attr_reader :room

    def initialize (map, player)
        @map = map
        @player = player
        spawn player
    end

    def spawn (player)
        # Based on the player's position spawn Grue in the far away room
        @room = @map.rooms[player.room]['spawn']
    end

    def move
        # Grue always takes the shortest path.
        direction = @map.shortest_paths[@room][@player.room]
        @room = @map.move @room, direction
    end

    def flee
        # The player found Grue and now Grue must flee to a random room
        room = @map.rooms[@room]

        @map.directions.shuffle.each do |direction|
            if room[direction]
                @room = @map.move @room, direction
                break
            end
        end
    end
end

class Game
    TARGET_GEM_COUNT = 5
    def play
        puts "Welcome to BasicQuest!"
        puts "Your goal is to collect %d gems and then find the teleporter" % TARGET_GEM_COUNT
        puts "Watch out for the Grue!"

        map = Map.new
        player = Player.new map
        grue = Grue.new map, player

        # Build a regex of allowed inputs for the direction
        directions_regex = map.directions.join('|')
        directions_regex = /#{directions_regex}/i

        # Main logic loop
        loop do
            3.times do
                direction = ask("Direction? ") { |prompt|
                    prompt.validate = directions_regex
                    prompt.responses[:not_valid] = "Direction must be one of " + map.directions.join(' ')
                }

                player.move direction.downcase

                if player.room == grue.room
                    grue.flee
                    player.gems += 1
                    puts "You have found a gem!  You know have %d gems." % player.gems
                    if player.gems == TARGET_GEM_COUNT
                        puts "You have enough gems to leave.  You should find the dias before the Grue finds you!"
                    end
                end

                if player.room == map.target and player.gems == TARGET_GEM_COUNT
                    puts "You put the gems in the dias and safely teleport away"
                    return
                end
            end

            puts "You are tired and need to rest"

            grue.move

            if grue.room == player.room
                puts "The Grue has found and killed you!"
                puts "You lost all your gems"
                player.spawn
                player.gems = 0
            end
        end
    end
end

game = Game.new
game.play
