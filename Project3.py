import tkinter as tk
from tkinter import simpledialog
import numpy as np
import math
import sympy as sp
import matplotlib.pyplot as plt


#
# Geotechnical Design II - Dr. Hudyma, Project 3
# Model: Cantilever Wall in Granular Soils (no water table)
# Lecture Slides: Cantilever Walls - Traditional Textbook Methods- 2024, Slides 5 - 9
# @author Jessika Solleder
#

# Assumptions
gamma_gransoil = 20  # kN/m^3, unit weight of soil

# Step 1: Gather User Inputs
def get_phi():
    while True:
        try:
            phi_str = simpledialog.askstring("Input", "Please answer the value for Phi in degrees")
            phi = float(phi_str)  # Convert to float
            if phi > 0:
                return phi
            else:
                print("Phi must be greater than zero (0). Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid numerical value.")

            
def get_height():
    while True:
        try:
            height = float(simpledialog.askstring("Input", "Please enter the pile height above the dredge line in meters"))
            if 0 < height <= 6:
                return height
            else:
                print("Height above the dredge line must be greater than 0 and less than or equal to 6 meters.")
        except ValueError:
            print("Invalid input. Please enter a valid numerical value.")

# Step 2: Calculate Ka
def get_ka(phi):
    phi_rad = np.radians(phi)
    Ka = np.tan(np.radians(45) - phi_rad / 2) ** 2
    return Ka

#Step 3: Calculate Kp
def get_kp(phi):
    phi_rad = np.radians(phi)
    Kp = np.tan(np.radians(45) + phi_rad / 2) ** 2
    return Kp

#Step 4: Calculate Sigma 2
def get_sigma2(gamma_gransoil, height, Ka):
    sigma2 = gamma_gransoil * height * Ka
    return sigma2

#Step 5: Calculate L3
def get_l3(Kp, Ka, height):
    l3 = ((height * Ka)/ (Kp - Ka)) 
    return l3

#Step 6: Calculate P
def get_p (sigma2, height, l3):
    p = (0.5* sigma2 * height) + (0.5 * sigma2 * l3)
    return p

#Step 7: Calculate zbar
def get_zbar(height, l3):
    zbar = (l3 + (height / 3))
    return zbar

#Step 8: Calculate Sigma 5
def get_sigma5(gamma_gransoil, height, Kp, l3, Ka):
    sigma5 = (gamma_gransoil * height * Kp) + (gamma_gransoil * l3 * (Kp - Ka))
    return sigma5

#Step 9: Calculate A1
def get_a1(gamma_gransoil, Kp, Ka, sigma5):
    a1 = sigma5 / ((gamma_gransoil) * (Kp - Ka))
    return a1

#Step 10: Calculate A2
def get_a2(p, Kp, Ka, gamma_gransoil):
    a2 = (8 * p) / (gamma_gransoil * (Kp - Ka))
    return a2

#Step 11: Calculate A3
def get_a3(p,zbar, Kp, Ka, sigma5, gamma_gransoil):
    a3 = 6 * p *(2 * zbar * (Kp - Ka) + sigma5) / ((gamma_gransoil ** 2) * (Kp - Ka) ** 2)
    return a3

#Step 11: Calculate A4
def get_a4 (p, zbar, sigma5, gamma_gransoil, Kp, Ka):
    a4 = (p * (6 * zbar * sigma5) + (4 * p)) / ((gamma_gransoil ** 2 ) * ((Kp - Ka) ** 2))
    return a4

#Step 12: Calculate L4
    # Define the function to calculate L4
def get_l4(a1, a2, a3, a4):
    # Define the coefficients of the quartic equation: ax^4 + bx^3 + cx^2 + dx + e = 0
    coefficients = [1, a1, -a2, -a3, -a4]
    
    # Find the roots of the quartic equation
    roots = np.roots(coefficients)
    
    # Select the positive root
    positive_root = None
    for root in roots:
        if np.isreal(root) and root > 0:
            positive_root = root
            break
    
    return positive_root

