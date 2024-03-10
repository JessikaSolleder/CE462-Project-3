import numpy as np
import matplotlib.pyplot as plt

# Constants
gamma_soil = 18  # kN/m^3, unit weight of soil
K0 = 0.5  # At-rest earth pressure coefficient, placeholder value

def calculate_embedment_depth_and_moment(height, phi, c):
# Calculate the required embedment depth and maximum moment
#for a cantilever sheet pile in soil.
    
# :param height: Height of the sheet pile in feet
# :param phi: Angle of internal friction of granular soil in degrees
# :param c: Cohesion of clay soil in kPa
# :return: Embedment depth (m) and maximum moment (kNm)
   
    # Check if sheet pile height is too tall
    if height > 6.000001:  # 20 feet in meters
        return "Sheet pile height exceeds cantilever limit (6 meters)", 0
    
    # Calculate lateral earth pressure coefficients using Rankine's theory
    phi_rad = np.radians(phi)
    Ka = np.tan(np.pi/4 - phi_rad/2)**2  # Active earth pressure coefficient
    
    # For simplicity, assuming a uniform soil condition below the excavation depth
    # Calculate required embedment depth
    D = height * (2 * Ka)  # Simplified assumption
    
    # Calculate maximum moment
    M_max = 0.5 * gamma_soil * Ka * height**2 * D  # Simplified assumption
    
    return D, M_max

# User inputs
height = float(input("Enter sheet pile height (m): "))
phi = float(input("Enter angle of internal friction (degrees): "))
c = float(input("Enter value for soil cohesion (kPa): "))

# Calculation
embedment_depth, max_moment = calculate_embedment_depth_and_moment(height, phi, c)
print(f"Required Embedment Depth: {embedment_depth} m, Maximum Moment: {max_moment} kNm")

def plot_lateral_earth_pressure(height, phi):

    # Plot the lateral earth pressure distribution for a given height and phi.
    phi_rad = np.radians(phi)
    Ka = np.tan(np.pi/4 - phi_rad/2)**2
    depths = np.linspace(0, height, 100)
    pressures = gamma_soil * depths * Ka
    
    plt.figure()
    plt.plot(pressures, -depths)
    plt.xlabel('Lateral Earth Pressure (kPa)')
    plt.ylabel('Depth (m)')
    plt.title('Lateral Earth Pressure Distribution')
    plt.grid(True)
    plt.show()

def sensitivity_analysis(parameter_range, height, parameter_type='phi'):
    """
    Perform sensitivity analysis on shear strength parameters.
    
    :param parameter_range: Range of values for the parameter being analyzed.
    :param height: Height of the sheet pile in meters
    :param parameter_type: Type of parameter ('phi' or 'c') for the analysis.
    """
    embedment_depths = []
    max_moments = []
    
    for param in parameter_range:
        if parameter_type == 'phi':
            D, M = calculate_embedment_depth_and_moment(height, param, c)
        else:  # 'c'
            D, M = calculate_embedment_depth_and_moment(height, phi, param)
        embedment_depths.append(D)
        max_moments.append(M)
    
    # Plotting results
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(parameter_range, embedment_depths)
    plt.xlabel(f'{parameter_type.upper()}')
    plt.ylabel('Embedment Depth (m)')
    plt.grid(True)
    plt.title('Sensitivity Analysis: Embedment Depth')
    
    plt.subplot(1, 2, 2)
    plt.plot(parameter_range, max_moments)
    plt.xlabel(f'{parameter_type.upper()}')
    plt.ylabel('Maximum Moment (kNm)')
    plt.grid(True)
    plt.title('Sensitivity Analysis: Maximum Moment')
    
    plt.tight_layout()
    plt.show()

# Execute plotting and sensitivity analysis
plot_lateral_earth_pressure(height, phi)

# Sensitivity analysis parameters
phi_range = np.linspace(20, 40, 5)  # Example range for phi
sensitivity_analysis(phi_range, height, 'phi')
