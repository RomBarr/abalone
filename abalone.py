
#Created by: Roman Barron
#Created date: 12/4/2022
#Version = 1.0
#-------------------------------------------------------------------------------------------
"""
 This class is an implementation of a subclass to Problem, with methods for actions and results
 to be used in conjuction with the search functions. Class Problem and the search functions
 are imported from the Search.py file, a public github repository.
"""
#---------------------------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------------------------
from games import *
import numpy as np
import copy

#---------------------------------------------------------------------------------------------
# Helper Functions
#---------------------------------------------------------------------------------------------

def valid_rq (r,q):
    if r >= -4 and r <= 4:
                if r >= 0:
                    if q >= -4 and q <= 4 - r:
                        return True
                if r < 0:
                    if q >= -4 + abs(r) and q <= 4:
                        return True
    return False

def neighborCoordinates(pair):
        """
        Returns list of coordinates of the neighbor hex spaces
        """
        axial_direction = [
            (1, 0), # downright
            (1, -1), # downleft
            (0, -1), # left
            (-1, 0), # upleft
            (-1, 1), # upright
            (0, 1)  # right
            ]
        neighborList = []
        direction = []
        for x in axial_direction:
            r, q = (pair[0] + x[0], pair[1] + x[1])
            if valid_rq(r,q):
                neighborList.append((r,q))
                direction.append(x)
          
        return neighborList, direction

def group_move_validation( tbl, pos, drct, player, sizeP, sizeO ):
    if sizeP <= 3:
        r, q = (pos[0] + drct[0], pos[1] + drct[1])
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        if valid_rq(r,q):
            if r in tbl[player]:
                if (r,q) in tbl[player][r]:
                    sizeP += 1
                    return group_move_validation(tbl, (r,q), drct, player, sizeP, sizeO)
                elif r in tbl[opponent]:
                    if (r,q) in tbl[opponent][r]:
                        sizeO += 1
                        if sizeO >= sizeP:  
                            return False
                        else:
                            return group_move_validation(tbl, (r,q), drct, player, sizeP, sizeO)
                    else:
                        return True
                else:
                    return True
            elif r in tbl[opponent]:
                if (r,q) in tbl[opponent][r]:
                    sizeO += 1
                    if sizeO >= sizeP:  
                        return False
                    else:
                        return group_move_validation(tbl, (r,q), drct, player, sizeP, sizeO)
            else:
                return True
        else:
            if (sizeP > sizeO and sizeO != 0): return True
            else: return False
    else: return False

def valid_moves( state, posOfMarble, player):
        v_moves = []
        neighbors, direction = neighborCoordinates(posOfMarble)
        tbl = state
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        ind = 0
        for n in neighbors:
            key = n[0]
            if key in tbl[player]:
                if n in tbl[player][key]:
                    #valid_check recursion? two marbles of same color. check if possible to move
                    b = group_move_validation(tbl, n, direction[ind], player, 2, 0)
                    if b:
                        v_moves.append(direction[ind])
                elif key in tbl[opponent]:
                    if n not in tbl[opponent][key]:
                        v_moves.append(direction[ind])
                else:
                    v_moves.append(direction[ind])
            elif key in tbl[opponent]:
                    if n not in tbl[opponent][key]:
                        v_moves.append(direction[ind])
            else:
                v_moves.append(direction[ind])

            ind += 1
                

        return v_moves

def initiate_move(tbl, move, player, opponent):

    try:
        currentPos = move[0]
        current_r = currentPos[0]
        current_q = currentPos[1]
        direction = move[1]
        new_r = current_r + direction[0]
        new_q = current_q + direction[1]
        nextPos = (new_r, new_q)

        inside_board = valid_rq(new_r, new_q)

        if inside_board:
            if nextPos in tbl[player][new_r]:
                tbl = initiate_move(tbl,(nextPos, direction),player,opponent)
            elif nextPos in tbl[opponent][new_r]:
                tbl = initiate_move(tbl,(nextPos, direction),opponent,player)

            tbl[player][current_r].remove(currentPos)
            tbl[player][new_r].append(nextPos)
        else:
            tbl[player][current_r].remove(currentPos)
    except ValueError:
        print("Not a valid move...")

    return tbl

#def initiate_move(tbl, move, player, opponent):
    
#    if move[0] not in tbl[player][move[0][0]]:
#        return tbl

#    r, q = move[0]
#    x, y = move[1]
#    new_r = r + x
#    new_q = q + y

#    inside_board = valid_rq(new_r,new_q)
#    if inside_board:

#        p = new_r in tbl[player]
#        o = new_r in tbl[opponent]

#        if not p and not o:
#            tbl[player].setdefault(new_r, [])
#            tbl[player][new_r].append((new_r, new_q))
#            tbl[player][r].remove(move[0])
    
#        elif p:
#            if (new_r, new_q) in tbl[player][new_r]:
#                tbl = initiate_move(tbl,((new_r,new_q),(x,y)), player, opponent)
#                tbl[player][r].remove(move[0])
#                tbl[player][new_r].append((new_r,new_q))
#            elif o:
#                if (new_r, new_q) in tbl[opponent][new_r]:
#                    tbl = initiate_move(tbl,((new_r,new_q),(x,y)), opponent, player)
#                    tbl[opponent][r].remove(move[0])
#                    tbl[player][new_r].append((new_r,new_q))
#                else:
#                    tbl[player][new_r].append((new_r,new_q))
#                    tbl[player][r].remove(move[0])
#            else:
#                tbl[player][new_r].append((new_r, new_q))
#                tbl[player][r].remove(move[0])
#        elif o:
#            if (new_r, new_q) in tbl[opponent][new_r]:
#                tbl = initiate_move(tbl,((new_r,new_q),(x,y)), opponent, player)
#                #tbl[opponent][r].remove(move[0])
#                #tbl[player][new_r].append((new_r,new_q))
#            else:
#                tbl[player][new_r].append((new_r,new_q))
#                tbl[player][r].remove(move[0])

