import numpy as np
import matplotlib.pyplot as plt

# Constants
gamma_soil = 18  # kN/m^3, unit weight of soil
K0 = 0.5  # At-rest earth pressure coefficient, placeholder value

def calculate_embedment_depth_and_moment(height, phi, c):
    """
    Calculate the required embedment depth and maximum moment
    for a cantilever sheet pile in soil.
    
    :param height: Height of the sheet pile in meters
    :param phi: Angle of internal friction of granular soil in degrees
    :param c: Cohesion of clay soil in kPa
    :return: Embedment depth (m) and maximum moment (kNm)
    """
    # Check if sheet pile height is too tall
    if height > 6.1:  # 20 feet in meters
        return "Sheet pile height exceeds cantilever limit (20 feet)", 0
    
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
print(f"Required Embedment Depth: {embedment_depth}m, Maximum Moment: {max_moment}kNm")

