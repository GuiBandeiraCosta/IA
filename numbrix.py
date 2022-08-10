# Grupo 61:
# 95586 Guilherme Costa
# 96904 Pedro Severino

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


def average_numbers(num1,num2):
        return int((num1+num2)/2)

def board_distance(pos_number1,pos_number2):
    distance_manhattan =abs(pos_number1[0] -pos_number2[0]) +  abs(pos_number1[1] -pos_number2[1])
    return distance_manhattan
def real_distance(num1,num2):
    return abs(num1-num2)

class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class Board:
    """ Representação interna de um tabuleiro de Numbrix. """    

    def __init__(self,board_setted, board_list,numbers_setted, board_list2, size, amount_setted,low_streak,high_streak):
        """ Representação do tabuleiro. """

        self.board_list = board_list
        self.board_list2 = board_list2
        self.board_setted = board_setted
        self.numbers_setted = numbers_setted
        self.size = size
        self.max = size*size
        self.amount_setted = amount_setted
        self.low_streak = low_streak
        self.high_streak = high_streak
       

    def show(self):
        """ O construtor especifica o estado inicial. """
        return "Board List: " + self.board_list.__str__() + "\nAmount Setted: " + self.amount_setted.__str__()
    
    def __repr__(self):
        string = ""
        
        for i in range(self.size):
            for j in range(self.size):
                
                string += str(self.get_number(i,j))
                string += '\t'
            string = string[:-1] + "\n"
        string = string[:-1] 
        return string    

    def is_setted(self,number):
        return self.board_list2[number-1] != (-1,-1)

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.board_list[row*self.size + col]

    def get_pos(self, number: int):
        """ Devolve o valor da posição no tabuleiro do respetivo número. """
        return self.board_list2[number-1]
    
    def adjacent_vertical_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        if (0 < row):
            above = self.get_number(row-1, col)
        else:
            above = None    

        if (row < self.size-1):
            below = self.get_number(row+1, col)
        else:
            below = None   
        return (above,below)
    
    def adjacent_horizontal_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        if (0 < col):
            left = self.get_number(row, col-1)
        else:
            left = None   
        if (col < self.size-1):
            right = self.get_number(row, col+1)
        else:
            right = None 
        return (left,right)

    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        lst = []
        
        f = open(filename, 'r')
        size = int(f.readline().rstrip())
        lines = f.readlines()
        lst2 = [(-1,-1) for i in range(size*size)]
        f.close()
        amount_setted = 0 
        board_setted = []
        numbers_setted = [False] *(size*size)
        
        for line in lines:
            line = line.rstrip("\n")
            
            row_numbers = line.split("\t")
            
            row_numbers[size-1]
            for c in row_numbers:
                if c.isdigit():
                    lst.append(int(c))
                    if(int(c) != 0):
                        amount_setted += 1  
        
        for i in range(0,size):
            for j in range(0,size):
                if(lst[i*size+j] != 0):
                    numbers_setted[lst[i*size+j]-1] = True
                    board_setted.append(lst[i*size+j])
                    lst2[lst[i*size+j]-1] = (i,j)

        low_streak, high_streak = 0,0
        while (lst2[low_streak+1-1] != (-1,-1)):
            low_streak+=1
        while(lst2[size*size-high_streak-1] != (-1,-1)):
            high_streak+=1

        board_setted.sort()

        return  Board(board_setted,lst,numbers_setted, lst2, size,amount_setted, low_streak, high_streak)
    
    def valid_action(self,row,col,number, size):
        prev = number
        next = number
        while not self.numbers_setted[prev-1]:
            if prev == 1:
                return True
            prev -=1
        while not self.numbers_setted[next-1]:
            if next == size*size:
                return True
            next +=1
        if board_distance((row,col),self.get_pos(prev)) > real_distance(number,prev):
            return False
        if board_distance((row,col),self.get_pos(next)) > real_distance(number,next):
            return False    
        return True
    
    def near_wall(self,row,col):
        if row  == 0 or row == self.size-1 or col == 0 or col  == self.size-1:
            return True
        return False

    def adj_setted(self, number):
        return self.is_setted(number-1) and self.is_setted(number+1)     
    
    def neighbours_nearby(self,number):
        if(number == 1):
            pos_number1 = self.get_pos(number+1)
            distance_1 = board_distance(pos_number,pos_number1)
            if distance_1 ==1:
                return True
            return False
        if(number == self.max):
            pos_number0 = self.get_pos(number-1)
            distance_0 = board_distance(pos_number,pos_number0)
            if distance_0 == 1:
                return True
            return False
        pos_number0 ,pos_number1= self.get_pos(number-1) ,self.get_pos(number+1)
        pos_number = self.get_pos(number)
        distance_0 = board_distance(pos_number,pos_number0)
        distance_1 = board_distance(pos_number,pos_number1)
        if distance_1 ==1 and  distance_0 == 1:
            return True
        return False

    def valid_board2(self,number):
            pos_num =self.get_pos(number)
            row,col = pos_num[0],pos_num[1]
            adjacents = self.adjacent_horizontal_numbers(row, col) +self.adjacent_vertical_numbers(row,col)
            number_to_set_count = 0
            if number-1 >= 1 and not self.is_setted(number-1):
                number_to_set_count += 1
            if number + 1 <= self.max and not self.is_setted(number+1):
                number_to_set_count+=1
            return number_to_set_count <= adjacents.count(0)
                
    def valid_board(self,number):
            if(number  >= self.max or number  <= 1): 
                return True
            if(self.adj_setted(number)):
                pos_number0 ,pos_number1= self.get_pos(number-1) ,self.get_pos(number+1)
                distance0_1 = board_distance(pos_number0,pos_number1)
                if(distance0_1 != 2):
                    return False
                if self.is_setted(number):
                    return self.neighbours_nearby(number)
            return True

