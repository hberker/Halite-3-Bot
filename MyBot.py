#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

from hlt import Position
# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

#Gets ships best move
def getShipMove(ship,sy):
    bestSpot = []
    best = 0
    amount = 820

    if game_map[game_map.normalize(ship.position)].halite_amount < constants.MAX_HALITE / 37 and (ship.halite_amount < amount ):
        for i in Direction.get_all_cardinals():
            if(game_map[ship.position.directional_offset(i)].is_occupied == False):
                bestSpot.append(game_map[ship.position.directional_offset(i)])

        for i in bestSpot:
            if(i.halite_amount > best):
                
                    #bestDir = game_map.naive_navigate(ship, i.position)
                    best = i.halite_amount
                    bestDir = game_map.get_unsafe_moves(ship.position, i.position)[0]
        
        if best < 50:
            bestDir = Direction.convertStr(random.choice(["n", "s","e","w"]))
        place = game_map[ship.position.directional_offset((bestDir))].position
        inPicked = False
        for i in placepicked:
            if (i.__eq__(place)):
                inPicked = True
        if inPicked == False and game_map[ship.position.directional_offset(bestDir)].is_occupied == False:
            placepicked.append(ship.position.directional_offset(bestDir))
            command_queue.append((ship.move(bestDir)))
        else:
            placepicked.append(ship.position)

            command_queue.append(ship.stay_still())

        #returnCommand = (ship.move(bestDir))
    else:
        if ship.is_full or ship.halite_amount > amount:
            #command_queue.append(game_map.get_unsafe_moves(ship.position, Shipyard)[0])
            placeVal = game_map[ship.position.directional_offset(game_map.get_unsafe_moves(ship.position, Shipyard)[0])].position
            inPicked = False
            for e in placepicked:
                if (placeVal.__eq__(e)):
                    inPicked = True

            if inPicked == True:
                command_queue.append(ship.stay_still())
                placepicked.append(ship.position)
            else:
                command_queue.append(ship.move(game_map.naive_navigate(ship, Shipyard)))
                placepicked.append(placeVal) 
        else:
            command_queue.append(ship.stay_still())
            placepicked.append(ship.position)


    #game_map[ship.position].mark_unsafe(ship)




Shipyard = Position(8, 16)

""" <<<Game Loop>>> """
while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map
    
    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    placepicked = []
    placepicked.clear()
    
    for ship in me.get_ships():
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        
        if game.turn_number == 2 or game.turn_number == 1 :
            Shipyard = ship.position
        #command_queue.append(getShipMove(ship))
        getShipMove(ship, Shipyard)
    #for i in placepicked:
        #print("picked: " + str(i) +"\n")
    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if (game.turn_number <= 100 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied):
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

