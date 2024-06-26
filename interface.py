import matplotlib.pyplot as plt
from tkinter import filedialog
import goddamoptimiser as GO
import pynomadopti  as PNO
import tkinter as tk
import pandas as pd
import numpy as np

def show_frame(frame):
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame.pack(fill='both', expand=True)

def lire_donnees_depuis_csv(chemin_fichier_csv):
    df = pd.read_csv(chemin_fichier_csv, delimiter=";")

    colonnes_requises = ['Niv Amont', 'Elav', 'Qtot', 'Qvan',
                         'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'P1', 'P2', 'P3', 'P4', 'P5']
    for col in colonnes_requises:
        if col not in df.columns:
            raise ValueError(f"La colonne {col} est manquante. Vérifiez le fichier CSV.")

    return df

def afficher_valeurs():
    valeurs_turbines = [entrees_turbines[i].get() for i in range(5)]
    print("Valeurs des turbines:", valeurs_turbines)
    for i, valeur in enumerate(valeurs_turbines):
        print(f"Valeur turbine {i+1}:", valeur)
        if int(valeur) >= 160:
            entrees_turbines[i].delete(0, tk.END)  # Efface la valeur
            entrees_turbines[i].insert(0, "160")   # Rétablit la valeur par défaut
    print("Valeurs des turbines:", valeurs_turbines)
    
    
def page2(debit, elevation, entrees_turbines):
    results = programmation_dynamique_func(debit, elevation, entrees_turbines)
    for widget in frame2.winfo_children():
        widget.destroy()
    tk.Label(frame2, text="Debit turbine 1 = "+str(results[1][0])+"\nDebit turbine 2 = "+str(results[1][1])+"\nDebit turbine 3 = "+str(results[1][2])+"\nDebit turbine 4 = "+str(results[1][3])+"\nDebit turbine 5 = "+str(results[1][4])+"\n").pack(pady=30)
    btn_to_frame1_from_frame2 = tk.Button(frame2, text="Retourner à la page de calculs", command=lambda: show_frame(frame1))
    btn_to_frame1_from_frame2.pack()
    show_frame(frame2)


def page3(debit, elevation, entrees_turbines):
	results = nomad_func(debit, elevation, entrees_turbines)
	for widget in frame3.winfo_children():
		widget.destroy()
	tk.Label(frame3, text="Debit turbine 1 = "+str(results[1][0])+"\nDebit turbine 2 = "+str(results[1][1])+"\nDebit turbine 3 = "+str(results[1][2])+"\nDebit turbine 4 = "+str(results[1][3])+"\nDebit turbine 5 = "+str(results[1][4])+"\n").pack(pady=30)
	btn_to_frame1_from_frame3 = tk.Button(frame3, text="Retourner à la page de calculs", command=lambda: show_frame(frame1))
	btn_to_frame1_from_frame3.pack()
	show_frame(frame3)

def programmation_dynamique_func(debit, elevation, entrees_turbines):
    results = GO.optimize(debit, elevation, entrees_turbines[0], entrees_turbines[1], entrees_turbines[2], entrees_turbines[3], entrees_turbines[4])
    return results
	
def nomad_func(debit, elevation, entrees_turbines):
    results = PNO.optimize(debit, elevation, entrees_turbines[0], entrees_turbines[1], entrees_turbines[2], entrees_turbines[3], entrees_turbines[4])
    return results
	

def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename()
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)
    return file_path
    
def fopen(file_path):
    df = lire_donnees_depuis_csv(file_path)
    elevations, debits = df['Niv Amont'].head(20), df['Qtot'].head(20)
    power_data_pynomad = []
    turbines_data_pynomad = []
    power_data_progdyn = []
    turbines_data_progdyn = []
    for i in range(20):
        ub = []
        for j in range(5):
            if df["Q"+str(j+1)][i] == 0:
                ub.append(0)
            else:
                ub.append(160)
        power_pynomad, turbines_pynomad = nomad_func(debits[i], elevations[i], ub)
        power_progdyn, turbines_progdyn = programmation_dynamique_func(debits[i], elevations[i], ub)   
        power_data_pynomad.append(power_pynomad)
        turbines_data_pynomad.append(turbines_pynomad)
        power_data_progdyn.append(power_progdyn)
        turbines_data_progdyn.append(turbines_progdyn)
    # Tracer le graphique
    x = [i for i in range(1, len(power_data_progdyn)+1)]
    plt.figure(figsize=(20, 9))
    plt.plot(x, power_data_pynomad, label='Pynomad')
    plt.plot(x, power_data_progdyn, label='Progdyn')
    plt.xlabel('Ligne du csv')
    plt.ylabel('Puissance (en unités appropriées)')
    plt.title('Puissance sur les 20 premières lignes du csv')
    plt.legend()
    plt.grid(True)
    plt.show()  

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


# Initialiser les variables qui seront affichees sur la page 1
elevation = tk.Label(frame1, text="Elevation Totale")
debit = tk.Label(frame1, text="Debit Total")
entryelev = tk.Entry(frame1, fg="white", bg="grey", width=50)
entrydeb = tk.Entry(frame1, fg="white", bg="grey", width=50)


# Initialisation des boutons
programmation_dynamique_btn = tk.Button(
	frame1,
    text="Programmation Dynamique",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command= lambda: page2(float(entrydeb.get()), float(entryelev.get()), [float(i.get()) for i in entrees_turbines])
)
nomad_btn = tk.Button(
	frame1,
    text="NOMAD",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command= lambda: page3(float(entrydeb.get()), float(entryelev.get()), [float(i.get()) for i in entrees_turbines])
)
#Selection de fichier
label_file_path = tk.Label(frame1, text="Chemin du fichier:")
entry_file_path = tk.Entry(frame1, fg="black", bg="white", width=50)
# Bouton pour ouvrir la boîte de dialogue de sélection de fichiers
button_browse = tk.Button(frame1, text="Parcourir...", command=open_file_dialog)
ok = tk.Button(frame1, text="OK", command=lambda: fopen(entry_file_path.get()))

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
entrydeb.pack()
elevation.pack()
entryelev.pack()
programmation_dynamique_btn.pack()
nomad_btn.pack()
#Choix de fichier
label_file_path.pack()
entry_file_path.pack()
button_browse.pack()
ok.pack()


# Affiche le premier cadre
show_frame(frame1)
# Démarre la boucle principale
root.mainloop()
