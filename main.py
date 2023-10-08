import random
from tkinter import *
import pandas
import random
import time

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# ----------------------------------------------Accessing CVS File-------------------------------------#
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")



def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(image_container, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"])

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(image_container, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"])


def delete_word():
    to_learn.remove(current_card)
    save_to_csv("data/words_to_learn.csv", to_learn)
    next_card()


def save_to_csv(filename, data_list):
    df = pandas.DataFrame(data_list)
    df.to_csv(filename, index=False)


# ---------------------------------------------- UI ---------------------------------------------------#

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR)
window.config(padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
image_container = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, font=("Ariel", "40", "italic"), text="")
card_word = canvas.create_text(400, 263, font=("Ariel", "60", "bold"), text="")

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=delete_word)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
