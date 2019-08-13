import tkinter as tk
from  tkinter  import ttk       
from tkinter import font  as tkfont
import configparser 
#from Othello import Game
class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.parent=kwargs['parent']
        self.config=kwargs['config']
        del kwargs['parent']
        del kwargs['config']
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(False,False)       #視窗長寬使用者是否可變動
        
        for num in range(3):             #設置每個視窗單位最少有佔多大空間
            if num==1:
                self.grid_rowconfigure(num, weight=10)
                self.grid_columnconfigure(num, weight=10)
            else:
                self.grid_rowconfigure(num, weight=1)
                self.grid_columnconfigure(num, weight=1)
        self.title_font = tkfont.Font(family='Times', size=18, weight="bold")
        self.container = tk.Frame(self)
        self.container.grid(row=1,column=1)
        
        #獲得每一個場景的實例並存到self.frames
        self.frames = {}
        for F in (Main_interface, Game_interface,Game_over_interface,CvC_Game_interface,CvC_Game_over_interface):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self,gd_parent=self.parent)
            self.frames[page_name] = frame
        #載入第一個場景
        self.show_frame("Main_interface",0)
        
    #顯示場景的函示
    def show_frame(self, page_name,mode=-1,other=None):
        frame = self.frames[page_name]
        frame.grid(row=0, column=0, sticky="nsew")
        if mode==0:                 #Main_interface
            self.resize_window(400,300)       #調整使窗長高
        elif mode==1:               #Game_interface PvP
            self.resize_window(500,500)
            frame.init_play(mode)
        elif mode==2:               #Game_interface PvC
            self.resize_window(500,500)
            frame.init_play(mode)
        elif mode==3:               #Game_interface CvC
            self.resize_window(500,500)
            frame.init_GUI(mode)
        elif mode==4:               #Game_over_interface
            frame.display_result(other)
        elif mode==5:               #CvC_Game_over_interface
            frame.display_result(other)
        frame.tkraise()
        
    def exit(self):
        self.destroy()
        
    def resize_window(self,width,height):
        self.geometry(str(width)+"x"+str(height))
        
class Interface(tk.Frame):
    def __init__(self, parent, controller,gd_parent):
        tk.Frame.__init__(self, parent)
        self.gd_parent=gd_parent
        self.parent=parent
        self.controller = controller
        
    def _widgets_grid(self):
        pass
    
class Main_interface(Interface):
    def __init__(self, parent, controller,gd_parent):
        super().__init__(parent, controller,gd_parent)
        self.widgets=[]
        self.gd_parent=gd_parent
        self.widgets.append(tk.Button(self, text="PvP",font=controller.title_font, width = 25 ,command=self._PvP))
        self.widgets.append(tk.Button(self, text="PvC",font=controller.title_font, width = 25 ,command=self._PvC))
        self.widgets.append(tk.Button(self, text="CvC",font=controller.title_font, width = 25 ,command=self._CvC))
        self.widgets.append(tk.Button(self, text="Exit",font=controller.title_font, width = 25 ,command=self._exit))
        self._widgets_grid()
        
    def _widgets_grid(self):
        for widget,num in zip(self.widgets,range(len(self.widgets))):
            widget.grid(column=1,row=num,sticky="nesw")
            
    def _PvP(self):
        self.grid_forget()
        self.controller.show_frame("Game_interface",1)
        
    def _PvC(self):
        self.grid_forget()
        self.controller.show_frame("Game_interface",2)
        
    def _CvC(self):
        self.grid_forget()
        self.controller.show_frame("CvC_Game_interface",3)
        
    def _exit(self):
        self.controller.exit()
        
class Game_over_interface(Interface):
    def __init__(self, parent, controller,gd_parent):
        super().__init__(parent, controller,gd_parent)
        self.gd_parent=gd_parent
        self.rewards=[]
        self.return_to_main=tk.Button(self, text="Return to menu",
                                      font=controller.title_font,
                                      width = 15 ,command=self._return_to_main)
        self.rewards.append([tk.Label(self, text="2",font=self.controller.title_font,width=2,height=1),0,3])
        self.rewards.append([tk.Label(self, text='2',font=self.controller.title_font,width=2,height=1),0,1])
        self.rewards.append([tk.Label(self, text="○",font=self.controller.title_font,width=2,height=1),0,2])
        self.rewards.append([tk.Label(self, text='●',font=self.controller.title_font,width=2,height=1),0,0])
        self.winner=tk.Label(self, text="?? win",font=self.controller.title_font,width=2,height=1)
        self._widgets_grid()
    def display_result(self,result):
        self.rewards[0][0].configure(text=str(result["rewards"][0]))
        self.rewards[1][0].configure(text=str(result["rewards"][1]))
        if result["winner"]==0:
            self.winner.configure(text="○ win")
        elif result["winner"]==1:
            self.winner.configure(text="● win")
        else:#flat:
            self.winner.configure(text="Flat")
    def _return_to_main(self):
        self.grid_forget()
        self.controller.show_frame("Main_interface",0)
    def _widgets_grid(self):
        self.return_to_main.grid(column=0,row=2,columnspan=4,sticky="nesw")
        self.winner.grid(column=0,row=1,columnspan=4,sticky="nesw")
        for ele in self.rewards:
            ele[0].grid(column=ele[2],row=ele[1],sticky="nesw")

