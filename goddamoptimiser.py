import argparse
import numpy as np
import pandas as pd
from scipy.optimize import minimize

def lire_donnees_depuis_csv(chemin_fichier_csv):
    df = pd.read_csv(chemin_fichier_csv, delimiter=";")
    
    colonnes_requises = ['Niv Amont', 'Elav', 'Qtot', 'Qvan',
                         'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'P1', 'P2', 'P3', 'P4', 'P5']
    for col in colonnes_requises:
        if col not in df.columns:
            raise ValueError(f"La colonne {col} est manquante. Vérifiez le fichier CSV.")
    
    return df

def modele_elevation_avale(debit_total):
    a, b, c = -1.45329562e-06, 7.02352036e-03, 9.99807998e+01
    return a * debit_total**2 + b * debit_total + c

def modele_puissance(debit_turbine, hauteur_chute_nette, i):
    modele_turbine = [(-4.63382637e-04, -1.69195505e-01, 1.26899438e+01, 3.63335578e-01, -2.36531963e+02),
                    (-2.75024556e-04, -1.79623689e-01, 1.37759472e+01, 3.53094268e-01, -2.61927181e+02),
                    (-6.33871586e-04, -2.18730415e-01, 1.57293911e+01, 3.88788224e-01, -2.82334058e+02),
                    (-5.25471618e-04, -2.44235045e-01, 1.81190162e+01, 4.08210465e-01, -3.36417000e+02),
                    (-5.85633942e-04, -1.56392085e-01, 1.19691372e+01, 4.03504883e-01, -2.27110218e+02)]
    a, b, c, d, e = modele_turbine[i]
    return a * (debit_turbine**2) + b * (hauteur_chute_nette**2) + c * hauteur_chute_nette + d * debit_turbine + e

def production_totale(x, debit_total_disponible, elevation_amont):
    elevation_avale = modele_elevation_avale(debit_total_disponible)
    hauteur_chute_brute = elevation_amont - elevation_avale
    hauteur_chute_nette = hauteur_chute_brute - (0.5 * 10**(-5)) * x**2
    result = np.sum([modele_puissance(x[i], hauteur_chute_nette, i) for i in range(len(x))])
    return -result

def optimize(debit_total_disponible, elevation_amont,t1, t2, t3, t4, t5):
    contraintes = ({'type': 'ineq', 'fun': lambda x: debit_total_disponible - sum(x)})
    x0 = [t1, t2, t3, t4, t5]
    bounds = [(0, t1),(0, t2),(0, t3),(0, t4),(0, t5)]
    result = minimize(production_totale, x0, args=(debit_total_disponible, elevation_amont), method='SLSQP', bounds=bounds, constraints=contraintes)

    if result.success:
        optimized_debits = result.x
        elevation_avale = modele_elevation_avale(debit_total_disponible)
        hauteur_chute_brute = elevation_amont - elevation_avale
        production_turbine = []
        for i, debit in enumerate(optimized_debits):
            hauteur_chute_nette = hauteur_chute_brute - (0.5 * 10**(-5)) * debit**2
            production = modele_puissance(debit, hauteur_chute_nette, i)
            production_turbine.append(production)
        return sum(production_turbine)

    else:
        print("L'optimisation n'a pas réussi.")
