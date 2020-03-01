% MATLAB script to generate a reference value used in the
% test_getMfp and test_getMassAttenCoff python unit tests

function getattenCoeff()
% calculate an mass attenuation coefficient
% at 0.66 MeV
format long
energy = 0.66;
density = 0.001205;

energyArray = [0.010, 0.015, 0.020, 0.030, 0.040, 0.050, 0.060, ...
               0.080, 0.100, 0.150, 0.200, 0.300, 0.400, 0.500, ...
               0.600, 0.800, 1.000, 1.500, 2.000, 3.000, 4.000, ...
               5.000, 6.000, 8.000, 10.000, 15.000, 20.000, 30.000];
coeffArray = [4.961E+00, 1.525E+00, 7.210E-01, 3.248E-01, 2.311E-01, ...
              1.964E-01, 1.791E-01, 1.614E-01, 1.509E-01, 1.341E-01, ...
              1.225E-01, 1.063E-01, 9.525E-02, 8.694E-02, 8.041E-02, ...
              7.065E-02, 6.349E-02, 5.168E-02, 4.440E-02, 3.573E-02, ...
              3.072E-02, 2.745E-02, 2.516E-02, 2.220E-02, 2.040E-02, ...
              1.805E-02, 1.702E-02, 1.624E-02];
          
xs = interp1(energyArray, coeffArray, energy)
distance = 10;
mfp = distance*xs*density

end


