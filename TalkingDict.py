from tkinter import *
from tkinter.messagebox import *
import json
from difflib import get_close_matches
import pyttsx3 as pp

engine = pp.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # [0]for male

root = Tk()
root.geometry('920x626+120+10')
root.title('Talking Dictionary by R.Revanth Raj')
root.resizable(0, 0)

meaning = ''
def search():
    global meaning
    textarea.delete(1.0, END)

    data = json.load(open("data.json"))

    word = enterwordentry.get()
    word = word.lower()
    if word in data:
        meaning = data[word]

    elif len(get_close_matches(word, data.keys())) > 0:
        close_match = get_close_matches(word, data.keys())[0]
        res = askyesno('Confirm', f'Did you mean {close_match} instead?')
        if res:
            textarea.delete(1.0, END)
            meaning = data[close_match]

        else:
            textarea.delete(1.0, END)
            showinfo("Information", "The word doesn't exist\nType a new word")
            enterwordentry.delete(0, END)
            meaning = ''


    else:
        showerror("Error", "The word doesn't exist. Please double check it.")

    if meaning != '':
        if type(meaning) == list:
            for item in meaning:
                textarea.insert(END, u'\u2022' + item + '\n\n')
        else:
            textarea.insert(END, meaning)


def wordaudio():
    engine.say(enterwordentry.get())
    engine.runAndWait()


def meaningaudio():
    engine.say(textarea.get(1.0, END))
    engine.runAndWait()


def clear():
    enterwordentry.delete(0, END)
    textarea.delete(1.0, END)


def exit():
    res = askyesno('Confirm', 'Do you want to exit?')
    if res:
        root.destroy()

    else:
        pass


bgimage = PhotoImage(file='bg.png')
bgLabel = Label(root, image=bgimage)
bgLabel.place(x=0, y=0)

enterwordLabel = Label(root, text='Enter Word', font=('castellar', 29, 'bold'), fg='red3', bg='whitesmoke')
enterwordLabel.place(x=330, y=20)

enterwordentry = Entry(root, font=('arial', 23, 'bold'), bd=8, relief=GROOVE, justify=CENTER)
enterwordentry.place(x=310, y=80)
enterwordentry.focus_set()

searchimage = PhotoImage(file='search.png')
searchButton = Button(root, image=searchimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                      command=search)
searchButton.place(x=420, y=150)

micimage = PhotoImage(file='mic.png')
micButton = Button(root, image=micimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                   command=wordaudio)
micButton.place(x=510, y=153)

meaningLabel = Label(root, text='Meaning', font=('castellar', 29, 'bold'), fg='red3', bg='whitesmoke')
meaningLabel.place(x=380, y=240)

textarea = Text(root, font=('arial', 18, 'bold'), bd=8, relief=GROOVE, height=8, width=34, wrap='word')
textarea.place(x=250, y=300)

audioimage = PhotoImage(file='microphone.png')
audioButton = Button(root, image=audioimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                     command=meaningaudio)
audioButton.place(x=330, y=555)

clearimage = PhotoImage(file='clear.png')
clearButton = Button(root, image=clearimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                     command=clear)
clearButton.place(x=460, y=555)

exitimage = PhotoImage(file='exit.png')
exitButton = Button(root, image=exitimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                    command=exit)
exitButton.place(x=590, y=555)

root.mainloop()
