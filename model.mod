param turbines := 5;
param Qmax{i in 1..turbines};
param Qmin{i in 1..turbines};
param elevationAmont;
param elevationAval;
param coefficientPerte := 0.5 * 10^-5;

var Q{i in 1..turbines} >= 0;
var hauteurChuteNette >= 0;

maximize productionTotale:
    sum{i in 1..turbines} puissanceTurbine(i, Q[i], hauteurChuteNette);

func puissanceTurbine{j in 1..turbines}(int j, real Q, real hauteur) := ... 

subject to contrainteHauteurChuteNette:
    hauteurChuteNette = elevationAmont - elevationAval - sum{i in 1..turbines} (coefficientPerte * Q[i]^2);

subject to contrainteDebitMax{i in 1..turbines}:
    Q[i] <= Qmax[i];

subject to contrainteDebitMin{i in 1..turbines}:
    Q[i] >= Qmin[i];

subject to contrainteDebitTotal:
    sum{i in 1..turbines} Q[i] <= Qtotal;