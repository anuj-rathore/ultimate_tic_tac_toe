import sys
import random
import signal
import random
import copy
import collections
from time import time

infinity = 10000000
MAX_DEPTH = 3  

class Player2(object):
    def __init__(self):
        # count_moves = 0
        pass

    def move(self, current_board_game, board_stat, move_by_opponent, flag):
        '''Return tuple of next move (row, column).Check if next move is valid or not'''

        # temp_board = current_board_game[:]
        # temp_block = board_stat[:]
        temp_board = copy.deepcopy(current_board_game)
        temp_block = copy.deepcopy(board_stat)
        old_move = move_by_opponent
        own_flag = flag
        print own_flag
        print "Total depth checked  : ",MAX_DEPTH

        count_moves = 0

        for i in range(9):
            for j in range(9):
                if temp_board[i][j] != '-':
                    count_moves +=1


        if count_moves == 0:
            return (4,4)
        else:
            move = self.alphabeta_search(temp_board, temp_block, old_move, own_flag)
        
        # self.count_moves +=1
        return move
       

    def alphabeta_search(self, state, block, old_move,own_flag):
        
        def max_value(cell, state, block, given_flag, alpha, beta, depth):
            v = -1*infinity
            old_move = cell
            new_state = copy.deepcopy(state)
            # new_block = block[:]
            new_block = copy.deepcopy(block)

            # we made the move that EARLIER ONE WAS SUPPOSED TO MAKE
            self.update_lists(new_state, new_block, cell,given_flag)

            if self.cutoff_test(cell,new_state,new_block,depth):
                return self.eval_fn(cell, new_state,block,own_flag)
            
            list_of_moves = self.get_allowed_moves(new_state, new_block,old_move,self.other_flag(given_flag))


            for a in list_of_moves:
                v = max(v, min_value(a, new_state, new_block, self.other_flag(given_flag),alpha, beta, depth+1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v            


        def min_value(cell, state, block, given_flag, alpha, beta, depth):
                 
            v = infinity
            old_move = cell
            new_state = copy.deepcopy(state)
            # new_block = block[:]
            new_block = copy.deepcopy(block)
            
            # we made the move that EARLIER ONE WAS SUPPOSED TO MAKE
            self.update_lists(new_state, new_block, cell,given_flag)
            # here , the game board is updated with earliers move
            # NOW BEGIN WITH MIN-Function
            if self.cutoff_test(cell,new_state,new_block,depth):
                 return self.eval_fn(cell, new_state,block,own_flag)

            # now which moves this MIN can make
            list_of_moves = self.get_allowed_moves(new_state, new_block,old_move,self.other_flag(given_flag))
            for a in list_of_moves:
                v = min(v, max_value(a, new_state, new_block, self.other_flag(given_flag),alpha, beta, depth+1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v
        

        list_of_moves = self.get_allowed_moves(state, block, old_move, own_flag)
        maximum_return_value= -1*infinity

        for i in list_of_moves:
            value=min_value( i , state, block , own_flag,-infinity, infinity, 0) # pass own flag to MIN
            # print "value",value
            if value>=maximum_return_value:
                maximum_return_value=value
                candidate_tuple=i
                # print "under_if",value
        
        return candidate_tuple


    def get_allowed_moves(self, temp_board, temp_block, old_move, flag):
        # return all possible TUPLEs (as a list) that we can make in temp_board
        blocks_allowed = []
        if old_move[0]==-1 and old_move[1]==-1: ## SUPPOSE WE ARE FIRST TO MOVE
            blocks_allowed=[4]
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
            blocks_allowed = [1,3]
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
            blocks_allowed = [1,5]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
            blocks_allowed = [3,7]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
            blocks_allowed = [5,7]
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
            blocks_allowed = [0,2]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
            blocks_allowed = [0,6]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
            blocks_allowed = [6,8]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
            blocks_allowed = [2,8]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
            blocks_allowed = [4]
        else:
            sys.exit(1)

        final_blocks_allowed = []
        for i in blocks_allowed:
            if temp_block[i] == '-':
                final_blocks_allowed.append(i)

        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = self.get_cells(temp_board, final_blocks_allowed, temp_block)
        return cells

    def get_cells(self, gameb, blal, block_stat):


        '''Gets empty cells from the list of possible blocks. Hence gets valid moves.'''
        cells = []  # it will be list of tuples
        #Iterate over possible blocks and get empty cells
        for idb in blal:
            id1 = idb/3
            id2 = idb%3
            for i in range(id1*3,id1*3+3):
                for j in range(id2*3,id2*3+3):
                    if gameb[i][j] == '-':
                        cells.append((i,j))

        # If all the possible blocks are full, you can move anywhere
        if cells == []:
            for i in range(9):
                for j in range(9):
                    no = (i/3)*3
                    no += (j/3)
                    if gameb[i][j] == '-' and block_stat[no] == '-':
                        cells.append((i,j)) 
        return cells

    def terminal_state_reached(self, game_board, bs):
        '''Checks whether end is reached'''
        #Check if game is won!
        ## Row win
        if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
            # print block_stat
            return True
        ## Col win
        elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
            # print block_stat
            return True
        ## Diag win
        elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
            # print block_stat
            return True
        else:
            smfl = 0
            for i in range(9):
                for j in range(9):
                    if game_board[i][j] == '-' and bs[(i/3)*3+(j/3)] == '-':
                        return False
            return True

    def update_lists(self, game_board, block_stat, move_ret, fl):
        #move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
        game_board[move_ret[0]][move_ret[1]] = fl

        block_no = (move_ret[0]/3)*3 + move_ret[1]/3
        id1 = block_no/3
        id2 = block_no%3
        mg = 0
        mflg = 0
        if block_stat[block_no] == '-':
            if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
                mflg=1
            if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
                mflg=1
            
            if mflg != 1:
                for i in range(id2*3,id2*3+3):
                    if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                        mflg = 1
                        break

                    ### row-wise
            if mflg != 1:
                for i in range(id1*3,id1*3+3):
                    if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                        mflg = 1
                        break

        
        if mflg == 1:
            block_stat[block_no] = fl
        
        #check for draw on the block.

        id1 = block_no/3
        id2 = block_no%3
        cells = []
        for i in range(id1*3,id1*3+3):
            for j in range(id2*3,id2*3+3):
                if game_board[i][j] == '-':
                    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        
        return


    def cutoff_test(self,cell,state,block,depth):
        if(depth>MAX_DEPTH):
            return 1
        else:
            return 0

    def other_flag(self, flag):
        if flag == 'x':
            return 'o'
        else:
            return 'x'

    def eval_fn(self,cell, board, block,own_flag):
        xs = (cell[0]/3) * 3
        xl = xs +3
        ys = (cell[1]/3) * 3 
        yl = ys + 3
        value = 0

        co = []
        flag = board[cell[0]][cell[1]]

        if own_flag == 'x':
            opp_flag = 'o'
        else:
            opp_flag ='x'
        # print "own_flag", own_flag
        
        game = []
        for i in range (xs,xs+3):
            for j in range (ys,ys+3):
                game.append(board[i][j])
        
        #GAME WINS CONDITIONS

        #dealing the columns
        if (game[0] == game[3] and game[3]== game[6]):
            if game[0] == own_flag:
                value = 100
            elif game[0] == opp_flag:
                value = -100
            else:
                pass

        if game[1] == game[4] and game[4]== game[7]:
            if game[1] == own_flag:
                value = 100
            elif game[1] == opp_flag:
                value = -100
            else:
                pass

        if game[2] == game[5] and game[5]== game[8]:
            if game[2] == own_flag:
                value =  100
            elif game[2] == opp_flag:
                value = -100
            else:
                pass


        # dealing the diagonals
        if game[0] == game [4] and game[4] == game[8]:
            if game[0] == own_flag:
                value = 100
            elif game[0] == opp_flag:
                value = -100
            else:
                pass

        if game[6] == game[4] and game[4] == game[2]:
            if game[2] == own_flag:
                value = 100
            elif game[2] == opp_flag:
                value = -100
            else:
                pass



        # dealing the rows
        if (game[0] == game[1] and game[1]== game[2]):
            if game[0] == own_flag:
                value = 100
            elif game[0] == opp_flag:
                value = -100
            else:
                pass

        if game[3] == game[4] and game[4]== game[5]:
            if game[3] == own_flag:
                value = 100
            elif game[3] == opp_flag:
                value = -100
            else:
                pass

        if game[6] == game[7] and game[7]== game[8]:
            if game[6] == own_flag:
                value = 100
            elif game[6] == opp_flag:
                value =-100
            else:
                pass

        #stopping opponent
        #what if, 2 ooponent and 1 own
        # what if 2 own and 1 opp in a row or col    
        

        #now deal the conditions when xx_ or x_x or _xx

        #upper row
        a = game[0] + game[1] + game[2]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 10
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value =-10
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 20
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -20

        #middle row
        a = game[3] + game[4] + game[5]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 10
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value =-10
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 20
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value =-20

        #bottom row
        a = game[6] + game[7] + game[8]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 10
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value =-10
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 20
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value =-20

        #left column
        a = game[0] + game[3] + game[6]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 10
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value =-10
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value =  20
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -20

        #middle column
        a = game[1] + game[4] + game[7]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 10
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value = -10
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 20
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -20

        #right column
        a = game[2] + game[5] + game[8]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 10
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value = -10
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 20
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -20

        # handle the diagonals
        a = game[0] + game[4] + game[8]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 10
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value = -10
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 20
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -20

        a = game[2] + game[4] + game[6]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 10
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value = -10
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 20
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -20


        if own_flag == board[cell[0]][cell[1]]:
            value = 1

        if opp_flag == board[cell[0]][cell[1]]:
            value = -1


        # Deal the final block
                #dealing the columns
        if (block[0] == block[3] and block[3]== block[6]):
            if block[0] == own_flag:
                value = 500
            elif block[0] == opp_flag:
                value = -500
            else:
                pass

        if block[1] == block[4] and block[4]== block[7]:
            if block[1] == own_flag:
                value = 500
            elif block[1] == opp_flag:
                value = -500
            else:
                pass

        if block[2] == block[5] and block[5]== block[8]:
            if block[2] == own_flag:
                value =  500
            elif block[2] == opp_flag:
                value = -500
            else:
                pass


        # dealing the diagonals
        if block[0] == block [4] and block[4] == block[8]:
            if block[0] == own_flag:
                value = 500
            elif block[0] == opp_flag:
                value = -500
            else:
                pass

        if block[6] == block[4] and block[4] == block[2]:
            if block[2] == own_flag:
                value = 500
            elif block[2] == opp_flag:
                value = -500
            else:
                pass



        # dealing the rows
        if (block[0] == block[1] and block[1]== block[2]):
            if block[0] == own_flag:
                value = 500
            elif block[0] == opp_flag:
                value = -500
            else:
                pass

        if block[3] == block[4] and block[4]== block[5]:
            if block[3] == own_flag:
                value = 500
            elif block[3] == opp_flag:
                value = -500
            else:
                pass

        if block[6] == block[7] and block[7]== block[8]:
            if block[6] == own_flag:
                value = 500
            elif block[6] == opp_flag:
                value =-500
            else:
                pass

        #stopping opponent
        #what if, 2 ooponent and 1 own
        # what if 2 own and 1 opp in a row or col    
        

        #now deal the conditions when xx_ or x_x or _xx

        #upper row
        a = block[0] + block[1] + block[2]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 50
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value =-50
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 100
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -100

        #middle row
        a = block[3] + block[4] + block[5]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 50
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value =-50
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 100
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value =-100

        #bottom row
        a = block[6] + block[7] + block[8]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 50
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value =-50
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 100
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value =-100

        #left column
        a = block[0] + block[3] + block[6]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 50
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value =-50
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value =  100
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -100

        #middle column
        a = block[1] + block[4] + block[7]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 50
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value = -50
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 100
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -100

        #right column
        a = block[2] + block[5] + block[8]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 50
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value = -50
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 100
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -100

        # handle the diagonals
        a = block[0] + block[4] + block[8]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 50
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value = -50
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 100
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -100

        a = block[2] + block[4] + block[6]
        dic = collections.Counter(a)
        if (dic[own_flag] == 2 and dic['-'] == 1):
            value = 50
        if dic[opp_flag] == 2 and dic ['-'] == 1 :
            value = -50
        if dic[opp_flag] == 2 and dic [own_flag] == 1 :
            value = 100
        if dic[own_flag] == 2 and dic [opp_flag] == 1 :
            value = -100


        # if own_flag == block[cell[0]][cell[1]]:
        #     value = 20

        # if opp_flag == block[cell[0]][cell[1]]:
        #     value = -20


        return value