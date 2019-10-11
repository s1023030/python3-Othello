'''
黑白棋、翻轉棋（Reversi）、奧賽羅棋（Othello）
規則:
棋盤共有8行8列共64格。開局時，棋盤正中央的4格先置放黑白相隔的4枚棋子（亦有求變化相鄰放置）。
通常黑子先行。雙方輪流落子。只要落子和棋盤上任一枚己方的棋子在一條線上（橫、直、斜線皆可）夾
著對方棋子，就能將對方的這些棋子轉變為我己方（翻面即可）。如果在任一位置落子都不能夾住對手的
任一顆棋子，就要讓對手下子。當雙方皆不能下子時，遊戲就結束，子多的一方勝。

盤面:board
棋子:disk

'''
import math
import random
import configparser 
from GUI import GUI
from Agent.Agent import Human
from Agent.AI_factory import AI_factory
class Game:
    def __init__(self):
        self.config=configparser.ConfigParser()
        self.config.read("Othello.cfg")
        self.players=[]
        self.gui= GUI(parent=self,config=self.config)
        self.gui.mainloop()

    def game_start(self,mode,turn=1,*args, **kwargs):
        #self.turn判斷是誰的回合
        #●:   1
        #○:  0
        self.mode=mode
        self.turn=turn
        self.board=[
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1, 0, 1,-1,-1,-1],
            [-1,-1,-1, 1, 0,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1]
        ]
        #self._desks紀錄現在盤面所有desk的位置，
        #self._desks[0]為 0 desks
        #self._desks[1]為 1 desks
        #以方便_possible_next_step()計算。
        #位置紀錄格式:(row數,col數)
        self._desks=[
            set([(3,3),(4,4)]),set([(3,4),(4,3)])
        ]
        self.poss_next_steps=set()
        self.has_passed_once=False
        #mode=1  PvP
        #mode=2  PvC
        #mode=3  CvC
        if self.mode==1:
            self.players=[Human(),Human()]
            winner,reward,self.poss_next_steps=self._cal_state()
            self.gui.frames['Game_interface'].init_GUI(self.board,reward,self.poss_next_steps)
        elif self.mode==2:
            ai=self.config._sections["AI"]["1"]                          ## hard code
            self.players=[AI_factory.generate_AI(ai),Human()]
            self.players[0].new_episode()
            random.shuffle(self.players)
            winner,reward,self.poss_next_steps=self._cal_state()
            self.gui.frames['Game_interface'].init_GUI(self.board,reward,self.poss_next_steps)
        elif self.mode==3:
            ai1=kwargs['c1']        #       computer 1 的演算法  
            ai2=kwargs['c2']        #       computer 2 的演算法
            del kwargs['c1']
            del kwargs['c2'] 
            if len(self.players)==0:
                print("Set player")
                self.players=[AI_factory.generate_AI(ai1),AI_factory.generate_AI(ai2)]
            self.players[0].new_episode()
            self.players[1].new_episode()
            #random.shuffle(self.players)
        self.game_loop=self._game_flow()
        winner,reward,poss_next_steps=next(self.game_loop)
        return

    def _game_flow(self):
        while True:
            winner,reward,self.poss_next_steps= self._cal_state()
            #已確定勝者
            if winner>-1:
                if self.mode==3:                                   #mode=3 ==> CvC 要回傳最終rewards
                    yield  winner,reward,self.poss_next_steps
                else:
                    self.gui.frames['Game_interface'].game_over(winner,reward)
            
            if self.players[self.turn].is_human:
                yield  winner,reward,self.poss_next_steps
            else:
                #player is AI
                next_step=self.players[self.turn].placing_desk(winner,self.turn,self.board,reward,self.poss_next_steps)
                if next_step[0]==(-1,-1):          #沒有下一手可下
                    pass
                else:
                    turn,change_disks,poss_last_steps=self.placing_disk(next_step[0])
                    if self.mode==2:           #PvC
                        self.gui.frames['Game_interface']._update_after_placing(turn,change_disks,poss_last_steps)
            self.turn=self.turn^1

            if self.mode==1 or self.mode==2:    #PvP or PvC
                winner,reward,self.poss_next_steps=self._cal_state()
                self.gui.frames['Game_interface']._change_reward_text(0,str(reward[0]))
                self.gui.frames['Game_interface']._change_reward_text(1,str(reward[1]))
                self.gui.frames['Game_interface']._update_desks(self.poss_next_steps,'．')

    def _cal_state(self):
        #檢查是否有贏家，同時計算彼此棋子數目，還有列出下一次可下的位置
        self.poss_next_steps=self._possible_next_step()
        #處理沒有"可能的下一步"的情況
        winner=-1
        reward=[len(self._desks[0]),len(self._desks[1])] #calculate reward
        if len(self.poss_next_steps)==0:
            if self.has_passed_once:
                if reward[0]>reward[1]:
                    return 0,reward,self.poss_next_steps
                elif reward[0]<reward[1]:
                    return 1,reward,self.poss_next_steps
                else:#flat
                    return 2,reward,self.poss_next_steps
            self.has_passed_once=True
            self.turn=self.turn^1
            tmp_generator=self._game_flow()
            winner,reward,self.poss_next_steps=next(tmp_generator)
        else:
            self.has_passed_once=False

        #檢查是否終局
        total_desks=reward[0]+reward[1]
        if total_desks==64 or winner>-1:
            if reward[0]>reward[1]:
                return 0,reward,self.poss_next_steps
            elif reward[0]<reward[1]:
                return 1,reward,self.poss_next_steps
            else:#flat
                return 2,reward,self.poss_next_steps
        return winner,reward,self.poss_next_steps
    
    def _possible_next_step(self):
        next_step=set()
        if self.turn==1:
            disk_of_turn=1
            oppenent=0
        else:
            disk_of_turn=0
            oppenent=1
        directions=[(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for tmp in self._desks[disk_of_turn]:
            for direction in directions:
                possible_pos=self._find_the_shore(tmp,direction,disk_of_turn,oppenent)
                if possible_pos is not None:
                    next_step.add(possible_pos)
        return next_step
    
    def placing_disk(self,pos):
        new_desk_set=set()
        if self.turn==1:
            disk_of_turn=1
            opponent=0
        else:
            disk_of_turn=0
            opponent=1
        #敵方棋子被夾擊後會翻轉
        for exist_desk in  self._desks[disk_of_turn]:
            if exist_desk[0]==pos[0] or exist_desk[1]==pos[1] or self._in_slash(exist_desk,pos):
                direction=self._gen_vector(pos,exist_desk)
                if self._connect_in_line(pos,exist_desk,direction,self._desks[opponent]):
                    new_desk_set |= (self._reverse_desks(pos,exist_desk,direction,disk_of_turn))
        
        self.board[pos[0]][pos[1]]=disk_of_turn
        new_desk_set.add(pos)
        self._desks[disk_of_turn] |= new_desk_set
        self._desks[opponent] -= new_desk_set
        return self.turn,new_desk_set,self.poss_next_steps

    def check_valid_step(self,step):
        if step in self.poss_next_steps:
            return True
        else:
            return False
        
    def _find_the_shore(self,from_pos,direction,disk_of_turn,opp):
        shore_row=0
        shore_row=0
        pos_row=from_pos[0]
        pos_col=from_pos[1]
        pos_row+=direction[0]
        pos_col+=direction[1]
        is_first=True
        while self._is_in_bound((pos_row,pos_col)) and self.board[pos_row][pos_col]==opp:
            pos_row+=direction[0]
            pos_col+=direction[1]
            shore_row=pos_row
            shore_col=pos_col
            is_first=False
        if is_first:
            return None
        elif not self._is_in_bound((pos_row,pos_col)):
            return None
        elif self._is_in_bound((pos_row,pos_col)) and self.board[pos_row][pos_col]==disk_of_turn:
            return None
        return (shore_row,shore_col)
    
    def _is_in_bound(self,pos=(None,None)):
        #確認row是否超過邊界
        if pos[0]>(len(self.board)-1) or pos[0]<0:
            return False
        #確認col是否超過邊界
        if pos[1]>(len(self.board)-1) or pos[1]<0:
            return False
        return True
    
    def _in_slash(self,a=(None,None),b=(None,None)):
        if abs(a[0]-b[0])==abs(a[1]-b[1]):
            return True
        return False
    
    def _gen_vector(self,from_pos=(None,None),to_pos=(None,None)):
        row=float(to_pos[0]-from_pos[0])
        col=float(to_pos[1]-from_pos[1])
        v_len=int(math.sqrt(math.pow(row,2.0)+math.pow(col,2.0)))
        return (round(row/v_len),round(col/v_len))
    
    def _connect_in_line(self,from_pos,to_pos,direction,opp_desk_set):
        is_first=True
        tmp_pos_row=from_pos[0]
        tmp_pos_col=from_pos[1]
        tmp_pos_row+=direction[0]
        tmp_pos_col+=direction[1]
        while tmp_pos_row!=to_pos[0] or tmp_pos_col!=to_pos[1]:
            if not((tmp_pos_row,tmp_pos_col) in opp_desk_set):
                return False
            tmp_pos_row+=direction[0]
            tmp_pos_col+=direction[1]
            is_first=False
        if is_first:
            return False
        return True
    
    def _reverse_desks(self,from_pos,to_pos,direction,disk_of_turn):
        new_disk_set=set()
        tmp_pos_row=from_pos[0]
        tmp_pos_col=from_pos[1]
        tmp_pos_row+=direction[0]
        tmp_pos_col+=direction[1]
        while tmp_pos_row!=to_pos[0] or tmp_pos_col!=to_pos[1]:
            self.board[tmp_pos_row][tmp_pos_col]=disk_of_turn
            new_disk_set.add((tmp_pos_row,tmp_pos_col))
            tmp_pos_row+=direction[0]
            tmp_pos_col+=direction[1]
        return new_disk_set

    def display(self):
        print("=========================")
        for row in self.board:
            for ele in row:
                if ele==-1:
                    print(" 。",end="")
                elif ele==0:
                    print(" ○",end="")
                elif ele==1:
                    print(" ●",end="")
            print("")
        print("=========================")
        return self.board


#======================================================================================

#==========================================================================================================
def main(): 
    game=Game()

if __name__ == '__main__':
    main()