class CvC_Game_over_interface(Interface):
    def __init__(self, parent, controller,gd_parent):
        super().__init__(parent, controller,gd_parent)
        self.gd_parent=gd_parent
        self.rewards=[]
        self.return_to_main=tk.Button(self, text="Return to menu",
                                      font=controller.title_font,
                                      width = 15 ,command=self._return_to_main)
        self.rewards.append([tk.Label(self, text="2",font=self.controller.title_font,width=4,height=1),1,1])
        self.rewards.append([tk.Label(self, text='2',font=self.controller.title_font,width=4,height=1),1,0])
        self.rewards.append([tk.Label(self, text="AI 2",font=self.controller.title_font,width=4,height=1),0,1])
        self.rewards.append([tk.Label(self, text='AI 1',font=self.controller.title_font,width=4,height=1),0,0])
        self.winner=tk.Label(self, text="?? win",font=self.controller.title_font,width=2,height=1)
        self._widgets_grid()
    def display_result(self,result):
        self.rewards[0][0].configure(text=str(result["win"][0]))
        self.rewards[1][0].configure(text=str(result["win"][1]))
        if result["win"][0]>result["win"][1]:
            self.winner.configure(text="AI 2 win")
        elif result["win"][0]<result["win"][1]:
            self.winner.configure(text="AI 1 win")
        else:#flat:
            self.winner.configure(text="Flat")
    def _return_to_main(self):
        self.grid_forget()
        self.controller.show_frame("Main_interface",0)
    def _widgets_grid(self):
        self.return_to_main.grid(column=4,row=3,sticky="nesw")
        self.winner.grid(column=4,row=1,sticky="nesw")
        for ele in self.rewards:
            ele[0].grid(column=ele[2],row=ele[1],sticky="nesw")

