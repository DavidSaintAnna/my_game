import random
from tkinter import *
from tkinter import messagebox
from typing import Dict

from PIL import Image as PILImage
from PIL import ImageTk

root = Tk()

app_width = 1400
app_height = 1200

root.geometry(f"{app_width}x{app_height}")

root.title("板 Memo")
root.iconbitmap("images/icon.ico")

my_img = ImageTk.PhotoImage(PILImage.open("images/card.jpg"))


image_paths = [
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

bg = PILImage.open("images/09909.png")
bg = bg.resize((app_width, app_height))
bg = ImageTk.PhotoImage(bg)

my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

random.shuffle(image_paths)


def shuffle_array(arr):
    shuffled = arr.copy()
    n = len(shuffled)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    return shuffled


def update_image_paths(level):
    # Shuffle the image paths and take the first `level * level / 2` paths, then double them to create pairs

    shuffled_paths = random.sample(image_paths, level * level // 2)
    return shuffle_array(shuffled_paths * 2)  # Double the paths to create pairs


levels_image_path = []


def create_buttons(level):
    buttons = []
    global levels_image_path, image_objects  # Make image_objects global
    levels_image_path = update_image_paths(level)
    image_objects = [
        ImageTk.PhotoImage(PILImage.open(path)) for path in levels_image_path
    ]

    for row in range(level):
        button_row = []
        for col in range(level):
            button = Button(
                buttons_frame,
                text=" ",
                height=85,
                width=85,
                image=my_img,
                command=lambda row=row, col=col: button_click(
                    buttons[row][col], row * level + col
                ),
            )
            button.grid(row=row, column=col)

            button_row.append(button)

        buttons.append(button_row)

    return buttons


def update_grid(buttons_frame, level):
    global current_level, levels_image_path
    current_level = level
    levels_image_path = update_image_paths(level)
    for widget in buttons_frame.winfo_children():
        widget.destroy()
    buttons = create_buttons(level)
    return buttons, current_level


count = 0
matched_pairs = 0
current_level = 2  # Starting level

buttons_frame = Frame(root)
buttons_frame.grid(row=0, column=0)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


buttons = create_buttons(current_level)  # Initialize buttons


def start_game():
    welcome_frame.grid_forget()  # Hide the welcome frame
    buttons_frame.grid(row=0, column=0)  # Show the game frame


bg_image = PILImage.open("images/0546444e.png")
bg_image = bg_image.resize((app_width, app_height))
bg_image = ImageTk.PhotoImage(bg_image)

# My Timer

minutes_var = StringVar(value="9")
seconds_var = StringVar(value="59")
timer_frame = Frame(root)
timer_frame.grid(row=0, column=0, sticky="nw", padx=(10, 0), pady=(10, 0))

minutes_label = Label(timer_frame, textvariable=minutes_var, font=("Helvetica", 50))
minutes_label.grid(row=0, column=0)
separator_label = Label(timer_frame, text=":", font=("Helvetica", 30))
separator_label.grid(row=0, column=1, sticky="nw", pady=(10, 0))
seconds_label = Label(timer_frame, textvariable=seconds_var, font=("Helvetica", 50))
seconds_label.grid(row=0, column=2, padx=(10, 0))


# Welcome Page
welcome_frame = Frame(root, width=app_width, height=app_height)
welcome_frame.grid(row=0, column=0, sticky="nsew")

canvas = Canvas(welcome_frame, width=app_width, height=app_height)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, anchor=NW, image=bg_image)
# canvas.create_text(650, 250, text="板 Memo", font=("Helvetica", 50), fill="yellow")

start_button = Button(
    canvas, text="Start Game", font=("Helvetica", 16), command=start_game
)
start_button.place(relx=0.5, rely=0.5, anchor=CENTER)


def flip_back():
    global check
    check = False
    for button in unmatched_buttons:
        button["image"] = my_img
        button["text"] = " "
    unmatched_buttons.clear()


check = False
answer_list: list = []
answer_dict = {}
unmatched_buttons = []


def button_click(button, number):
    global answer_list, answer_dict, matched_pairs, current_level, unmatched_buttons, levels_image_path, check
    if check:
        return
    if button["text"] == " " and len(answer_list) < 2:
        button["image"] = image_objects[number]
        button["text"] = str(number)

        answer_dict[button] = levels_image_path[number]
        print(answer_dict)
        answer_list.append(levels_image_path[number])
        if len(answer_list) == 2:
            if answer_list[0] == answer_list[1]:
                print(answer_list)
                messagebox.showinfo("板 Memo", "YOU RIGHT!")

                for button in answer_dict:
                    button["state"] = "disabled"

                answer_list = []
                answer_dict = {}

                matched_pairs += 1

                if matched_pairs == current_level * current_level / 2:
                    if current_level == 8:  # Maximum level reached
                        messagebox.showinfo("板 Memo", "Congratulations! You Won!")
                    else:
                        buttons, current_level = update_grid(
                            buttons_frame, current_level + 2
                        )  # Update grid
                        matched_pairs = 0
            else:
                # messagebox.showinfo("板 Memo", "hmph..WRONG!")
                check = True
                unmatched_buttons = [key for key in answer_dict]
                root.after(1000, flip_back)
                answer_list = []

                for button in answer_dict:
                    button["text"] = " "

                answer_dict = {}


root.mainloop()
# import random
# from tkinter import *
# from tkinter import messagebox
# from typing import Dict

# from PIL import Image as PILImage
# from PIL import ImageTk

# root = Tk()
# root.geometry("1400x1200")
# root.title("板 Memo")
# root.iconbitmap("c:/Users/david/Documents/MyGame/images/icon.ico")

# my_img = ImageTk.PhotoImage(
#     PILImage.open("c:/Users/david/Documents/MyGame/images/card.jpg")
# )

# image_paths = [
#     "c:/Users/david/Documents/MyGame/images/V1_001_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_001_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_002_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_002_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_005_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_005_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_006_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_006_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_007_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_007_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_008_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_008_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_009_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_009_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_011_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_011_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_014_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_014_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_018_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_018_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_021_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_021_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_030_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_030_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_031_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_031_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_032_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_032_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_033_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_033_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_034_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_034_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_036_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_036_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_037_.png",
#     "c:/Users/david/Documents/MyGame/images/V1_037_.png",
# ]

# random.shuffle(image_paths)
# image_objects = [ImageTk.PhotoImage(PILImage.open(path)) for path in image_paths]

# count = 0
# total_pairs = len(image_paths) // 2
# matched_pairs = 0
# unmatched_buttons: list = []
# answer_list: list = []
# answer_dict: dict = {}


# def flip_back():
#     for button in unmatched_buttons:
#         button["image"] = my_img
#         button["text"] = " "
#     unmatched_buttons.clear()


# def button_click(b, number):
#     global count, answer_list, answer_dict, unmatched_buttons, matched_pairs
#     if b["text"] == " " and count < 2:
#         # Set the button's image based on the shuffled image list
#         b["image"] = image_objects[number]
#         b["text"] = str(number)  # Store the index in the button's text
#         answer_list.append(image_paths[number])
#         answer_dict[b] = image_paths[number]
#         count += 1
#         print(answer_dict)
#         # print(answer_list)
#         if len(answer_list) == 2:
#             if answer_list[0] == answer_list[1]:
#                 messagebox.showinfo("板 Memo", "YOU RIGHT!")
#                 for key in answer_dict:
#                     key["state"] = "disabled"
#                 count = 0
#                 answer_list = []
#                 answer_dict = {}
#                 matched_pairs += 1
#                 if matched_pairs == total_pairs:
#                     messagebox.showinfo("板 Memo", "Congratulations! You Won!")
#             else:
#                 messagebox.showinfo("板 Memo", "hmph..WRONG!")
#                 unmatched_buttons = [key for key in answer_dict]
#                 root.after(1000, flip_back)
#                 count = 0
#                 answer_list = []
#                 for key in answer_dict:
#                     key["text"] = " "
#                 answer_dict = {}


# b0: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b0, 0)
# )
# b1: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b1, 1)
# )
# b2: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b2, 2)
# )
# b3: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b3, 3)
# )
# b4: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b4, 4)
# )
# b5: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b5, 5)
# )
# b6: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b6, 6)
# )
# b7: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b7, 7)
# )
# b8: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b8, 8)
# )
# b9: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b9, 9)
# )
# b10: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b10, 10)
# )
# b11: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b11, 11)
# )
# b12: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b12, 12)
# )
# b13: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b13, 13)
# )
# b14: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b14, 14)
# )
# b15: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b15, 15)
# )
# b16: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b16, 16)
# )
# b17: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b17, 17)
# )
# b18: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b18, 18)
# )
# b19: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b19, 19)
# )
# b20: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b20, 20)
# )
# b21: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b21, 21)
# )
# b22: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b22, 22)
# )
# b23: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b23, 23)
# )
# b24: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b24, 24)
# )
# b25: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b25, 25)
# )
# b26: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b26, 26)
# )
# b27: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b27, 27)
# )
# b28: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b28, 28)
# )
# b29: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b29, 29)
# )
# b30: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b30, 30)
# )
# b31: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b31, 31)
# )
# b32: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b32, 32)
# )
# b33: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b33, 33)
# )
# b34: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b34, 34)
# )
# b35: Button = Button(
#     text=" ", height=110, width=110, image=my_img, command=lambda: button_click(b35, 35)
# )

# b0.grid(row=0, column=0)
# b1.grid(row=0, column=1)
# b2.grid(row=0, column=2)
# b3.grid(row=0, column=3)
# b4.grid(row=0, column=4)
# b5.grid(row=0, column=5)

# b6.grid(row=1, column=0)
# b7.grid(row=1, column=1)
# b8.grid(row=1, column=2)
# b9.grid(row=1, column=3)
# b10.grid(row=1, column=4)
# b11.grid(row=1, column=5)


# b12.grid(row=2, column=0)
# b13.grid(row=2, column=1)
# b14.grid(row=2, column=2)
# b15.grid(row=2, column=3)
# b16.grid(row=2, column=4)
# b17.grid(row=2, column=5)

# b18.grid(row=3, column=0)
# b19.grid(row=3, column=1)
# b20.grid(row=3, column=2)
# b21.grid(row=3, column=3)
# b22.grid(row=3, column=4)
# b23.grid(row=3, column=5)

# b24.grid(row=4, column=0)
# b25.grid(row=4, column=1)
# b26.grid(row=4, column=2)
# b27.grid(row=4, column=3)
# b28.grid(row=4, column=4)
# b29.grid(row=4, column=5)

# b30.grid(row=5, column=0)
# b31.grid(row=5, column=1)
# b32.grid(row=5, column=2)
# b33.grid(row=5, column=3)
# b34.grid(row=5, column=4)
# b35.grid(row=5, column=5)

# root.mainloop()
