from tkinter import *
from tkinter import PhotoImage
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def show_new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    print(current_card)
    canvas.itemconfig(title_label, text="French", fill="black")
    canvas.itemconfig(word_label, text=current_card["French"], fill="black")
    canvas.itemconfig(card_canvas, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(title_label, text="English", fill="white")
    canvas.itemconfig(word_label, text=current_card["English"], fill="white")
    canvas.itemconfig(card_canvas, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    show_new_word()


# ---------------------UI


window = Tk()
window.title("flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
card_canvas = canvas.create_image(400, 263, image=card_front_img)
title_label = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_label = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

right_button_img = PhotoImage(file="images/right.png")
wrong_button_img = PhotoImage(file="images/wrong.png")

know_button = Button(image=right_button_img, highlightthickness=0, command=is_known)
know_button.grid(row=1, column=1)

dunno_button = Button(image=wrong_button_img, highlightthickness=0, command=show_new_word)
dunno_button.grid(row=1, column=0)

show_new_word()

window.mainloop()
