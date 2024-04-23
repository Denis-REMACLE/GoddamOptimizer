import tkinter as tk
from tkinter import filedialog
import goddamoptimiser as GO
import pynomadopti  as PNO

def show_frame(frame):
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame.pack(fill='both', expand=True)


def afficher_valeurs():
    valeurs_turbines = [entrees_turbines[i].get() for i in range(5)]
    print("Valeurs des turbines:", valeurs_turbines)
    for i, valeur in enumerate(valeurs_turbines):
        print(f"Valeur turbine {i+1}:", valeur)
        if int(valeur) >= 160:
            entrees_turbines[i].delete(0, tk.END)  # Efface la valeur
            entrees_turbines[i].insert(0, "160")   # Rétablit la valeur par défaut
    print("Valeurs des turbines:", valeurs_turbines)
    
    
def page2():
	programmation_dynamique_func()
	for widget in frame2.winfo_children():
		widget.destroy()
	tk.Label(frame2, text="Ceci est la page 2").pack(pady=20)
	btn_to_frame1_from_frame2 = tk.Button(frame2, text="Retourner à la page de calculs", command=lambda: show_frame(frame1))
	btn_to_frame1_from_frame2.pack()
	show_frame(frame2)


def page3():
	nomad_func()
	for widget in frame3.winfo_children():
		widget.destroy()
	tk.Label(frame3, text="Ceci est la page 3").pack(pady=30)
	btn_to_frame1_from_frame3 = tk.Button(frame3, text="Retourner à la page de calculs", command=lambda: show_frame(frame1))
	btn_to_frame1_from_frame3.pack()
	show_frame(frame3)

def programmation_dynamique_func():
	...
	
def nomad_func():
	...
	

def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename()
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)
    return file_path
    
def fopen():
    print(file_path)



# Crée l'instance de Tk
root = tk.Tk()
root.title("Interface Utilisateur")

# Crée des cadres pour chaque partie de l'application
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)

# Variables pour stocker les valeurs des entrées
valeurs_turbines = [tk.StringVar(value="160") for _ in range(5)]

# Créer les entrées avec valeurs par défaut
entrees_turbines = [tk.Entry(frame1, textvariable=valeur) for valeur in valeurs_turbines]

# Initialisation des boutons
programmation_dynamique_btn = tk.Button(
	frame1,
    text="Programmation Dynamique",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=page2
)
nomad_btn = tk.Button(
	frame1,
    text="NOMAD",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=page3
)


# Initialiser les variables qui seront affichees sur la page 1
elevation = tk.Label(frame1, text="Elevation Totale")
debit = tk.Label(frame1, text="Debit Total")
entry1 = tk.Entry(frame1, fg="white", bg="grey", width=50)
entry2 = tk.Entry(frame1, fg="white", bg="grey", width=50)
#Selection de fichier
label_file_path = tk.Label(frame1, text="Chemin du fichier:")
entry_file_path = tk.Entry(frame1, fg="black", bg="white", width=50)
# Bouton pour ouvrir la boîte de dialogue de sélection de fichiers
button_browse = tk.Button(frame1, text="Parcourir...", command=open_file_dialog)
OK = tk.Button(frame1, text="OK", command=fopen)

# Ce qui sera affiche sur la Frame 1
tk.Label(frame1, text="Entrer la puissance maximale disponible pour chaque turbine").pack()
# Champs de texte Turbines
for entree in entrees_turbines:
    entree.pack()
# Bouton pour afficher les valeurs
bouton_afficher_valeurs = tk.Button(frame1, text="Afficher les valeurs", command=afficher_valeurs)
bouton_afficher_valeurs.pack()
#Champs de Texte Elevation Debit
debit.pack()
entry1.pack()
elevation.pack()
entry2.pack()
programmation_dynamique_btn.pack()
nomad_btn.pack()
#Choix de fichier
label_file_path.pack()
entry_file_path.pack()
button_browse.pack()
OK.pack()


# Affiche le premier cadre
show_frame(frame1)
# Démarre la boucle principale
root.mainloop()
