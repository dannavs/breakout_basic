import tkinter as tk
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *


class Breakout(tk.Tk):

    def __init__(self):
        Tk.__init__(self)

        self.all_game_pads = {}
        self.ball_x = 250
        self.ball_y = 350
        self.ball_move_x = 2
        self.ball_move_y = 2

        self.game_pad_width = 50
        self.game_pad_height = 10
        self.game_pad_columns = 3  # change back to 12
        self.game_pad_rows = 5  # change back to 8
        self.game_pad_list = []
        self.start_x = 40
        self.start_y = 10

        self.app_width = 800
        self.app_height = 600
        self.x_cor = (0.5 * self.winfo_screenwidth()) - (0.5 * self.app_width)
        self.y_cor = (0.5 * self.winfo_screenheight()) - (0.5 * self.app_height)
        self.geometry('%dx%d+%d+%d' % (self.app_width, self.app_height, self.x_cor, self.y_cor))
        self.focus_force()
        self.title("Basically Breakout")

        self.player_score = 0
        self.player_lives = 3

        self.lives_frame = ttk.Frame(borderwidth=10, relief='raised', width=40)
        self.lives_frame.grid(row=1, column=1)
        self.lives_label = ttk.Label(master=self.lives_frame, text=f"{self.player_lives}\nLives", justify='center',
                                     font='helvetica 24', width=15, anchor='center')
        self.lives_label.pack()

        self.center_frame = ttk.Frame(borderwidth=0, width=330)
        self.center_frame.grid(row=1, column=2)

        self.center_label = Label(master=self.center_frame, font='helvetica 20')
        self.center_label.pack()

        self.points_frame = ttk.Frame(borderwidth=10, relief='raised', width=40)
        self.points_frame.grid(row=1, column=3)
        self.points_label = ttk.Label(master=self.points_frame, text=f"{self.player_score}\npoints", justify='center',
                                      font='helvetica 24', width=15, anchor='center')
        self.points_label.pack()

        self.game_canvas = Canvas(self, width=785, height=590, background='black', borderwidth=5)
        self.game_canvas.grid(row=2, column=1, columnspan=3)

        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_coords = Label(self)
        self.mouse_coords.place(x=350, y=0)
        self.show_mouse_pos()

        self.paddle_width = 100
        self.x_user_pos = (800 / 2 - self.paddle_width / 2)
        self.user_pad = self.game_canvas.create_rectangle(self.x_user_pos,
                                                          490,
                                                          self.x_user_pos + self.paddle_width,
                                                          500,
                                                          fill='white',
                                                          outline='red',
                                                          tags='always_protect')

        self.ball = self.game_canvas.create_oval(self.ball_x - 5,
                                                 self.ball_y - 5,
                                                 self.ball_x + 5,
                                                 self.ball_y + 5,
                                                 fill='white',
                                                 tags='always_protect'
                                                 )

        self.create_pads()

        while True:
            self.show_mouse_pos()

            self.bind('<Left>', lambda e: self.move_user_pad('left'))
            self.bind('<Right>', lambda e: self.move_user_pad('right'))
            self.bind('<Escape>', lambda e: self.destroy())

            self.ball_move()

            self.game_canvas.update()
            sleep(0)

    def show_mouse_pos(self):
        self.mouse_x = self.game_canvas.winfo_pointerx() - self.game_canvas.winfo_rootx()
        self.mouse_y = self.game_canvas.winfo_pointery() - self.game_canvas.winfo_rooty()
        self.mouse_coords.config(text=f"{self.mouse_x}, {self.mouse_y}")

    def move_user_pad(self, direction):
        if direction == 'left':
            if self.game_canvas.coords(self.user_pad)[0] <= 10:
                pass
            else:
                self.game_canvas.move(self.user_pad, -20, 0)

        if direction == 'right':
            if self.game_canvas.coords(self.user_pad)[0] + self.paddle_width >= 790:
                pass
            else:
                self.game_canvas.move(self.user_pad, 20, 0)

        else:
            pass

    def ball_move(self):
        self.ball_x = self.game_canvas.coords(self.ball)[0] + 8
        self.ball_y = self.game_canvas.coords(self.ball)[1] + 8

        if self.ball_x <= 10 or self.ball_x >= 790:  # side walls bounce
            self.ball_move_x = -self.ball_move_x

        if self.ball_y <= 10:  # top wall bounce
            self.ball_move_y = -self.ball_move_y

        if self.ball_y > 515:  # escaped from the bottom
            # print("You've fallen out") # Lose a life, reset the ball/player paddle
            lost_a_life = self.game_canvas.create_text(350, 300, text="Out!", font='helvetica 50')
            if self.player_lives == 1:
                self.player_lives = 0
                self.lives_label.config(text=f"{self.player_lives}\nlives")
                self.game_canvas.create_text(350, 350, text="Game Over", font='helvetica 50')
                self.after(3000, self.destroy)


            elif self.player_lives > 1:
                self.player_lives -= 1
                if self.player_lives == 1:
                    self.lives_label.config(text=f"{self.player_lives}\nlife")
                else:
                    self.lives_label.config(text=f"{self.player_lives}\nlives")
                self.update()
                self.game_canvas.moveto(self.ball, 250, 350)
                self.ball_move_x = 2
                self.ball_move_y = 2
                self.game_canvas.after(2000, self.game_canvas.delete, lost_a_life)
                self.paddle_width = 100
                self.x_user_pos = (800 / 2 - self.paddle_width / 2)
                self.game_canvas.moveto(self.user_pad, self.x_user_pos, 490)
        else:
            pass

        if 490 <= self.ball_y + 5 <= 500 and self.game_canvas.coords(self.user_pad)[0] <= \
                self.game_canvas.coords(self.ball)[0] + 5 <= self.game_canvas.coords(self.user_pad)[2]:
            self.ball_move_y = -self.ball_move_y

            paddle_left_edge = self.game_canvas.coords(self.user_pad)[0]
            paddle_width = self.paddle_width
            ball_loc = self.game_canvas.coords(self.ball)[0] + 5

            if ball_loc <= paddle_left_edge + 0.25 * paddle_width:
                self.ball_move_x = -3
            elif ball_loc >= paddle_left_edge + 0.75 * paddle_width:
                self.ball_move_x = 3
            elif paddle_left_edge + 0.25 * paddle_width < ball_loc < paddle_left_edge + 0.75 * paddle_width:
                if self.ball_move_x > 0:
                    self.ball_move_x = 2
                else:
                    self.ball_move_x = -2

        self.game_canvas.move(self.ball, self.ball_move_x, self.ball_move_y)

        self.game_canvas.addtag_overlapping(
            'destroy_me', self.ball_x - 5, self.ball_y - 5, self.ball_x + 5, self.ball_y + 5)
        # self.game_canvas.delete('destroy_me' and 'can_destroy')
        # print(self.game_canvas.find_withtag('destroy_me'))
        # print(self.game_canvas.find_withtag('always_protect'))
        destroy_list = list(self.game_canvas.find_withtag('destroy_me'))
        always_protect_list = list(self.game_canvas.find_withtag('always_protect'))
        for x in destroy_list:
            if x in always_protect_list:
                pass
            else:
                self.game_canvas.delete(x)
                self.ball_move_y = -self.ball_move_y

    def create_pads(self):
        for y in range(0, self.game_pad_rows):
            for x in range(0, self.game_pad_columns):
                pad_object = self.game_canvas.create_rectangle(
                    (x * 300 + 100) - 100,
                    (y * 55 + 20) - 10,
                    (x * 300 + 100) + 100,
                    (y * 55 + 20) + 10,
                    fill='white',
                    tags='can_destroy'
                )


root = Breakout()
root.mainloop()
