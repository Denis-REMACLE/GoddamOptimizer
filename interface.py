import tkinter as tk
import goddamoptimiser as GO
import pynomadopti  as PNO

window = tk.Tk()

def open_window(): #Programmation Dynamique
    window = tk.Toplevel()
    window.attributes('-topmost', True)
    label = tk.Label(window, text="Voici une nouvelle fenêtre!")
    label2 = tk.Label(window, text=entry1.get())
    label.pack(pady=20)
    label2.pack()
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

def afficher_etat_turbines():
    print("Turbine 1:", var_turbine1.get())
    print("Turbine 2:", var_turbine2.get())
    print("Turbine 3:", var_turbine3.get())
    print("Turbine 4:", var_turbine4.get())
    print("Turbine 5:", var_turbine5.get())
    
# Initialisation des entrees
turbine = tk.Label(text="Cocher les turbines indisponibles")
elevation = tk.Label(text="Elevation Totale")
debit = tk.Label(text="Debit Total")
entry1 = tk.Entry(fg="white", bg="grey", width=50)
entry2 = tk.Entry(fg="white", bg="grey", width=50)

# Initialisation des Boutons concernant les turbines à cocher
var_turbine1 = tk.BooleanVar()
var_turbine2 = tk.BooleanVar()
var_turbine3 = tk.BooleanVar()
var_turbine4 = tk.BooleanVar()
var_turbine5 = tk.BooleanVar()

turbine1 = tk.Checkbutton(window, text="Turbine 1", variable=var_turbine1)
turbine2 = tk.Checkbutton(window, text="Turbine 2", variable=var_turbine2)
turbine3 = tk.Checkbutton(window, text="Turbine 3", variable=var_turbine3)
turbine4 = tk.Checkbutton(window, text="Turbine 4", variable=var_turbine4)
turbine5 = tk.Checkbutton(window, text="Turbine 5", variable=var_turbine5)



# Bouton pour afficher l'état des turbines - utile pour debug
'''bouton_afficher_etat = tk.Button(window, text="Afficher l'état des turbines", command=afficher_etat_turbines)
bouton_afficher_etat.pack()
'''

#Initialisation des boutons
programmation_dynamique = tk.Button(
    text="Programmation Dynamique",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=open_window
)
nomad = tk.Button(
    text="NOMAD",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=open_window2
)


#Turbines
turbine.pack()
turbine1.pack()
turbine2.pack()
turbine3.pack()
turbine4.pack()
turbine5.pack()
#Champs de textes
debit.pack()
entry1.pack()
elevation.pack()
entry2.pack()
#Boutons
programmation_dynamique.pack()
nomad.pack()
#Initialisation de la fenetre
window.mainloop()