class CvC_Game_interface(Interface):
    def __init__(self, parent, controller,gd_parent):
        super().__init__(parent, controller,gd_parent)
        self.first_play=True
        self.question=None
        self.text=None
        
    def init_GUI(self,mode):
        self.question = tk.Label(self, text="How many times?",font=self.controller.title_font,width=20,height=1)
        vcmd = (self.controller.register(self._validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.text = tk.Entry(self,validatecommand = vcmd,width=10)
        self.button = tk.Button(self, text = 'Start', font=self.controller.title_font,
                                                     width=10,height=1,
                                                     command=self._start_game)
        AI_list=[]
        for k,v in self.controller.config._sections["AI"].items():
            AI_list.append(v)
        self.c1=ttk.Combobox(self,value=AI_list)
        self.c2=ttk.Combobox(self,value=AI_list)
        self.txt_c1 = tk.Label(self,text="Player 1",width=10,height=1)
        self.txt_c2 = tk.Label(self,text="Player 2",width=10,height=1)
        self._widgets_grid()
        
    def _widgets_grid(self):
        self.question.grid(column=0,row=0,columnspan=3,sticky="nesw")
        self.text.grid(column=0,row=2,columnspan=3,sticky="nesw")
        self.txt_c1.grid(column=0,row=4)
        self.txt_c2.grid(column=2,row=4)
        self.c1.grid(column=0,row=6,sticky="nesw")
        self.c2.grid(column=2,row=6,sticky="nesw")
        self.button.grid(column=0,row=8,columnspan=3,sticky="nesw")
        self.c1.current(0)
        self.c2.current(0)

    def _validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if len(value_if_allowed)==0:
            return True
        if text in '0123456789':
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    def _start_game(self):
        win=[0,0]
        times=(int)(self.text.get())
        for i in range(times):
            self.gd_parent.game_start(3,c1=self.c1.get(),c2=self.c2.get())
            winner=-1
            while winner==-1:
                winner,reward,poss_next_steps=next(self.gd_parent.game_loop)
                if winner!=-1:
                    break
            if winner!=2:
                win[winner]+=1
        self.grid_forget()
        self.controller.show_frame("CvC_Game_over_interface",5,{"win":win})
        self.first_play=False
        
        

        
class Game_interface(Interface):
    def __init__(self, parent, controller,gd_parent):
        super().__init__(parent, controller,gd_parent)
        self.first_play=True
        self.board=[]
        self.col_index=[]
        self.row_index=[]
        self.rewards=[]
        
    def init_play(self,mode):
        self.gd_parent.game_start(mode)
        '''self._init_GUI(board,reward,poss_next_steps)
        if mode==2:#PvC
            winner,reward,poss_next_steps=next(self.gd_parent.game_loop)'''
        
    def init_GUI(self,board,reward,poss_next_steps):
        if self.first_play:
            for row,r in zip(board,range(len(board))):
                wid_row=[]
                for ele,c in zip(row,range(len(row))):
                    if ele==-1:
                        if (r,c) in poss_next_steps:
                            wid_row.append([tk.Button(self, text = '．',
                                                     font=self.controller.title_font,
                                                     width=2,height=1,
                                                     command=lambda x=r,y=c: self._placing_disk(x,y)),r+2,c+1])
                        else:
                            wid_row.append([tk.Button(self, text = '　',
                                                     font=self.controller.title_font,
                                                     width=2,height=1,
                                                     command=lambda x=r,y=c: self._placing_disk(x,y)),r+2,c+1])
                    elif ele==0:
                        wid_row.append([tk.Button(self, text = '○',
                                                 font=self.controller.title_font,
                                                 width=2,height=1,
                                                 command=lambda x=r,y=c: self._placing_disk(x,y)),r+2,c+1])
                    elif ele==1:
                        wid_row.append([tk.Button(self, text = '●',
                                                 font=self.controller.title_font,
                                                 width=2,height=1,
                                                 command=lambda x=r,y=c: self._placing_disk(x,y)),r+2,c+1])
                self.board.append(wid_row)
            for i in range(8):
                self.col_index.append([ tk.Label(self, text=str(i+1),
                                        font=self.controller.title_font,
                                        width=2,height=1),i+2,0])
            for i in range(8):
                self.row_index.append([ tk.Label(self, text=chr(ord('A') + i),
                                        font=self.controller.title_font,
                                        width=2,height=1),1,i+1])
            self.rewards.append([tk.Label(self, text="2",font=self.controller.title_font,width=2,height=1),0,7])
            self.rewards.append([tk.Label(self, text='2',font=self.controller.title_font,width=2,height=1),0,3])
            self.rewards.append([tk.Label(self, text="○",font=self.controller.title_font,width=2,height=1),0,5])
            self.rewards.append([tk.Label(self, text='●',font=self.controller.title_font,width=2,height=1),0,1])
            self._widgets_grid()
        else:
            self._change_reward_text(who=0,text="2")
            self._change_reward_text(who=1,text="2")
            for row,r in zip(board,range(len(board))):
                for ele,c in zip(row,range(len(row))):
                    if ele==-1:
                        if (r,c) in poss_next_steps:
                            self._change_board_text(r,c,'．')
                        else:
                            self._change_board_text(r,c,'　')
                    elif ele==0:
                        self._change_board_text(r,c,'○')
                    elif ele==1:
                        self._change_board_text(r,c,'●')
        
        
    def _widgets_grid(self):
        for row,num_row in zip(self.board,range(len(self.board))):
            for ele,num_col in zip(row,range(len(row))):
                ele[0].grid(column=ele[2],row=ele[1],sticky="nesw")
        for ele in self.col_index:
            ele[0].grid(column=ele[2],row=ele[1],sticky="nesw")
        for ele in self.row_index:
            ele[0].grid(column=ele[2],row=ele[1],sticky="nesw")
        for ele in self.rewards:
            ele[0].grid(column=ele[2],row=ele[1],columnspan=2,sticky="nesw")
                
                
    def _update_desks(self,change_desks,text):
        for step in change_desks:
            self._change_board_text(step[0],step[1],text)
            
    def _update_after_placing(self,turn,change_disks,poss_last_steps):
        if turn==1:
            text="●"
        else:
            text="○"
        poss_last_steps-=change_disks
        self._update_desks(change_disks,text)
        self._update_desks(poss_last_steps,' ')
        
    def _change_board_text(self,row,col,text):
        self.board[row][col][0].configure(text=text)
    def _change_reward_text(self,who,text):
        self.rewards[who][0].configure(text=text)
        
    def _placing_disk(self,row,col):
        if self.gd_parent.check_valid_step((row,col)):
            turn,change_disks,poss_last_steps=self.gd_parent.placing_disk((row,col))
            self._update_after_placing(turn,change_disks,poss_last_steps)
            winner,reward,poss_next_steps=next(self.gd_parent.game_loop)
            '''self._change_reward_text(0,str(reward[0]))
            self._change_reward_text(1,str(reward[1]))
            if winner>-1:
                self._game_over()
            self._update_desks(poss_next_steps,'．')'''
            
    def game_over(self,winner,reward):
        self.grid_forget()
        self.controller.show_frame("Game_over_interface",4,{"winner":winner,"rewards":reward})
        self.first_play=False
