from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
FONT_LANG = ('Arial', 40, 'italic')
FONT_TRANSLATION = ('Arial', 60, 'bold')


try:
    words_to_learn = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    words_to_learn = pandas.read_csv('data/french_words.csv')

data_dict = words_to_learn.to_dict(orient='records')
global indexes


def generate_index():
    index = random.randint(0, len(data_dict))
    return index


def words_learned():
    data_dict.remove(data_dict[indexes])
    generate_word()


def card_flip():
    canvas.itemconfig(front_card, image=card_back_image)
    canvas.itemconfig(word_lang, text='English', fill='white')
    english_translation = data_dict[indexes]['English']
    canvas.itemconfig(word_translation, text=english_translation, fill='white')


def generate_word():
    global timer
    window.after_cancel(timer)
    indexes = generate_index()
    canvas.itemconfig(front_card, image=front_card_image)
    french_word = data_dict[indexes]['French']
    canvas.itemconfig(word_lang, text='French', fill='black')
    canvas.itemconfig(word_translation, text=french_word, fill='black')
    timer = window.after(3000, func=card_flip)


window = Tk()
window.title('Flash Card')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, func=card_flip)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_card_image = PhotoImage(file='images/card_front.png')
card_back_image = PhotoImage(file='images/card_back.png')
front_card = canvas.create_image(400, 263, image=front_card_image)
canvas.grid(row=0, column=0, columnspan=2)

word_lang = canvas.create_text(400, 150, text='', font=FONT_LANG, fill='black')
word_translation = canvas.create_text(400, 263, text='', font=FONT_TRANSLATION, fill='black')

x_image = PhotoImage(file='images/wrong.png')
x_button = Button(image=x_image, highlightthickness=0, command=generate_word)
x_button.grid(row=1, column=0)

check_image = PhotoImage(file='images/right.png')
check_button = Button(image=check_image, highlightthickness=0, command=words_learned)
check_button.grid(row=1, column=1)

generate_word()

window.mainloop()

to_learn = pandas.DataFrame(data_dict)
to_learn.to_csv('data/words_to_learn.csv', index=False)
