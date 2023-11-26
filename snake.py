import pygame
import time
import random
import os
import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog
from configparser import ConfigParser

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.config = ConfigParser()
        self.load_config()
        self.initialize_display()

    def load_config(self):
        if not os.path.exists('SnakeSettings.ini'):
            with open('SnakeSettings.ini', 'a') as f:
                f.write("[colors]\nsnake_color_red = 0\nsnake_color_green = 255\nsnake_color_blue = 0\nbackground_color_red = 0\nbackground_color_green = 0\nbackground_color_blue = 0\n[settings]\npass_through_walls = false\nsnake_speed = 15")
                f.close()
        self.config.read('SnakeSettings.ini')

    def initialize_display(self):
        self.width, self.height = 800, 600
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.font = pygame.font.SysFont(None, 35)
        self.snake_block = 20
        self.board_size = (self.width // self.snake_block, self.height // self.snake_block)
        self.apple_pos = [0, 0]
        self.wrap_around = self.config.getboolean('settings', 'pass_through_walls')
        self.snake_speed = int(self.config.get('settings', 'snake_speed'))
        self.snake_color = (
            int(self.config.get('colors', 'snake_color_red')),
            int(self.config.get('colors', 'snake_color_green')),
            int(self.config.get('colors', 'snake_color_blue'))
        )
        self.background_color = (
            int(self.config.get('colors', 'background_color_red')),
            int(self.config.get('colors', 'background_color_green')),
            int(self.config.get('colors', 'background_color_blue'))
        )

    def our_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.display, self.snake_color, [x[0], x[1], self.snake_block, self.snake_block])

    def message(self, msg, color, y_offset=0):
        mesg = self.font.render(msg, True, color)
        self.display.blit(mesg, [self.width / 6, self.height / 3 + y_offset])

    def game_loop(self):
        game_over = False
        game_close = False
        x1, y1 = self.width / 2, self.height / 2
        x1_change, y1_change = 0, 0
        snake_list = []
        length_of_snake = 1
        self.apple_pos = [round(random.randrange(0, self.board_size[0]) * self.snake_block),
                          round(random.randrange(0, self.board_size[1]) * self.snake_block)]

        while not game_over:
            while game_close:
                self.display.fill(self.background_color)
                self.message("You Lost! Press C to Play Again or Q to Quit", (255, 0, 0))
                self.message("Your Score Was " + str(length_of_snake), (0, 255, 0), 100)
                self.our_snake(snake_list)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            self.settings()
                        elif event.key == pygame.K_q:
                            return False
                        elif event.key == pygame.K_c:
                            return True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change == 0:
                        x1_change = -self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change == 0:
                        x1_change = self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change == 0:
                        y1_change = -self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change == 0:
                        y1_change = self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_s:
                        self.settings()

            if not self.wrap_around:
                if x1 >= self.width or x1 < 0 or y1 >= self.height or y1 < 0:
                    game_close = True
            else:
                if x1 >= self.width:
                    x1 = 0
                elif x1 < 0:
                    x1 = self.width - self.snake_block

                if y1 >= self.height:
                    y1 = 0
                elif y1 < 0:
                    y1 = self.height - self.snake_block

            x1 += x1_change
            y1 += y1_change
            self.display.fill(self.background_color)
            pygame.draw.rect(self.display, (255, 0, 0), [self.apple_pos[0], self.apple_pos[1], self.snake_block, self.snake_block])
            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            self.our_snake(snake_list)
            mesg = self.font.render("Score: " + str(length_of_snake), True, (0, 255, 0))
            text_width, text_height = self.font.size("Score: " + str(length_of_snake))
            self.display.blit(mesg, [(self.width - text_width) // 2, 0 + 10])

            pygame.display.update()

            if x1 == self.apple_pos[0] and y1 == self.apple_pos[1]:
                self.apple_pos = [round(random.randrange(0, self.board_size[0]) * self.snake_block),
                                  round(random.randrange(0, self.board_size[1]) * self.snake_block)]
                length_of_snake += 1

            pygame.time.Clock().tick(self.snake_speed)

        pygame.quit()
        quit()

    def settings(self):
        settings_window = tk.Tk()
        settings_window.title("Settings")

        def change_snake_color():
            color = colorchooser.askcolor(title="Choose Snake Color")
            if color[1]:
                self.snake_color = tuple(map(int, color[0]))
                self.config.set('colors', 'snake_color_red', str(self.snake_color[0]))
                self.config.set('colors', 'snake_color_green', str(self.snake_color[1]))
                self.config.set('colors', 'snake_color_blue', str(self.snake_color[2]))

        def change_background_color():
            color = colorchooser.askcolor(title="Choose Background Color")
            if color[1]:
                self.background_color = tuple(map(int, color[0]))
                self.config.set('colors', 'background_color_red', str(self.background_color[0]))
                self.config.set('colors', 'background_color_green', str(self.background_color[1]))
                self.config.set('colors', 'background_color_blue', str(self.background_color[2]))

        def toggle_wrap_around():
            self.wrap_around = not self.wrap_around
            self.config.set('settings', 'pass_through_walls', str(self.wrap_around))

        def save(speed):
            if speed:
                self.snake_speed = int(speed)
                self.config.set('settings', 'snake_speed', speed)

            settings_window.destroy()
            self.config.write(open('SnakeSettings.ini', 'w'))

        def is_integer(i):
            return i.isdigit()

        snake_color_button = tk.Button(settings_window, text="Snake Color", command=change_snake_color)
        snake_color_button.pack(pady=10)

        background_color_button = tk.Button(settings_window, text="Background Color", command=change_background_color)
        background_color_button.pack(pady=10)

        wrap_around_var = tk.BooleanVar()
        wrap_around_var.set(self.wrap_around)
        wrap_around_checkbox = tk.Checkbutton(settings_window, text="Pass Through Walls", variable=wrap_around_var,
                                              command=toggle_wrap_around)
        wrap_around_checkbox.pack(pady=10)

        reg = settings_window.register(is_integer)
        speed_label = tk.Label(settings_window, text="Snake Speed (current: " + str(self.snake_speed) + ")")
        speed_label.pack(pady=10)
        speed_entry = tk.Entry(settings_window, validate='key', validatecommand=(reg, '%P'))
        speed_entry.pack()
        update_button = tk.Button(settings_window, text="Save", command=lambda: save(speed_entry.get()))
        update_button.pack(pady=10)
        cancel_button = tk.Button(settings_window, text="Cancel", command=settings_window.destroy)
        cancel_button.pack()
        settings_window.mainloop()

# Instantiate the SnakeGame class
snake_game = SnakeGame()

while True:
    if not snake_game.game_loop():
        break
