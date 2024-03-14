donnees = readtable('DataProjet2024.csv', delimiter=";");
Qtot_et_Qvan = donnees.Qtot + donnees.Qvan;

scatter(Qtot_et_Qvan, donnees.Elav)
title('Élévation Avale en fonction du Débit Total')
xlabel('Débit Total (Qtot + Qvan) [m^3/s]')
ylabel('Élévation Avale [m]')
grid on

mdl = fitlm(Qtot_et_Qvan, donnees.Elav);