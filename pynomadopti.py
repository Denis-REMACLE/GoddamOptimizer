import PyNomad
import numpy as np
import pandas as pd

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

def modele_puissance(debit_turbine, hauteur_chute_brute, i):
    modele_turbine = [(-4.63382637e-04, -1.69195505e-01, 1.26899438e+01, 3.63335578e-01, -2.36531963e+02),
                    (-2.75024556e-04, -1.79623689e-01, 1.37759472e+01, 3.53094268e-01, -2.61927181e+02),
                    (-6.33871586e-04, -2.18730415e-01, 1.57293911e+01, 3.88788224e-01, -2.82334058e+02),
                    (-5.25471618e-04, -2.44235045e-01, 1.81190162e+01, 4.08210465e-01, -3.36417000e+02),
                    (-5.85633942e-04, -1.56392085e-01, 1.19691372e+01, 4.03504883e-01, -2.27110218e+02)]
    a, b, c, d, e = modele_turbine[i]
    hauteur_chute_nette = hauteur_chute_brute - (0.5 * 10**(-5)) * debit_turbine**2
    print(debit_turbine)
    return a * (debit_turbine**2) + b * (hauteur_chute_nette**2) + c * hauteur_chute_nette + d * debit_turbine + e

#fonction pour l'optimisation
#faudra penser a boucler dans le csv pour tester les 100 premières combinaisons pour les deux floats
def production_totale(debit_total, elevation_amont, ub, x):
    try:
        dim = x.size()
        elevation_avale = modele_elevation_avale(debit_total) # 578.01 = débit total
        hauteur_chute_brute = elevation_amont - elevation_avale # 137.90 = élévation amont
        result = np.sum([modele_puissance(x.get_coord(i), hauteur_chute_brute, i) for i in range(dim)])
        for i in range(dim):
            if ub[i] == 0 and x.get_coord(i) != 0:
                result-=result
        if debit_total < np.sum([x.get_coord(i) for i in range(dim)]):
            result-=result
        x.setBBO(str(-result).encode("UTF-8"))
    except Exception as e:
        print("Unexpected error in bb_block()", str(e))
        return 0
    return 1

def production_totale_closure(debit_total, elevation_amont, ub):
    def production_totale_closure_impl(x):
        return production_totale(debit_total, elevation_amont, ub, x)
    return production_totale_closure_impl


def optimize(debit_total, elevation_amont, t1, t2, t3, t4, t5):
    x0 = [0, 0, 0, 0, 0]
    lb = [0, 0, 0, 0, 0]
    ub = [t1, t2, t3, t4, t5]

    parametres = [
        'DIMENSION 5',
        'BB_OUTPUT_TYPE OBJ',
        'MAX_BB_EVAL 100',
        'DISPLAY_STATS BBE OBJ',
        'X0 ( 0 0 0 0 0 )',
        'LOWER_BOUND ( 0 0 0 0 0 )',
        'UPPER_BOUND * 160',
    ]

    # Lancement de l'optimisation avec NOMAD
    resultat = PyNomad.optimize(production_totale_closure(debit_total, elevation_amont, ub), x0, lb, ub, parametres)
    #ça marche pas envie de crever profonde
    # Affichage des résultats
    return -resultat["f_best"], resultat["x_best"]
