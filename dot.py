from tkinter import *
import numpy as np
size_of_board=600
distance_between_dots=100
dot_width=50
number_of_dots = 5
player1_color='#0492CF'
player2_clor='#EE4035'

class dot_and_lines:
    # initializing the game
    def __init__(self):
        self.window = Tk()
        self.window.title('chuka chuka kalipitae bokka')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.setup()

    def mainloop(self):
        self.window.mainloop()
    # sets the board
    def setup(self):
        for i in range(number_of_dots):
            x = i * distance_between_dots + distance_between_dots
            self.canvas.create_line(x, distance_between_dots , x,
                                    size_of_board - distance_between_dots ,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(distance_between_dots, x,
                                    size_of_board - distance_between_dots, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i * distance_between_dots + distance_between_dots
                end_x = j * distance_between_dots + distance_between_dots
                self.canvas.create_oval(start_x - dot_width / 2, end_x - dot_width / 2, start_x + dot_width / 2,
                                        end_x + dot_width / 2, fill='#000000',
                                        outline='#000000')
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))
        self.player1_score = 0
        self.player2_score = 0
        self.player_color=player1_color
        self.player1_turn=True
        self.canvas.create_text(130, 30, font="cmr 40 bold ", fill=player1_color, text='player 1')
        self.canvas.create_text(400, 30, font="cmr 40 bold", fill=player2_clor, text='player 2')
        self.textid=self.canvas.create_text(250, 560, font="cmr 40 bold", fill='#000000', text='player 1\'s chance ',tag='some')

    # converting the mouse click into index numbers
    def conversion(self,x,y):
        x=(x-75)//50
        y=(y-75)//50
        type = False
        r=-1
        c=-1
        if y % 2 == 0 and (x - 1) % 2 == 0:
            r = int((x - 1) // 2)
            c = int(y // 2)
            type = 'row'

        elif x % 2 == 0 and (y - 1) % 2 == 0:
            c = int((y - 1) // 2)
            r = int(x // 2)
            type = 'col'

        return r,c, type
    # updates the status
    def update_status(self,r,c,type):
        val=1
        self.double = False
        if type=='row':
           if self.row_status[c][r]==1:
               val=0
               self.double=True
        elif type=='col':
            if self.col_status[c][r] == 1:
                val = 0
                self.double = True
        self.prev = self.board_status.copy()
        if c < (number_of_dots - 1) and r < (number_of_dots - 1):
            self.board_status[c][r] += val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c - 1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r - 1] += val

        print(self.board_status,self.row_status,self.col_status)
    # draws the line after click
    def draw_lines(self,r,c,type):
        if type == 'row':
            start_x = distance_between_dots  + r * distance_between_dots
            end_x = start_x + distance_between_dots
            start_y = distance_between_dots  + c * distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots  + c * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots  + r * distance_between_dots
            end_x = start_x
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill='#000000', width=3)
        if(not self.double):
            if self.player1_turn:
               self.player1_turn=False
            else:
               self.player1_turn=True

        if not self.player1_turn:
            self.player_color=player1_color
        else:
            self.player_color=player2_clor

        if self.player1_turn :
            chance = 'player 1\'s chance '
        else:
            chance = 'player 2\'s chance '
        self.canvas.delete('some')
        self.textid=self.canvas.create_text(250, 560, font="cmr 40 bold", fill='#000000', text=chance,tag='some')
    # fills the box if it is lined on four sides
    def fill_box(self):
        # print(self.prev,self.board_status)
        arr=[]
        for i in range(0,4):
            for j in range(0,4):
                if self.prev[i][j]!=self.board_status[i][j] and self.board_status[i][j]==4:
                    arr.append([i,j])
        # print(arr)
        for k in arr:
            r=k[1]
            c=k[0]
            start_x = distance_between_dots + r * distance_between_dots
            start_y = distance_between_dots + c * distance_between_dots
            end_x=start_x+100
            end_y=start_y+100
            self.canvas.create_rectangle(start_x+10, start_y+10, end_x-10, end_y-10, fill=self.player_color, outline='')
            if(self.player_color==player1_color):
                self.player1_score+=1
            elif self.player_color==player2_clor:
                self.player2_score+=1
            if not self.player1_turn:
                self.player1_turn=True
            elif  self.player1_turn:
                self.player1_turn=False

            if self.player1_turn:
                chance = 'player 1 again'
            else:
                chance = 'player 2 again'
            self.canvas.delete('some')
            self.textid = self.canvas.create_text(250, 560, font="cmr 40 bold", fill='#000000', text=chance, tag='some')
    # tells wether is game over
    def is_game_over(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    def result(self):
        if(self.player1_score>self.player2_score):
            some_text='player 1 wins'
        elif(self.player1_score<self.player2_score):
            some_text = 'player 2 wins'
        else:
            some_text='Draw'
        self.canvas.delete('some')
        self.canvas.create_text(250, 560, font="cmr 40 bold", fill='#000000', text=some_text)

    def click(self,event):
        # print(event.x, event.y)
        row,colou,typo=self.conversion(event.x,event.y)
        # print(row,colou,typo)
        if typo:
            self.update_status(row,colou,typo)
            self.draw_lines(row,colou,typo)
            self.fill_box()

        if self.is_game_over():
            self.result();
        #print(self.board_status,self.row_status,self.col_status)

# inistatiating the game
game_instance = dot_and_lines()
game_instance.mainloop()