#    else:
#        tbl[player][r].remove(move[0])
#    return tbl

#---------------------------------------------------------------------------------------------
# Classes & Functions
#---------------------------------------------------------------------------------------------

class abalone_game(Game):

    def __init__(self):
        """
        Default Constructor sets current state of the board.
        MAX represents player White; MIN represents player Black.
        """
        super().__init__()

        """
        Board state represented as an axial grid (r,q). 
        r index is horizontal spaces, q diagonal spaces.
        Game of Abalone hex grid has a size of 5 for each side. 
        (min,max)q = (-4,4) ; (min,max)r = (-4,4). When representing the state
        of the board, we only need to include the spaces that are occupied
        with White and Black pieces. The default initial state of Abalone
        is represented as the array in this function. ( (r, q), player )
        MAX = player white = 0, MIN = player black = 1. 
        """
        startBoard = [
                ((-4,0),1), ((-4,1),1), ((-4,2),1), ((-4,3),1), ((-4,4),1),
            ((-3,-1),1), ((-3,0),1), ((-3,1),1), ((-3,2),1), ((-3,3),1), ((-3,4), 1),
                            ((-2,0),1), ((-2,1),1), ((-2,2),1),

                            ((2,-2),0), ((2,-1),0), ((2,0),0),
             ((3,-4),0), ((3,-3),0), ((3,-2),0), ((3,-1),0), ((3,0),0), ((3,1), 0),
                ((4,-4),0), ((4,-3),0), ((4,-2),0), ((4,-1),0), ((4,0),0)
            ]

        #create hashtable; white = 1, black = 0
        tbl = {"BLACK": {}, "WHITE": {}}

        for x in range(-4, 5):
             tbl["WHITE"].setdefault(x, [])
             tbl["BLACK"].setdefault(x, [])
        
        for pos in startBoard:
            key = pos[0][0]
            if pos[1] == 1:
                tbl["WHITE"].setdefault(key, [])
                tbl["WHITE"][key].append(pos[0])
            else:
                tbl["BLACK"].setdefault(key, [])
                tbl["BLACK"][key].append(pos[0])


        #all marbles share a general pattern move set (currentX, currentY) + (moveX,moveY)
        p_moves =  {"BLACK": {}, "WHITE": {}}
        for key in tbl["BLACK"]:
            for posOfMarble in tbl["BLACK"][key]:
                p_moves["BLACK"].setdefault(posOfMarble, [])
                p_moves["BLACK"][posOfMarble].extend(valid_moves(tbl, posOfMarble, "BLACK"))

        for key in tbl["WHITE"]:
            for posOfMarble in tbl["WHITE"][key]:
                p_moves["WHITE"].setdefault(posOfMarble, [])
                p_moves["WHITE"][posOfMarble].extend(valid_moves(tbl, posOfMarble, "WHITE"))


        self.initial = GameState(to_move="WHITE", utility=0, board=tbl, moves=p_moves)

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        currentState = copy.deepcopy(state)
        player = currentState.to_move
        opponent = "WHITE" if player == "BLACK" else "BLACK"
        brd = currentState.board
        tbl = initiate_move(brd, move, player, opponent)
        p_moves =  {"BLACK": {}, "WHITE": {}}
        for key in tbl["BLACK"]:
            for posOfMarble in tbl["BLACK"][key]:
                p_moves["BLACK"].setdefault(posOfMarble, [])
                p_moves["BLACK"][posOfMarble].extend(valid_moves(tbl, posOfMarble, "BLACK"))

        for key in tbl["WHITE"]:
            for posOfMarble in tbl["WHITE"][key]:
                p_moves["WHITE"].setdefault(posOfMarble, [])
                p_moves["WHITE"][posOfMarble].extend(valid_moves(tbl, posOfMarble, "WHITE"))
        
        """
        determines utility.
        If MAX wins with this move then util = +1, if Min wins then util = -1
        else return 0.
        """
        util = 0
        w = {key: len(value) for key, value in tbl["WHITE"].items()}
        length_dict_w = sum(w.values())
        b = {key: len(value) for key, value in tbl["BLACK"].items()}
        length_dict_b = sum(b.values())
        if length_dict_w < 9:
            util = -1
        elif length_dict_b < 9:
            util = 1
        else:
            util = 0

        currentState = GameState(to_move=opponent, utility=util, board=tbl, moves=p_moves)
        return currentState
        

    def actions(self, state):
        """ Return the actions that can be excecuted in given state. """
        player = state.to_move
        actList = []
        for key in state.moves[player]:
            for action in state.moves[player][key]:
                actList.append((key, action))
        return actList

        
    def terminal_test(self, state):
        """Returns true if the given state represents end game"""
        tbl = state.board
        w = {key: len(value) for key, value in tbl["WHITE"].items()}
        length_dict_w = sum(w.values())
        b = {key: len(value) for key, value in tbl["BLACK"].items()}
        length_dict_b = sum(b.values())
        if length_dict_w < 9:
            return 1
        if length_dict_b < 9:
            return 1
        return 0

    def utility(self, state, player):
        """Returns +1 if WHITE wins, -1 if BLACK wins """
        return state.utility if player == "WHITE" else -state.utility

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    