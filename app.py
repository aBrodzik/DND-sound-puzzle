import tkinter as tk
from PIL import Image, ImageTk
import pygame
import threading
import time

# Initialize Pygame for sound
pygame.mixer.init()

# Load sound
click_sound = [pygame.mixer.Sound("0_C#.wav"), pygame.mixer.Sound("1_D4.wav"), pygame.mixer.Sound("2_E4.wav"),
               pygame.mixer.Sound("3_F.wav"), pygame.mixer.Sound("4_G.wav"), pygame.mixer.Sound("5_E5.wav"),
               pygame.mixer.Sound("6_B.wav"), pygame.mixer.Sound("7_C5.wav"), pygame.mixer.Sound("8_D5.wav")]
# 0 1 2
# 3 4 5
# 6 7 8

# Image paths
default_image_path = "default.png"
clicked_image_path = "clicked.png"

# Correct combination (example: top row)
correct_combination = [5, 4, 7, 2]


class ImageButton:
    def __init__(self, master, index, on_click):
        self.master = master
        self.index = index
        self.on_click = on_click
        self.clicked = False

        self.default_img = ImageTk.PhotoImage(Image.open(str(index)+".png").resize((200, 200)))
        self.clicked_img = ImageTk.PhotoImage(Image.open(str(index)+"-clicked.png").resize((200, 200)))

        self.button = tk.Button(master, image=self.default_img, command=self.click)
        self.button.grid(row=(index // 3)+1, column=index % 3)

    def click(self):
        if not self.clicked:
            self.clicked = True
            self.button.config(image=self.clicked_img)
            click_sound[self.index].play()
            self.on_click(self.index)

    def reset_image(self):
        self.button.config(image=self.default_img)
    def light_image(self):
        self.button.config(image=self.clicked_img)


class ImageGridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tablica za Goblińskim Tronem")

        for i in range(3):
                    self.grid_columnconfigure(i, weight=1)

        self.help_button = None
        self.bind("<h>", self.show_help_button)

        self.clicked_buttons = []
        self.buttons = []

        for i in range(9):
            btn = ImageButton(self, i, self.handle_click)
            self.buttons.append(btn)
            
    def show_help_button(self, event=None):
        if self.help_button is None:
            self.help_button = tk.Button(
                self,
                text="🧙 Pomoc od Boblina",
                font=("Arial", 14),
                command=self.play_boblin_melody
            )
            self.help_button.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 5))

    def handle_click(self, index):
        print(index)
        self.clicked_buttons.append(index)
        print(correct_combination)
        print(self.clicked_buttons)
        if (len(correct_combination)<=len(self.clicked_buttons)):
            if correct_combination==self.clicked_buttons:
                self.light_all_buttons()
                self.success_action()
            else:
                self.clicked_buttons = []
                self.reset_all_buttons()

    def reset_all_buttons(self):
        for btn in self.buttons:
            btn.reset_image()
            btn.clicked = False

    def light_all_buttons(self):
        for btn in self.buttons:
            btn.light_image()
            btn.clicked = True

    def success_action(self):
        # Example action: popup message
        success_popup = tk.Toplevel(self)
        pygame.mixer.Sound("succes.wav").play()
        tk.Label(success_popup, text="Sekretne przejście otwiera się...", font=("Arial", 16)).pack(padx=20, pady=20)

    def play_boblin_melody(self):
        pygame.mixer.Sound("boblinFlute.wav").play()

if __name__ == "__main__":
    app = ImageGridApp()
    app.mainloop()