#Step 13: Calculate sigma4
def get_sigma4(l4, Kp, Ka, sigma5, gamma_gransoil):
    sigma4 = sigma5 + (gamma_gransoil * l4 * (Kp - Ka))
    return sigma4

#Step 14: Calculate sigma3
def get_sigma3(l4, Kp, Ka, gamma_gransoil):
    sigma3 = l4 * (Kp - Ka) * gamma_gransoil
    return sigma3

#Step 15: Calculate l5
def get_l5(sigma3, l4, p, sigma4):
    l5 = ((sigma3 * l4) - (2 * p)) / (sigma3 + sigma4)
    return l5

 #Step 16: Pressure Distribution Diagram - see below
 
 #Step 17: Calculate Theoretical Depth
def get_Dtheor(l3, l4):
    Dtheor = l3 + l4
    return Dtheor

#Step 18: Calculate Actual Depth (provides FS in model)
def get_Dactual(Dtheor):
    Dactual = 1.3 * Dtheor
    return Dactual
#Step 19: Calculate Location of Maximum Moment (zprime)
def get_zprime(p, Kp, Ka, gamma_gransoil):
    zprime = math.sqrt((2*p) / ((Kp - Ka) * gamma_gransoil))
    return zprime
#Step 20: Calculate Maximum Moment
def get_Mmax(p, zbar, zprime, gamma_gransoil, Kp, Ka):
    Mmax = ((p * (zbar + zprime)) - (0.5 * ( gamma_gransoil * zprime ** 2) * (Kp - Ka)) * (zprime / 3))
    return Mmax

#Additional Option 1: Factored Moment Method




root = tk.Tk()
root.withdraw()

# Ensure the code is able to access variables throughout the program
phi = get_phi()
height = get_height()
Ka = get_ka(phi)
Kp = get_kp(phi)
sigma2 = get_sigma2(gamma_gransoil, height, Ka)
l3 = get_l3 (Kp, Ka, height)
zbar = get_zbar(height, l3)
p = get_p (sigma2, height, l3)
sigma5 = get_sigma5(gamma_gransoil, height, Kp, l3, Ka)
a1 = get_a1(gamma_gransoil, Kp, Ka, sigma5)
a2 = get_a2(p, Kp, Ka, gamma_gransoil)
a3 = get_a3(p,zbar, Kp, Ka, sigma5, gamma_gransoil)
a4 = get_a4 (p, zbar, sigma5, gamma_gransoil, Kp, Ka)
l4 = get_l4(a1, a2, a3, a4)
sigma4 = get_sigma4(l4, Kp, Ka, sigma5, gamma_gransoil)
sigma3 = get_sigma3(l4, Kp, Ka, gamma_gransoil)
l5 = get_l5(sigma3, l4, p, sigma4)
Dtheor = get_Dtheor(l3, l4)
Dactual = get_Dactual(Dtheor)
zprime = get_zprime(p, Kp, Ka, gamma_gransoil)
Mmax = get_Mmax(p, zbar, zprime, gamma_gransoil, Kp, Ka)

# Print the positive root of the quartic equation
print("Positive root of the quartic equation:", l4)

# Plot the Lateral Earth Pressure Diagram
    # Define the x and y coordinates of the points
x_values = [0, sigma2, 0, -sigma3, sigma4, 0 ]
y_values = [0, -height, -(height + l3), -(height + Dactual - l5), -(height + Dactual), -(height + Dactual)]
plt.axvline(x=3, color='red', linestyle='--')
    # Plot the points
plt.plot(x_values, y_values, marker='o', linestyle='-')  # Connect points with a line
plt.xlabel('X Axis')  # Label for the x-axis
plt.ylabel('Y Axis')  # Label for the y-axis
plt.title('Lateral Earth Pressure Diagram. Red Dotted Line = Sheet Pile')  # Title of the plot
plt.grid(True)  # Show grid
plt.show()  # Display the plot