def returned_actions(actions):
        if(actions == []):
            return []
        a = [actions[0]]
        b = []

        for i in range(1,len(actions)):
            if(len(b) != 0 and actions[i][2] != a[0][2] and actions[i][2] != b[0][2]):
                if(len(b) == 1):
                    return b
                if len(a) == 1:
                    return a
                if(len(b) < len(a)):
                    a = b[:]
                b.clear()
            if(actions[i][2] == a[0][2]):
                a.append(actions[i])
            else:
                b.append(actions[i])
            
        if( len(b) > 0 and len(b) < len(a)):
            return b
        return a

class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        super().__init__(NumbrixState(board))
        self.board = board

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []

        for number  in state.board.board_setted: 
            if not state.board.valid_board2(number):
                return []
            if not state.board.valid_board(number-1) or not state.board.valid_board(number + 1):
                return []
            row,col = state.board.get_pos(number)[0],state.board.get_pos(number)[1]
            if row - 2 >= 0:
                is_number = state.board.get_number(row-2,col)
                if is_number != 0:
                    if abs(number-is_number) == 2:
                        if state.board.get_number(row-1,col) == 0:
                            return [(row-1,col,average_numbers(number,is_number))]
            if row + 2 <= state.board.size -1:
                is_number = state.board.get_number(row+2,col)
                if is_number != 0:
                    if abs(number-is_number) == 2:
                        if state.board.get_number(row+1,col) == 0:
                            return [(row+1,col,average_numbers(number,is_number))]

            if col + 2 <= state.board.size -1:
                is_number = state.board.get_number(row,col+2)
                if is_number != 0:
                    if abs(number-is_number) == 2:
                        if state.board.get_number(row,col+1) == 0:
                            
                            return [(row,col+1,average_numbers(number,is_number))]
            if col - 2 >= 0:
                is_number = state.board.get_number(row,col-2)
                if is_number != 0:
                    if abs(number-is_number) == 2:
                        if state.board.get_number(row,col-1) == 0:
                            return [(row,col-1,average_numbers(number,is_number))]

            adjacents =  state.board.adjacent_horizontal_numbers(row, col) + state.board.adjacent_vertical_numbers(row,col)
            num_left, num_right, num_up, num_down = adjacents[0], adjacents[1], adjacents[2], adjacents[3]
            if num_left == 0:
                if number -1 != 0 and not state.board.is_setted(number-1):
                    if state.board.valid_action(row,col-1,number-1,state.board.size):
                        actions.append((row,col-1,number-1))
                if number + 1 <= state.board.max and not state.board.is_setted(number+1):
                    if state.board.valid_action(row,col-1,number+1,state.board.size):
                        actions.append((row,col-1,number+1))
            if num_right == 0:
                if number -1 != 0 and not state.board.is_setted(number-1):
                    if state.board.valid_action(row,col+1,number-1,state.board.size):                
                        actions.append((row,col+1,number-1))
                if number + 1 <= state.board.max and not state.board.is_setted(number+1):    
                    if state.board.valid_action(row,col+1,number+1,state.board.size):              
                        actions.append((row,col+1,number+1))
            if num_down == 0:
                if number -1 != 0 and not state.board.is_setted(number-1): 
                    if state.board.valid_action(row+1,col,number-1,state.board.size):               
                        actions.append((row+1,col,number-1))
                if number + 1 <= state.board.max and not state.board.is_setted(number+1):
                    if state.board.valid_action(row+1,col,number+1,state.board.size):                  
                        actions.append((row+1,col,number+1))
            if num_up == 0:
                if number -1 != 0 and not state.board.is_setted(number-1):
                    if state.board.valid_action(row-1,col,number-1,state.board.size):                 
                        actions.append((row-1,col,number-1))
                if number + 1 <= state.board.max and not state.board.is_setted(number+1):
                    if state.board.valid_action(row-1,col,number+1,state.board.size):
                        actions.append((row-1,col,number+1))

        no = list(set(actions))
        no.sort(key = lambda x: x[2])
        a = returned_actions(no)

        return a
        

        

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        
        row = action[0]
        col = action[1]
        number = int(action[2])
        new_board_list = state.board.board_list[:]
        new_board_list[row*state.board.size + col] = number
        new_board_list2 = state.board.board_list2[:]
        new_board_list2[number-1] = (row, col)
        new_board_setted = state.board.board_setted[:]
        new_board_setted.append(number)
        
        low_streak, high_streak = 0,0
        while (low_streak != state.board.size*state.board.size and new_board_list2[low_streak+1-1] != (-1,-1)):
            low_streak+=1
        while(low_streak != state.board.size*state.board.size and new_board_list2[state.board.size*state.board.size-high_streak-1] != (-1,-1)):
            high_streak+=1

        new_numbers_setted = state.board.numbers_setted[:]
        new_numbers_setted[number-1] = True

        new_board_setted.sort()
        new_board = Board(new_board_setted,new_board_list,new_numbers_setted,new_board_list2, state.board.size, state.board.amount_setted +1,low_streak,high_streak)
        new_state = NumbrixState(new_board)

        
        

      
        return new_state
        

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        board_size = state.board.size
        if not (state.board.amount_setted == state.board.max):
            return False
        for i in range(board_size):
            for j in range(state.board.size):
                number = state.board.get_number(i, j)
                adjacents =  state.board.adjacent_horizontal_numbers(i, j) + state.board.adjacent_vertical_numbers(i,j)
                if (number == 1):
                    if (not (number+1) in adjacents):
                        return False
                elif (number == state.board.max):
                    if(not (number-1) in adjacents):
                        return False
                else:
                    if not (number+1 in adjacents or number-1 in adjacents):
                        return False
        return True
        
    def h(self, node: Node):
        if(node.action == None):
            return 0
         
        j = node.action[1]
        i = node.action[0]
        adjacents =  node.state.board.adjacent_horizontal_numbers(i, j) + node.state.board.adjacent_vertical_numbers(i,j)
        sum = 0
        amount_None = 0
        for i in adjacents:
            if i == 0:
                sum += 1
            if i == None:
                amount_None += 1         
        sum2 = 0

        lst = node.state.board.numbers_setted
        first1 = lst.index(1)
        next1 = first1 +1
        while next1 < node.state.board.size*node.state.board.size-1:
            while not lst[next1]:
                next1 += 1
                if next1 == node.state.board.size*node.state.board.size-1:
                    break

            if real_distance(first1+1, next1+1) != board_distance(node.state.board.get_pos(next1+1),node.state.board.get_pos(first1+1)):
                sum2 += 1
            first1 = next1
            next1 = first1 +1
        return -node.state.board.low_streak*2 - node.state.board.high_streak*2 + sum*20 - sum2*10 - amount_None*3

if __name__ == "__main__":
    print(astar_search(Numbrix(Board.parse_instance(sys.argv[1]))).state.board)