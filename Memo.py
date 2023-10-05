import random
from tkinter import *
from tkinter import messagebox
from typing import Dict

from PIL import Image as PILImage
from PIL import ImageTk


class GameClass:
    def __init__(self):
        self.root = Tk()
        self.app_width = 1400
        self.app_height = 1200
        self.root.geometry(f"{self.app_width}x{self.app_height}")
        self.root.title("板 Memo")
        self.root.iconbitmap("images/icon.ico")

        self.bg = PILImage.open("images/09909.png")
        self.bg = self.bg.resize((self.app_width, self.app_height))
        self.bg = ImageTk.PhotoImage(self.bg)

        self.image_paths = [
            "images/V1_001_.png",
            "images/V1_002_.png",
            "images/V1_005_.png",
            "images/V1_006_.png",
            "images/V1_007_.png",
            "images/V1_008_.png",
            "images/V1_009_.png",
            "images/V1_011_.png",
            "images/V1_014_.png",
            "images/V1_018_.png",
            "images/V1_021_.png",
            "images/V1_030_.png",
            "images/V1_031_.png",
            "images/V1_032_.png",
            "images/V1_033_.png",
            "images/V1_034_.png",
            "images/V1_036_.png",
            "images/V1_037_.png",
            "images/V1_038_.png",
            "images/V1_039_.png",
            "images/V1_042_.png",
            "images/V1_043_.png",
            "images/V1_046_.png",
            "images/V1_047_.png",
            "images/V1_048_.png",
            "images/V1_050_.png",
            "images/V1_051_.png",
            "images/V1_052_.png",
            "images/V1_053_.png",
            "images/V1_054_.png",
            "images/V1_055_.png",
            "images/V1_056_.png",
            "images/V1_057_.png",
            "images/V1_058_.png",
        ]
        self.minutes = 14
        self.seconds = 59
        self.my_img = ImageTk.PhotoImage(PILImage.open("images/card.jpg"))
        self.answer_dict = {}
        self.unmatched_buttons = []
        self.buttons = []
        self.image_objects = []
        self.levels_image_path = []
        self.matched_pairs = 0
        self.check = False
        self.current_level = 2
        self.answer_list = []
        self.bg_image = PILImage.open("images/0546444e.png")
        self.bg_image = self.bg_image.resize((self.app_width, self.app_height))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.my_label = Label(self.root, image=self.bg)
        self.my_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_widgets()

        random.shuffle(self.image_paths)

        # Additional setup code goes here

    def create_widgets(self):
        # Create frames
        self.buttons_frame = Frame(self.root)
        self.buttons_frame.grid(row=0, column=0)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.timer_frame = Frame(self.root)
        self.timer_frame.grid(row=0, column=0, sticky="nw", padx=(10, 0), pady=(10, 0))

        # Create labels
        self.minutes_var = StringVar(value=str(self.minutes).zfill(2))
        self.seconds_var = StringVar(value=str(self.seconds).zfill(2))

        self.minutes_label = Label(
            self.timer_frame, textvariable=self.minutes_var, font=("Helvetica", 50)
        )
        self.minutes_label.grid(row=0, column=0)

        self.separator_label = Label(self.timer_frame, text=":", font=("Helvetica", 30))
        self.separator_label.grid(row=0, column=1, sticky="nw", pady=(10, 0))

        self.seconds_label = Label(
            self.timer_frame, textvariable=self.seconds_var, font=("Helvetica", 50)
        )
        self.seconds_label.grid(row=0, column=2, padx=(10, 0))

        # Create start button
        self.start_button = Button(
            self.buttons_frame,
            text="Start Game",
            font=("Helvetica", 16),
            command=self.start_game,
        )
        self.start_button.grid(row=1, column=1, pady=(20, 0))

        # Create welcome frame
        self.welcome_frame = Frame(
            self.root, width=self.app_width, height=self.app_height
        )
        self.welcome_frame.grid(row=0, column=0, sticky="nsew")

        self.canvas = Canvas(
            self.welcome_frame, width=self.app_width, height=self.app_height
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=NW, image=self.bg_image)

        self.start_button = Button(
            self.canvas,
            text="Start Game",
            font=("Helvetica", 16),
            command=self.start_game,
        )
        self.start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    def countdown(self):
        minutes = int(self.minutes_var.get())
        seconds = int(self.seconds_var.get())

        def update_timer():
            nonlocal minutes, seconds
            if minutes == 0 and seconds == 0:
                messagebox.showinfo("板 Memo", "Game Over! MWHAHAHA!")
                self.reset_game()
                return
            if seconds == 0:
                minutes -= 1
                seconds = 59
            else:
                seconds -= 1

            self.minutes_var.set(str(minutes).zfill(2))
            self.seconds_var.set(str(seconds).zfill(2))
            self.root.after(1000, update_timer)

        update_timer()

    def shuffle_array(self, arr):
        shuffled = arr.copy()
        n = len(shuffled)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        return shuffled

    def update_image_paths(self, level):
        # Shuffle the image paths and take the first `level * level / 2` paths, then double them to create pairs
        shuffled_paths = random.sample(self.image_paths, level * level // 2)
        return self.shuffle_array(
            shuffled_paths * 2
        )  # Double the paths to create pairs

    def create_buttons(self, level):
        self.buttons = []
        self.levels_image_path = self.update_image_paths(level)
        self.image_objects = [
            ImageTk.PhotoImage(PILImage.open(path)) for path in self.levels_image_path
        ]

        for row in range(level):
            button_row = []
            for col in range(level):
                button = Button(
                    self.buttons_frame,
                    text=" ",
                    height=85,
                    width=85,
                    image=self.my_img,
                    command=lambda row=row, col=col: self.button_click(
                        self.buttons[row][col], row * level + col
                    ),
                )
                button.grid(row=row, column=col)

                button_row.append(button)

            self.buttons.append(button_row)

        return self.buttons

    def update_grid(self, level):
        self.current_level = level
        self.levels_image_path = self.update_image_paths(level)
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        self.buttons = self.create_buttons(level)
        self.buttons_frame.grid(row=0, column=0)
        return self.buttons, self.current_level

    def reset_game(self):
        self.current_level = 2
        self.matched_pairs = 0
        self.minutes = 14
        self.seconds = 59
        self.minutes_var.set(str(self.minutes).zfill(2))
        self.seconds_var.set(str(self.seconds).zfill(2))
        self.answer_list = []
        self.answer_dict = {}
        self.unmatched_buttons = []
        self.buttons = []
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        buttons = self.create_buttons(self.current_level)
        self.welcome_frame.grid(row=0, column=0, sticky="nsew")

    def run(self):
        self.root.mainloop()

    def flip_back(self):
        self.check = False
        for button in self.unmatched_buttons:
            button["image"] = self.my_img
            button["text"] = " "
        self.unmatched_buttons.clear()

    def button_click(self, button, number):
        if self.check:
            return
        if button["text"] == " " and len(self.answer_list) < 2:
            button["image"] = self.image_objects[number]
            button["text"] = str(number)

            self.answer_dict[button] = self.levels_image_path[number]
            self.answer_list.append(self.levels_image_path[number])
            if len(self.answer_list) == 2:
                if self.answer_list[0] == self.answer_list[1]:
                    messagebox.showinfo("板 Memo", "YOU RIGHT!")

                    for button in self.answer_dict:
                        button["state"] = "disabled"

                    self.answer_list = []
                    self.answer_dict = {}

                    self.matched_pairs += 1

                    if (
                        self.matched_pairs
                        == self.current_level * self.current_level / 2
                    ):
                        if self.current_level == 8:
                            messagebox.showinfo("板 Memo", "Congratulations! You Won!")
                        else:
                            buttons, self.current_level = self.update_grid(
                                self.buttons_frame, self.current_level + 2
                            )
                            self.matched_pairs = 0
                else:
                    self.check = True
                    self.unmatched_buttons = [key for key in self.answer_dict]
                    self.root.after(1000, self.flip_back)
                    self.answer_list = []

                    for button in self.answer_dict:
                        button["text"] = " "

                    self.answer_dict = {}

    def start_game(self):
        self.welcome_frame.grid_forget()
        self.buttons_frame.grid(row=0, column=0)
        self.countdown()
        self.buttons = self.create_buttons(self.current_level)


if __name__ == "__main__":
    game = GameClass()
    game.run()
