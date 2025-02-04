% MATLAB script to generate reference values 
% In test_material.py
%   See test_getBuildupFactor()
% Uses:
%   akima.m
%   alimaSlopes.m

function buildupFactor()
    % calculate an air GP buildup factor
    % at 0.66 MeV and 10 MFP
    format long
    energy = 0.66;
    mfp = 10;
    
    gpEnergy = [0.015, 0.020, 0.030, 0.040, 0.050, 0.060, 0.080, ...
                0.100, 0.150, 0.200, 0.300, 0.400, 0.500, 0.600, ...
                0.800, 1.000, 1.500, 2.000, 3.000, 4.000, 5.000, ...
                6.000, 8.000, 10.000, 15.000]'   ;
            
    gpCoeff =    [1.170, 0.459, 0.175, 13.73, -0.0862; ...
     1.407, 0.512, 0.161, 14.40, -0.0819; ...
     2.292, 0.693, 0.102, 13.34, -0.0484; ...
     3.390, 1.052, -0.004, 19.76, -0.0068; ...
     4.322, 1.383, -0.071, 13.51, 0.0270; ...
     4.837, 1.653, -0.115, 13.66, 0.0511; ...
     4.929, 1.983, -0.159, 13.74, 0.0730; ...
     4.580, 2.146, -0.178, 12.83, 0.0759; ...
     3.894, 2.148, -0.173, 14.46, 0.0698; ...
     3.345, 2.147, -0.176, 14.08, 0.0719; ...
     2.887, 1.990, -0.160, 14.13, 0.0633; ...
     2.635, 1.860, -0.146, 14.24, 0.0583; ...
     2.496, 1.736, -0.130, 14.32, 0.0505; ...
     2.371, 1.656, -0.120, 14.27, 0.0472; ...
     2.207, 1.532, -0.103, 14.12, 0.0425; ...
     2.102, 1.428, -0.086, 14.35, 0.0344; ...
     1.939, 1.265, -0.057, 14.24, 0.0232; ...
     1.835, 1.173, -0.039, 14.07, 0.0161; ...
     1.712, 1.051, -0.011, 13.67, 0.0024; ...
     1.627, 0.983, 0.006, 13.51, -0.0051; ...
     1.558, 0.943, 0.017, 13.82, -0.0117; ...
     1.505, 0.915, 0.025, 16.37, -0.0231; ...
     1.418, 0.891, 0.032, 12.06, -0.0167; ...
     1.358, 0.875, 0.037, 14.01, -0.0226; ...
     1.267, 0.844, 0.048, 14.55, -0.0344]    ; 
  
    % b = interp1(gpEnergy, gpCoeff(:,1), energy, 'makima')
    % c = interp1(gpEnergy, gpCoeff(:,2), energy, 'makima')
    % a = interp1(gpEnergy, gpCoeff(:,3), energy, 'makima')
    % X = interp1(gpEnergy, gpCoeff(:,4), energy, 'makima')
    % d = interp1(gpEnergy, gpCoeff(:,5), energy, 'makima')
 
    b = akima(log(gpEnergy), gpCoeff(:,1), log(energy));
    c = akima(log(gpEnergy), gpCoeff(:,2), log(energy));
    a = akima(log(gpEnergy), gpCoeff(:,3), log(energy));
    X = akima(log(gpEnergy), gpCoeff(:,4), log(energy));
    d = akima(log(gpEnergy), gpCoeff(:,5), log(energy));

    K = (c * (mfp^a)) + (d * (tanh(mfp/X -2) - tanh(-2))) / (1 - tanh(-2));

    if K == 1
        GP = 1 + (b-1)*mfp;
    else
        GP = 1 + (b-1)*((K^mfp) - 1)/(K -1);
    end
fprintf('=================================\n')
fprintf('Matlab script buildupFactor.m\n')
fprintf('Reference values for Air at %g MeV \n\n', energy)
fprintf('test_getBuildupFactor() Function: \n')
fprintf('Geometric progression buildup factor at %g mfp is %.8g \n\n', mfp, GP)
end