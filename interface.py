import tkinter as tk
from tkinter import filedialog
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

def afficher_valeurs():
    valeurs_turbines = [entrees_turbines[i].get() for i in range(5)]
    print("Valeurs des turbines:", valeurs_turbines)
    for i, valeur in enumerate(valeurs_turbines):
        print(f"Valeur turbine {i+1}:", valeur)
        if int(valeur) >= 160:
            entrees_turbines[i].delete(0, tk.END)  # Efface la valeur
            entrees_turbines[i].insert(0, "160")   # Rétablit la valeur par défaut
    print("Valeurs des turbines:", valeurs_turbines)
    
   
def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename()
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)
    return file_path
    
def fopen():
    print(file_path)
	
    
      
# Initialisation des entrees
turbine = tk.Label(text="Cocher les turbines indisponibles")
elevation = tk.Label(text="Elevation Totale")
debit = tk.Label(text="Debit Total")
entry1 = tk.Entry(fg="white", bg="grey", width=50)
entry2 = tk.Entry(fg="white", bg="grey", width=50)

# Initialisation des entrees
label_file_path = tk.Label(text="Chemin du fichier:")
entry_file_path = tk.Entry(fg="black", bg="white", width=50)


# Variables pour stocker les valeurs des entrées
valeurs_turbines = [tk.StringVar(value="160") for _ in range(5)]

# Créer les entrées avec valeurs par défaut
entrees_turbines = [tk.Entry(window, textvariable=valeur) for valeur in valeurs_turbines]



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

# Bouton pour ouvrir la boîte de dialogue de sélection de fichiers
button_browse = tk.Button(window, text="Parcourir...", command=open_file_dialog)
OK = tk.Button(window, text="OK", command=fopen)

#Turbines
# Placer les entrées dans la fenêtre
for entree in entrees_turbines:
    entree.pack()

# Bouton pour afficher les valeurs
bouton_afficher_valeurs = tk.Button(window, text="Afficher les valeurs", command=afficher_valeurs)
bouton_afficher_valeurs.pack()
#Champs de textes
debit.pack()
entry1.pack()
elevation.pack()
entry2.pack()
#Boutons
programmation_dynamique.pack()
nomad.pack()
#Choix de fichier
label_file_path.pack()
entry_file_path.pack()
button_browse.pack()
OK.pack()
#Initialisation de la fenetre
window.mainloop()
