import os
from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
french_word = ""
english_word = ""
card_flipped = None
words_data = None
words_dict = []
random_word = {}


def generate_dict():
    global words_data, words_dict
    try:
        words_data = pandas.read_csv("./data/words_to_learn.csv")
    except FileNotFoundError:
        words_data = pandas.read_csv("./data/french_words.csv")
        words_dict = words_data.to_dict("records")
    except pandas.errors.EmptyDataError:
        pass
    else:
        words_dict = words_data.to_dict("records")


# Generate Random Word
def new_word():
    global french_word, english_word, random_word
    random_word = random.choice(words_dict)
    french_word = random_word['French']
    english_word = random_word['English']


def next_card():
    global card_flipped

    if not words_dict:
        os.remove("./data/words_to_learn.csv")
        generate_dict()

    if card_flipped is not None:
        window.after_cancel(card_flipped)

    new_word()
    canvas.itemconfig(canvas_img, image=front_card_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=french_word, fill="black")
    card_flipped = window.after(3000, flip_card)


# Timer
def flip_card():
    canvas.itemconfig(canvas_img, image=back_card_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=english_word, fill="white")


def correct_answer():
    words_dict.remove(random_word)
    export_data = pandas.DataFrame(words_dict)
    export_data.to_csv("./data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Ultimate Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

front_card_img = PhotoImage(file="./images/card_front.png")
back_card_img = PhotoImage(file="./images/card_back.png")
correct_image = PhotoImage(file="./images/right.png")
wrong_image = PhotoImage(file="./images/wrong.png")

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_img = canvas.create_image(400, 263, image=front_card_img)
title_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 253, text="Word", font=("Ariel", 60, "bold"))

# Buttons
correct_button = Button(image=correct_image, highlightthickness=0, border=0, command=correct_answer)
wrong_button = Button(image=wrong_image, highlightthickness=0, border=0, command=next_card)

# Layout
canvas.grid(column=0, columnspan=2, row=0)
correct_button.grid(column=1, row=1)
wrong_button.grid(column=0, row=1)

if words_data is None:
    generate_dict()

next_card()
window.mainloop()
