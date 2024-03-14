fichierCSV = 'DataProjet2024.csv';
donnees = readtable(fichierCSV, delimiter=";");
HauteurChuteNette = donnees.NivAmont - donnees.Elav;

Q1 = donnees.Q1 - 0.5 * 10^(-5) * donnees.Q1.^2;
P1 = donnees.P1;

mdlTurbine1 = fitlm([HauteurChuteNette, Q1], P1);

Q2 = HauteurChuteNette - 0.5 * 10^(-5) * donnees.Q2.^2;
P2 = donnees.P2;

mdlTurbine2 = fitlm([HauteurChuteNette, Q2], P2);

Q3 = donnees.Q3 - 0.5 * 10^(-5) * donnees.Q3.^2;
P3 = donnees.P3;

mdlTurbine3 = fitlm([HauteurChuteNette, Q3], P3);

Q4 = donnees.Q4 - 0.5 * 10^(-5) * donnees.Q4.^2;
P4 = donnees.P4;

mdlTurbine4 = fitlm([HauteurChuteNette, Q4], P4);

Q5 = donnees.Q5 - 0.5 * 10^(-5) * donnees.Q5.^2;
P5 = donnees.P5;

mdlTurbine5 = fitlm([HauteurChuteNette, Q5], P5);