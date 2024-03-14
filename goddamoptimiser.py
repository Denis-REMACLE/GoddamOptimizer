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
    modele_turbine = [(0.00844367, 0.31262701) , (0.008863, 0.28795731), (0.00854668, 0.39207585), (0.0089237, 0.63343666), (0.0089318, 0.60632745)]
    a, b = modele_turbine[i]
    return a * debit_turbine * hauteur_chute_nette + b

def production_totale(x, debit_total_disponible, elevation_amont):
    elevation_avale = modele_elevation_avale(debit_total_disponible)
    hauteur_chute_brute = elevation_amont - elevation_avale
    hauteur_chute_nette = hauteur_chute_brute - (0.5 * 10**(-5)) * x**2
    result = np.sum([modele_puissance(x[i], hauteur_chute_nette, i) for i in range(len(x))])
    return -result

def optimize(elevation_amont, debit_total_disponible, bounds):
    contraintes = ({'type': 'ineq', 'fun': lambda x: debit_total_disponible - sum(x)})
    x0 = [0] * len(bounds)

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
        return np.round(optimized_debits, 2), production_turbine, sum(production_turbine)

    else:
        print("L'optimisation n'a pas réussi.")

def main():
    parser = argparse.ArgumentParser(
        prog="GoddamOptimiser",
        description="This script optimises dams",
    )
    parser.add_argument(
        "-c",
        "--csv",
        type=str,
        default=False,
        help="Uses a csv to optimise multiple times",
    )
    args = parser.parse_args()
    if args.csv:
        df = lire_donnees_depuis_csv(args.csv)
        elevations, debits = df['Niv Amont'].head(100), df['Qtot'].head(100)
        for i in range(100):
            bounds = []
            for j in range(5):
                if df["Q"+str(j+1)][i] == 0:
                    bounds.append((0, 0))
                else:
                    bounds.append((0, 160))
            print(optimize(elevations[i], debits[i], bounds))

if __name__ == "__main__":
    main()