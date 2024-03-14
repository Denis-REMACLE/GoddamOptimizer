import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

filepath = "DataProjet2024.csv"

def load_data_from_csv(chemin_fichier_csv):
    """
    Lit un fichier CSV et extrait les colonnes pour 'Qtot' et 'Elevations'.
    
    Paramètres :
    - chemin_fichier_csv : Le chemin complet vers le fichier CSV.
    
    Retourne :
    - Un tuple de deux arrays: (Qtot, Elevations)
    """
    df = pd.read_csv(chemin_fichier_csv, delimiter=";")
    
    Qtot = df['Qtot'].to_numpy()
    Elevations = df['Elav'].to_numpy()
    
    return Qtot, Elevations

def poly_model(x, a, b, c):
    return a * x**2 + b * x + c

debits, elevations = load_data_from_csv(filepath)
params, covariance = curve_fit(poly_model, debits, elevations)
a, b, c = params
debits_fit = np.linspace(debits.min(), debits.max(), 500)
elevations_fit = poly_model(debits_fit, a, b, c)

plt.figure(figsize=(10, 6))
plt.scatter(debits, elevations, label='Données observées')
plt.plot(debits_fit, elevations_fit, color='red', label='Courbe ajustée')
plt.xlabel('Débit total turbiné (Qtot)')
plt.ylabel('Élévation avale')
plt.title('Modélisation de l\'Élévation Avale en Fonction du Débit Total')
plt.legend()
plt.show()

print(params)