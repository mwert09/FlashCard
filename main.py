from tkinter import *
from pandas import *
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
try:
    data = read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict('records')
new_card = {}

def get_new_word():
    global new_card, flip_timer
    window.after_cancel(flip_timer)
    new_card = random.choice(to_learn)
    canvas.itemconfig(lang, text="French", fill="black")
    canvas.itemconfig(word, text=new_card['French'], fill="black")
    canvas.itemconfig(background_img, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def is_known():
    to_learn.remove(new_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    get_new_word()

def flip_card():
    canvas.itemconfig(lang, text="English", fill="white")
    canvas.itemconfig(word, text=new_card['English'], fill="white")
    canvas.itemconfig(background_img, image=card_back_img)

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
cross_image = PhotoImage(file="images/wrong.png")
check_image = PhotoImage(file="images/right.png")

canvas = Canvas(width=800, height=526)
background_img = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
lang = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

unknown_button = Button(image=cross_image, command=get_new_word)
unknown_button.config(highlightthickness=0)
unknown_button.grid(row=1, column=0)

known_button = Button(image=check_image, command=is_known)
known_button.config(highlightthickness=0)
known_button.grid(row=1, column=1)

get_new_word()

window.mainloop()