import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

filepath = "DataProjet2024.csv"

def lire_donnees_depuis_csv(chemin_fichier_csv):
    df = pd.read_csv(chemin_fichier_csv, delimiter=";")
    
    colonnes_requises = ['Niv Amont', 'Elav', 'Qtot', 'Qvan',
                         'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'P1', 'P2', 'P3', 'P4', 'P5']
    for col in colonnes_requises:
        if col not in df.columns:
            raise ValueError(f"La colonne {col} est manquante. Vérifiez le fichier CSV.")
    
    return df

def tracer_modele_puissance(x_data, y_data, z_data, params, titre='Modélisation de la Puissance Produite'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(x_data, y_data, z_data, c='blue', marker='o', label='Données réelles')
    
    X, Y = np.meshgrid(np.linspace(min(x_data), max(x_data), 50), np.linspace(min(y_data), max(y_data), 50))
    Z = params[0] * X * Y + params[1]
    
    ax.plot_surface(X, Y, Z, color='red', alpha=0.5, edgecolor='none')
    
    ax.set_xlabel('Débit Turbiné')
    ax.set_ylabel('Hauteur de Chute Nette')
    ax.set_zlabel('Puissance Produite')
    ax.legend()
    
    plt.show()

def calculer_hauteur_chute_nette(elevation_amont, elevation_avale, debit_turbine):
    pertes = (0.5 * 10**(-5)) * debit_turbine**2
    return elevation_amont - elevation_avale - pertes

def modele_puissance(x, a, b, c):
    debit_turbine, hauteur_chute_nette = x
    return a + b * debit_turbine + c * hauteur_chute_nette

df = lire_donnees_depuis_csv(filepath)

df['Hauteur_Chute_Nette1'] = calculer_hauteur_chute_nette(df['Niv Amont'], df['Elav'], df['Q1'])
params, _ = curve_fit(modele_puissance, (df['Q1'], df['Hauteur_Chute_Nette1']), df['P1'])
print("Paramètres du modèle pour la Turbine 1: ", params)

df['Hauteur_Chute_Nette2'] = calculer_hauteur_chute_nette(df['Niv Amont'], df['Elav'], df['Q2'])
params, _ = curve_fit(modele_puissance, (df['Q2'], df['Hauteur_Chute_Nette2']), df['P2'])
print("Paramètres du modèle pour la Turbine 2: ", params)

df['Hauteur_Chute_Nette3'] = calculer_hauteur_chute_nette(df['Niv Amont'], df['Elav'], df['Q3'])
params, _ = curve_fit(modele_puissance, (df['Q3'], df['Hauteur_Chute_Nette3']), df['P3'])
print("Paramètres du modèle pour la Turbine 3: ", params)

df['Hauteur_Chute_Nette4'] = calculer_hauteur_chute_nette(df['Niv Amont'], df['Elav'], df['Q4'])
params, _ = curve_fit(modele_puissance, (df['Q4'], df['Hauteur_Chute_Nette4']), df['P4'])
print("Paramètres du modèle pour la Turbine 4: ", params)

df['Hauteur_Chute_Nette5'] = calculer_hauteur_chute_nette(df['Niv Amont'], df['Elav'], df['Q5'])
params, _ = curve_fit(modele_puissance, (df['Q5'], df['Hauteur_Chute_Nette5']), df['P5'])
print("Paramètres du modèle pour la Turbine 5: ", params)