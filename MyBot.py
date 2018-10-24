#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

from hlt import Position
# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction
from hlt.positionals import commands
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
# get high halite areas
def getTargetAreas(ship, targetArea):
    for places in ship.position.get_surrounding_cardinals():
        if game_map[places].halite_amount > 100 and not places.__eq__(Shipyard):
            targetArea.append(game_map[places].position)
    if len(targetArea) > 0: 
        cleanPlaces(targetArea)

def getClosestSpot(ship):
    possible = []
    cleanPlaces(targetArea)
    for i in targetArea:   
        if i != ship.position:
            pickDir = game_map.get_unsafe_moves(ship.position, i)[0]
            if ((pickDir).__ne__(Direction.Still) ) and (ship.position.__ne__(i)) and game_map[i].halite_amount > 100:
                possible.append(i)
    
    if len(possible) > 0:
        closest = possible[0]
        for i in possible:
            if game_map.calculate_distance(ship.position, i) < game_map.calculate_distance(ship.position, closest):   
                if  game_map.get_unsafe_moves(ship.position, i)[0] != Direction.Still:
                    closest = i
        
        return  Direction.convert(game_map.get_unsafe_moves(ship.position, closest)[0])
    else:
        for i in Direction.get_all_cardinals():
            if(game_map[ship.position.directional_offset(i)].is_occupied == False):
                return Direction.convert(game_map.get_unsafe_moves(ship.position, ship.position.directional_offset(i))[0])
        

def cleanPlaces(targetArea):
    index = 0
    temp = []
    for place in targetArea:
        
        if game_map[place].halite_amount > 50 and  game_map[place].is_occupied == False:
            try:
                if place not in temp:
                    temp.append(place)
            except ValueError:
                pass
            index += 1
    targetArea = temp
#Gets ships best move
def getShipMove(ship,sy):
    cleanPlaces(targetArea)
    bestSpot = []
    best = 0
    amount = 820
    options = 0
    if ship.position == Shipyard:
        openSpot = False
        for i in Direction.get_all_cardinals():
            if(game_map[ship.position.directional_offset(i)].is_occupied == False):
                openSpot = True

        if openSpot == False:
            bestDir = Direction.North
            placepicked.append(ship.position.directional_offset(bestDir))
            command_queue.append(ship.move(bestDir))
            return 0


    #< constants.MAX_HALITE / 35
    if (game_map[ship.position].halite_amount == 0 and (ship.halite_amount < amount )) or (Shipyard.__eq__(ship.position)):
        #print("WOOOOOOLK")
        for i in Direction.get_all_cardinals():
            if(game_map[ship.position.directional_offset(i)].is_occupied == False):
                bestSpot.append(game_map[ship.position.directional_offset(i)])
                options +=1
        for i in bestSpot:
            if(i.halite_amount >= best):
                    #bestDir = game_map.naive_navigate(ship, i.position)
                    best = i.halite_amount
                    bestDir = game_map.get_unsafe_moves(ship.position, i.position)[0]
        if  best < 100 :
            if len(targetArea) == 0 :
                pos = []
                for i in Direction.get_all_cardinals():
                    found = False
                    if(game_map[ship.position.directional_offset(i)].is_occupied == False and game_map[ship.position.directional_offset(i)].position.__ne__(game_map[me.shipyard].position)):
                        pos.append(i)
                        #bestDir = (i)
                        found = True
                bestDir = random.choice(pos)
                if found == False:
                    bestDir = (0,0)
                placepicked.append(ship.position.directional_offset(bestDir))
                command_queue.append(ship.move(bestDir))
                return 0
            else:
                
                bestDir = Direction.convertStr(getClosestSpot(ship))
                if game_map[ship.position.directional_offset(bestDir)].is_occupied == False and not game_map[ship.position.directional_offset(bestDir)].position in placepicked:
                    placepicked.append(ship.position.directional_offset(bestDir))
                    command_queue.append(ship.move(bestDir))
                    return 0
                bestDir = (0,0)

        place = game_map[ship.position.directional_offset((bestDir))].position
        inPicked = False
        for i in placepicked:
            if (i.__eq__(place)):
                inPicked = True
        if inPicked == False and game_map[ship.position.directional_offset(bestDir)].is_occupied == False:
            placepicked.append(ship.position.directional_offset(bestDir))
            command_queue.append((ship.move(bestDir))) 
            return 0
        else:
            isFound = False
            bestDir = (0,0)
            for i in Direction.get_all_cardinals():
                if(game_map[ship.position.directional_offset(i)].is_occupied == False) and ((game_map[ship.position.directional_offset(i)].position in placepicked) == False):
                    bestDir = (game_map.get_unsafe_moves(ship.position, ship.position.directional_offset(i))[0])
                    isFound = True
                    placepicked.append(ship.position.directional_offset(bestDir))
                    command_queue.append(ship.move(bestDir))
                    return 0

            if isFound == False:
                command_queue.append(ship.stay_still())
                placepicked.append(ship.position)
                return 0

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
                isFound = False
                bestDir = (0,0)
                for i in Direction.get_all_cardinals():
                    if(game_map[ship.position.directional_offset(i)].is_occupied == False) and ((game_map[ship.position.directional_offset(i)].position in placepicked) == False):
                        bestDir = (game_map.get_unsafe_moves(ship.position, ship.position.directional_offset(i))[0])
                        isFound = True
                        placepicked.append(ship.position.directional_offset(bestDir))
                        command_queue.append(ship.move(bestDir))
                        return 0
                
                ##command_queue.append(ship.stay_still())
                ##placepicked.append(ship.position)
                ##return 0

            else:
                command_queue.append(ship.move(game_map.naive_navigate(ship, Shipyard)))
                placepicked.append(placeVal) 
                return 0

        else:
            if game_map[ship.position].halite_amount > 0:
                command_queue.append(ship.stay_still())
                placepicked.append(ship.position)
                return 0
            else:
                isFound = False
                bestDir = (0,0)
                for i in Direction.get_all_cardinals():
                    if(game_map[ship.position.directional_offset(i)].is_occupied == False) and ((game_map[ship.position.directional_offset(i)].position in placepicked) == False):
                        bestDir = (game_map.get_unsafe_moves(ship.position, ship.position.directional_offset(i))[0])
                        isFound = True
                placepicked.append(ship.position.directional_offset(bestDir))
                command_queue.append(ship.move(bestDir))
                return 0




    #game_map[ship.position].mark_unsafe(ship)




Shipyard = Position(8, 16)
targetArea = []

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
        getTargetAreas(ship, targetArea)
        if game.turn_number == 2 or game.turn_number == 1 :
            Shipyard = ship.position
        #command_queue.append(getShipMove(ship))
        getShipMove(ship, Shipyard)
    #for i in placepicked:
        #print("picked: " + str(i) +"\n")    230
    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if (len(me.get_ships()) < 20 and game.turn_number < 230 and me.halite_amount >= constants.SHIP_COST * 1.2 and not game_map[me.shipyard].is_occupied) and game_map[me.shipyard].position not in placepicked:
    #if( me.halite_amount >= constants.SHIP_COST() and not game_map[me.shipyard].is_occupied):
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
 
