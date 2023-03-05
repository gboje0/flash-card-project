from tkinter import *

import pandas
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("data/words to learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    screen.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    selected_word = current_card["French"]
    screen_image.itemconfig(translate_title, text="french", fill="black")
    screen_image.itemconfig(translate_word, text=selected_word, fill="black")
    screen_image.itemconfig(default_card, image=card_front)
    flip_timer = screen.after(3000, func=flip_card)


def flip_card():
    screen_image.itemconfig(translate_title, text="English", fill="white")
    screen_image.itemconfig(translate_word, text=current_card["English"], fill="white")
    screen_image.itemconfig(default_card, image=card_back)


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv")
    next_card()


# ++++++++++++++++++++ux setup+++++++++++++++

screen = Tk()
screen.title("Flash Cards Translator")
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = screen.after(3000, func=flip_card)
screen_image = Canvas(width=800, height=526)
card_front = PhotoImage(file="./images/card_front.png")
default_card = screen_image.create_image(400, 263, image=card_front)
card_back = PhotoImage(file="images/card_back.png")

# titles
translate_title = screen_image.create_text(400, 130, text="", font=("Ariel", 40, "italic"))
translate_word = screen_image.create_text(400, 260, text="", font=("Ariel", 60, "bold"))
# doing_great = screen_image.create_image(400, 130, image=wrong_image)

screen_image.config(bg=BACKGROUND_COLOR, highlightthickness=0)
screen_image.grid(column=0, row=0, columnspan=2)

# button
next_word = PhotoImage(file="images/wrong.png")
next_word_button = Button(image=next_word, command=next_card)
next_word_button.grid(column=0, row=1)

correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=is_known)
correct_button.grid(column=1, row=1)

next_card()

screen.mainloop()
