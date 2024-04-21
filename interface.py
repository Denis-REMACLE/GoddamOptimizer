import tkinter as tk
import GoddamOptimizer as GO
import pynomadopti  as PNO

window = tk.Tk()

def open_window(): #Programmation Dynamique
    window = tk.Toplevel()
    window.attributes('-topmost', True)
    label = tk.Label(window, text="Voici une nouvelle fenêtre!")
    label.pack(pady=20)
    window.bind('<Return>', lambda event: window.destroy())


def open_window2(): #NOMAD
    window = tk.Toplevel()
    window.attributes('-topmost', True)
    label = tk.Label(window, text="Voici une autre nouvelle fenêtre!")
    label.pack(pady=20)
    window.bind('<Return>', lambda event: window.destroy())


def programmation_dynamique():
    ...


def nomad():
    ...


label1 =tk.Label(text="Elevation Totale")
label2 = tk.Label(text="Debit Total")
entry1 = tk.Entry(fg="white", bg="grey", width=50)
entry2 = tk.Entry(fg="white", bg="grey", width=50)

button1 = tk.Button(
    text="Programmation Dynamique",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=open_window
)
button2 = tk.Button(
    text="NOMAD",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=open_window2
)



label1.pack()
entry1.pack()
label2.pack()
entry2.pack()
button1.pack()
button2.pack()
