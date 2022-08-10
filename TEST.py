# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 61:
# 96904 Pedro Severino
# 95586 Guilherme Costa



import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search
import copy
import time



class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """    

    def __init__(self, board_list, size, numbers_setted, amount_setted):
        """ Representação do tabuleiro. """
        self.size = size
        self.board_list = board_list
        self.numbers_setted = numbers_setted
        self.amount_setted = amount_setted

    def __repr__(self):
        """ O construtor especifica o estado inicial. """
        return "Board List: " + self.board_list.__str__() + "\nSize: "+ self.size.__str__() + "\nNumbers Setted: " + self.numbers_setted.__str__() +\
             "\nAmount Setted: " + self.amount_setted.__str__()
    
    def to_string(self):
        string = ""
        
        for i in range(self.size):
            for j in range(self.size):
                
                string += str(self.board_list[i][j])
                string += '\t'
            string = string[:-1] + "\n"
        string = string[:-1] 
        return string    


    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.board_list[row][col]
    
    def adjacent_vertical_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        if (0 < row):
            num1 = self.board_list[row - 1][col]
        else:
            num1 = None    

        if (row < self.size-1):
            num2 = self.board_list[row + 1][col]
        else:
            num2 = None   
        return (num1,num2)

    def adjacent_horizontal_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        if (0 < col):
            num1 = self.board_list[row][col-1]
        else:
            num1 = None   
        if (col < self.size-1):
            num2 = self.board_list[row][col+1]
        else:
            num2 = None 
        return (num1,num2)
    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        lst = []
        f = open(filename, 'r')
        size = int(f.readline().rstrip())
        lines = f.readlines()

        f.close()
        numbers_setted = [0] * (size*size)
        amount_setted = 0 
        board_dict = {}
        for line in lines:
            line = line.rstrip("\n")
            
            row_numbers = line.split("\t")
            
            row_numbers[size-1]
            lst2 = []
            for c in row_numbers:
                
                if c.isdigit():
                    
                    lst2.append(int(c))
                    if(int(c) != 0):
                        numbers_setted[int(c) -1 ] = 1
                        amount_setted += 1    
            lst.append(lst2)
        for i in range(0,size):
            for j in range(0,size):
                if(lst[i][j] != 0):
                    board_dict[lst[i][j]] = (i,j)
        return  Board(lst, size, numbers_setted, amount_setted,board_dict)

    # TODO: outros metodos da classe


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
        possible_actions = []
        best_actions = []
        for i in range(0,state.board.size):
            for j in range(0,state.board.size):
                number = state.board.get_number(i,j)
                adjacents =  state.board.adjacent_horizontal_numbers(i, j) + state.board.adjacent_vertical_numbers(i,j)
                if(number == 0):       
                    print(adjacents) 
                    for adj in adjacents:
                        if(adj != None and adj != 0 and adj +1 <= state.board.size *state.board.size and state.board.numbers_setted[adj+1 -1 ] == 0 ):
                            if((i,j,adj+1) in possible_actions):
                                possible_actions.remove((i,j,adj+1))
                                print("||||||||||||||||||||||||||||||||||||||||||||||")
                                print("Best Actions1: ")
                                print([(i,j,adj+1)])
                                print("||||||||||||||||||||||||||||||||||||||||||||||")
                                best_actions.append((i,j,adj+1))
                            else:
                                
                                if(state.board.numbers_setted[adj-1 -1 ] == 1 and state.board.numbers_setted[adj+1-1]  == 1 and adj -1 not in adjacents and adj  + 1  not in adjacents):
                                    print("sheesh")
                                else: 
                                    possible_actions.append((i,j,adj+1))
                        if(adj != None and adj != 0 and adj -1 > 0 and state.board.numbers_setted[adj-1 -1 ] == 0 ):
                            if((i,j,adj-1) in possible_actions):
                                possible_actions.remove((i,j,adj-1))
                                print("||||||||||||||||||||||||||||||||||||||||||||||")
                                print("Best Actions2: ")
                                print([(i,j,adj-1)])
                                print("||||||||||||||||||||||||||||||||||||||||||||||")
                                best_actions.append((i,j,adj-1))
                            else:
                                print()
                                if(state.board.numbers_setted[adj -1-1] == 1 and state.board.numbers_setted[adj+1-1]  == 1 and adj -1  not in adjacents and adj + 1 not in adjacents):
                                    print("sheesh")
                                else:
                                    possible_actions.append((i,j,adj-1))
        
        
        if(best_actions):
            possible_actions = best_actions 
        possible_actions.sort(key = lambda x: x[2])

        a = returned_actions(possible_actions)
        print("\n\n")
        print("This is returned ACTIONS" + str(a))
        input()
        return a
        

        

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        
        row = action[0]
        col = action[1]
        number = int(action[2])
        
        new_board_list = copy.deepcopy(state.board.board_list)
        new_board_list[row][col] = number

        new_numbers_setted = copy.deepcopy(state.board.numbers_setted)
        new_numbers_setted[number-1] = 1 
        
        new_amount_setted = state.board.amount_setted +1
        
     
        boardsd = Board(new_board_list, state.board.size, new_numbers_setted, new_amount_setted)
        new_state = NumbrixState(boardsd)

        print("##############################################")
        print("ID: " +str(new_state.id))
        print("\n" + new_state.board.to_string(),sep = "")
        
        print("##############################################")
        

      
        return new_state
        

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        board_size = state.board.size
        if not (state.board.amount_setted == board_size*board_size):
            return False
        for i in range(board_size):
            for j in range(state.board.size):
                number = state.board.get_number(i, j)
                adjacents =  state.board.adjacent_horizontal_numbers(i, j) + state.board.adjacent_vertical_numbers(i,j)
                if (number == 1):
                    if (not (number+1) in adjacents):
                        return False
                elif (number == board_size*board_size):
                    if(not (number-1) in adjacents):
                        return False
                else:
                    if(not set((number-1, number+1)).issubset(set(adjacents))):
                        return False
        return True
        

    def h(self, node: Node):
        if(node.action == None):
            return 0
        print(node.action)
        j = node.action[1]
        i = node.action[0]
        adjacents =  node.state.board.adjacent_horizontal_numbers(i, j) + node.state.board.adjacent_vertical_numbers(i,j)
        sum = adjacents.count(0) * 100
        print(sum)
        print(adjacents)
        return sum
    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance(sys.argv[1])
    
    
    problem = Numbrix(board)

    print("##############################################")   
    print("\nInitial state:")
    print(board.to_string() + "\n", sep = "")
    print("##############################################")
    input()

    goal_node = astar_search(problem)
    
    if (goal_node):
        print("\nFinal solution:")
        print(goal_node.state.board.to_string())
    else:
        print("\nNo Solution found.")



    
  
   
    
    
    
    

