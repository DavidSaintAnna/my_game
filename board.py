import random
from tkinter import *
from tkinter import messagebox
from typing import Dict

from PIL import Image as PILImage
from PIL import ImageTk

root = Tk()
root.geometry("1400x1200")
root.title("板 Memo")
root.iconbitmap("c:/Users/david/Documents/MyGame/images/icon.ico")

my_img = ImageTk.PhotoImage(
    PILImage.open("c:/Users/david/Documents/MyGame/images/card.jpg")
)

image_paths = [
    "c:/Users/david/Documents/MyGame/images/V1_001_.png",
    "c:/Users/david/Documents/MyGame/images/V1_001_.png",
    "c:/Users/david/Documents/MyGame/images/V1_002_.png",
    "c:/Users/david/Documents/MyGame/images/V1_002_.png",
    "c:/Users/david/Documents/MyGame/images/V1_005_.png",
    "c:/Users/david/Documents/MyGame/images/V1_005_.png",
    "c:/Users/david/Documents/MyGame/images/V1_006_.png",
    "c:/Users/david/Documents/MyGame/images/V1_006_.png",
    "c:/Users/david/Documents/MyGame/images/V1_007_.png",
    "c:/Users/david/Documents/MyGame/images/V1_007_.png",
    "c:/Users/david/Documents/MyGame/images/V1_008_.png",
    "c:/Users/david/Documents/MyGame/images/V1_008_.png",
    "c:/Users/david/Documents/MyGame/images/V1_009_.png",
    "c:/Users/david/Documents/MyGame/images/V1_009_.png",
    "c:/Users/david/Documents/MyGame/images/V1_011_.png",
    "c:/Users/david/Documents/MyGame/images/V1_011_.png",
    "c:/Users/david/Documents/MyGame/images/V1_014_.png",
    "c:/Users/david/Documents/MyGame/images/V1_014_.png",
    "c:/Users/david/Documents/MyGame/images/V1_018_.png",
    "c:/Users/david/Documents/MyGame/images/V1_018_.png",
    "c:/Users/david/Documents/MyGame/images/V1_021_.png",
    "c:/Users/david/Documents/MyGame/images/V1_021_.png",
    "c:/Users/david/Documents/MyGame/images/V1_030_.png",
    "c:/Users/david/Documents/MyGame/images/V1_030_.png",
    "c:/Users/david/Documents/MyGame/images/V1_031_.png",
    "c:/Users/david/Documents/MyGame/images/V1_031_.png",
    "c:/Users/david/Documents/MyGame/images/V1_032_.png",
    "c:/Users/david/Documents/MyGame/images/V1_032_.png",
    "c:/Users/david/Documents/MyGame/images/V1_033_.png",
    "c:/Users/david/Documents/MyGame/images/V1_033_.png",
    "c:/Users/david/Documents/MyGame/images/V1_034_.png",
    "c:/Users/david/Documents/MyGame/images/V1_034_.png",
    "c:/Users/david/Documents/MyGame/images/V1_036_.png",
    "c:/Users/david/Documents/MyGame/images/V1_036_.png",
    "c:/Users/david/Documents/MyGame/images/V1_037_.png",
    "c:/Users/david/Documents/MyGame/images/V1_037_.png",
]

random.shuffle(image_paths)


def update_image_paths(level):
    # Shuffle the image paths and take the first `level * level / 2` paths, then double them to create pairs
    shuffled_paths = random.sample(image_paths, level * level // 2)
    return shuffled_paths * 2  # Double the paths to create pairs


def create_buttons(level):
    buttons = []
    global image_objects  # Make image_objects global

    image_objects = [
        ImageTk.PhotoImage(PILImage.open(path)) for path in update_image_paths(level)
    ]

    for row in range(level):
        button_row = []
        for col in range(level):
            button = Button(
                text=" ",
                height=110,
                width=110,
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
    for widget in buttons_frame.winfo_children():
        widget.destroy()

    buttons = create_buttons(level)
    return buttons


count = 0
matched_pairs = 0
current_level = 2  # Starting level
buttons_frame = Frame(root)
buttons_frame.grid(row=0, column=0)

buttons = create_buttons(current_level)  # Initialize buttons


def flip_back():
    for button in unmatched_buttons:
        button["image"] = my_img
        button["text"] = " "
    unmatched_buttons.clear()


unmatched_buttons = []
answer_list = []
answer_dict = {}


def button_click(b, number):
    global count, answer_list, answer_dict, unmatched_buttons, matched_pairs, current_level
    new_list = update_image_paths(current_level)

    if b["text"] == " " and count < 2:
        b["image"] = image_objects[number]
        b["text"] = str(number)
        answer_dict[b] = image_paths[number]
        count += 1

        if len(new_list) == 4:
            if new_list[0] == new_list[1]:
                messagebox.showinfo("板 Memo", "YOU RIGHT!")
                for key in answer_dict:
                    key["state"] = "disabled"
                count = 0
                answer_list = []
                answer_dict = {}
                matched_pairs += 1

                if matched_pairs == current_level * current_level:
                    if current_level == 6:  # Maximum level reached
                        messagebox.showinfo("板 Memo", "Congratulations! You Won!")
                    else:
                        current_level += 1
                        buttons = update_grid(
                            buttons_frame, current_level
                        )  # Update grid
                        matched_pairs = 0

            else:
                messagebox.showinfo("板 Memo", "hmph..WRONG!")
                unmatched_buttons = [key for key in answer_dict]
                root.after(1000, flip_back)
                count = 0
                answer_list = []
                for key in answer_dict:
                    key["text"] = " "
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
