import pickle
class Player:
    def __init__(self, mode, symbol,alpha=0.1, gamma=0.9):
        self.mode = mode
        self.symbol = symbol
        self.q_table={}
        self.state_list=[]
        self.alpha = alpha  
        self.gamma = gamma  
        self.exploration_rate=1
        
    def board_to_string(self,board):
        boardstr=""
        for elem in board:
            boardstr+=str(elem)
    def exploration_rate_decay(self):
        a=self.exploration_rate-0.0001
        self.exploration_rate=max(0.01,a)
        
    def qlearning_action(self,board,a_pos,way='test'):
        if way=='train':
            if random.random()<self.exploration_rate:
                return random.choice(a_pos)
            else:
                strboard=self.board_to_string(board)
                max_value=-10000
                best_action=random.choice(a_pos)
                for key,value in self.q_table[strboard]:
                  if(value>max_value):
                    if key in a_pos:
                        best_action=key
                    max_value=value
            self.exploration_rate_decay()
        if way=='test':
            strboard=self.board_to_string(board)
            max_value=-10000
            best_action=random.choice(a_pos)
            for key,value in self.q_table[strboard]:
              if(value>max_value):
                if key in a_pos:
                    best_action=key
                max_value=value
        return best_action
    def store_state_list(self,board,pos):
        self.state_list.append((board,pos))
    
    def update_q_table(self,winner):
        reward = self.get_reward(winner)


        for index in range(len(self.state_list) - 1, -1, -1):
            (sta_list, action) = self.state_list[index]
            state=self.board_to_string(sta_list)
            if state not in self.q_table:
                self.q_table[state] = {}
            if action not in self.q_table[state]:
                self.q_table[state][action] = 0

            if index < len(self.state_list) - 1:
                next_state, _ = self.state_list[index + 1]
                if next_state in self.q_table:
        
                    max_q_next = max(self.q_table[next_state].values()) 
                else:
                    max_q_next=0
            else:
                max_q_next = 0

            # 更新Q值
            self.q_table[state][action] += self.alpha * (reward + self.gamma * max_q_next - self.q_table[state][action])

            reward = 0
        
    def get_reward(self, winner):
        if winner ==self.symbol:
            return 1  # Reward for winning
        elif winner == 0:
            return 0.5  # Reward for drawing
        else:
            return -1  # Reward for losing

    def savePolicy(self):
        fw = open('./q_table', 'wb')
        pickle.dump(self.q_table, fw)
        fw.close()

    def loadPolicy(self):
        fr_q =pickle.load(open("./q_learning_policy", 'rb'))

        self.q_table = fr_q

import random

class TicTacToe:
    def __init__(self, player1_mode, player2_mode, first_player='player1'):
        self.board = [0] * 9
        self.player1 = Player(player1_mode, 1)
        self.player2 = Player(player2_mode, -1)
        self.current_player = self.player1 if first_player == 'player1' else self.player2
        self.gameover = False

    def print_game_start(self):
        self.reset_board()
        
        print("Game Start!")
        print(f"Player 1 mode: {self.player1.mode}")
        print(f"Player 2 mode: {self.player2.mode}")
        self.print_board()

    def print_board(self):
        
        board_2d=[self.board[0:3],self.board[3:6],self.board[6:9]]
        
        for row in board_2d:
            print(row)

    def define_position_available(self):
        return [i for i, val in enumerate(self.board) if val == 0]

    def reset_board(self):
        self.board = [0] * 9
        self.gameover = False
        

    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2



    def update_board(self, position):
        self.board[position] = self.current_player.symbol


    def if_game_over(self):
        '''
        [0,0,0,1,1,1,1,-1,0]
        
        i (0,1,2): 
        row: (0,1,2),(3,4,5),(6,7,8)  ->3i,index=(3i,3i+1,3i+2)
        
        column: (0,3,6),(1,4,7),(2,5,8) -> i,index=(i,i+3,i+6)
        
        diagonal: (0,4,8),(2,4,6)
        '''
        winner=0
    
        for i in range(0,3):
            #check row/column
            if (self.board[3*i]+self.board[3*i+1]+self.board[3*i+2])==3 or (self.board[i]+self.board[i+3]+self.board[i+6])==3:
                winner=1
                break
            if (self.board[3*i]+self.board[3*i+1]+self.board[3*i+2])==-3 or (self.board[i]+self.board[i+3]+self.board[i+6])==-3:
                winner=-1
                break
        if self.board[0]+self.board[4]+self.board[8]==3 or self.board[2]+self.board[4]+self.board[6]==3: 
            winner=1
        if self.board[0]+self.board[4]+self.board[8]==-3 or self.board[2]+self.board[4]+self.board[6]==-3: 
            winner=-1
        
            
        if winner==1 or winner==-1:
            #print('gameover =true')
            self.gameover=True
        elif winner==0 and (len(self.define_position_available())==0):
            self.gameover=True
        # else:
        #     self.gameover=False
        
        return winner

    def print_game_result(self, result):
        if result == 'Draw':
            print("It's a draw!")
        else:
            print(f"Player {result} wins!")
    def generate_position(self,way='test'):
    
            position=0 # 1 D board positionposition
            if self.current_player.mode == 'user':
                [row,column]=map(int,input("Input row/column").split("/"))
                position=row*3+column

            elif self.current_player.mode == 'random':
                position=random.randint(0,8)

            elif self.current_player.mode=='qlearning':
                position=self.current_player.qlearning_action(self.board,self.define_position_availible(),way=way)
                
            else:
                print("the player don't has this mode")
            return position
    
    
    def game_over(self,winner,way='test'):
        if way=='test':
            if winner==1:
                print("player1 win~!")
            elif winner==-1:
                print("player2 win~!")
            else:
                print('tie')
            print('game done')
        if way=='train':
            if self.player1.mode=='qlearning':
                self.player1.update_q_table(winner)
                self.player1.statelist=[]
            if self.player2.mode=='qlearning':
                self.player2.update_q_table(winner)
                self.player2.statelist=[]


    def train(self,episode=1000):
        if not (self.player1.mode=='qlearning' or self.player2.mode=='qlearning'):
            print("there is  no player need to  train")
            return None
        for i in range(episode):
            self.print_game_start()
            while not self.game_over:
                position = self.generate_position(way='train')
                if self.current_player.mode=='qlearning':
                    self.current_player.store_state_list(self.board,position)
                self.update_board(position)
                #self.print_board()

                winner = self.if_game_over()
                self.switch_player()
                if self.gameover:
                    self.game_over(winner,way='train')
        if self.player1.mode=='qlearning':
            self.player1.savePolicy()
        if self.player2.mode=='qlearning':
            self.player2.savePolicy()
    def play(self):
        self.print_game_start()
        
        while not self.gameover:
            if self.current_player==self.player1:
                cur='player1'
            else:
                cur='player2'
            print("current player:",cur)
            position = self.generate_position()
            self.update_board(position)
            self.print_board()
            
            winner = self.if_game_over()
            #print("winner:",winner)
            #print("game over:",self.gameover)
            self.switch_player()

            if self.gameover:
                self.game_over(winner)
    
# Example of how to use these methods
if __name__ == "__main__":
    game = TicTacToe(player1_mode='qleaerning', player2_mode='random')
    #game.player1.loadPolicy()
    game.play()

