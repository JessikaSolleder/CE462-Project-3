import cmath
from math import sin
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Assumptions
gamma_gransoil = 20  # kN/m^3, unit weight of soil
gamma_claysoil = 24  # kN/m^3, unit weight of soil below groundwater table

def quadratic_roots(c, height, p1):
    a = 4 * c - gamma_gransoil * height
    b = 2 * p1
    c1 = (p1 * (p1 + 12 * c * (height / 3))) / (gamma_gransoil * height + 2 * c)
    
    # Calculate the discriminant
    discriminant = (b**2) - (4*a*c1)
    
    # Check if the discriminant is positive, negative, or zero
    if discriminant >= 0:
        # If the discriminant is non-negative, there are real roots
        root1 = (-b + discriminant**0.5) / (2*a)
        root2 = (-b - discriminant**0.5) / (2*a)
        
        # Choose the positive root
        if root1 >= 0:
            return root1, None
        elif root2 >= 0:
            return root2, None
        else:
            return None, None  # No positive roots
    else:
        # If the discriminant is negative, there are no real roots
        return None, None

def calculate_D_actual(height, phi, c):
    p1 = 0.5 * ((height ** 2)* np.tan(np.radians(45) - np.radians(phi) / 2) ** 2 * gamma_gransoil)
    root, _ = quadratic_roots(c, height, p1)
    if root is not None:
        D_actual = 1.5 * root
        print("D_actual:", D_actual)
        return D_actual
    else:
        print("No positive real root found. Please review your inputs.")
        return None

def calculate_M_max(height, phi, c):
    try:
        p1 = 0.5 * ((height ** 2)* np.tan(np.radians(45) - np.radians(phi) / 2) ** 2 * gamma_gransoil)
        z1 = height / 3
        sigma6 = gamma_gransoil * height * np.tan(np.radians(45) - np.radians(phi) / 2) ** 2
        D_actual = calculate_D_actual(height, phi, c)
        
        if D_actual is not None:
            M_max_location = p1 / sigma6
            M_max = p1 * (M_max_location + z1) - ((sigma6 * (M_max_location ** 2)/ 2))

            # Formatting values to 3 significant figures
            D_actual_rounded = "{:.3g}".format(D_actual)
            M_max_rounded = "{:.3g}".format(M_max)

            # Creating the message
            message = f"Required Embedment Depth: {D_actual_rounded} meters\n\n"
            message += f"Maximum Bending Moment: {M_max_rounded} kilonewton-meters"
            messagebox.showinfo("Results", message)
        
    except ValueError:
        messagebox.showerror("Error", "Please ensure all inputs are numeric.")
        
####################################################################################
####################################################################################


####################################################################################
####################################################################################
root = tk.Tk()
root.title("Sheet Pile Calculator")
        
root = tk.Tk()
root.title("Sheet Pile Calculator")

# Entry fields for input parameters
tk.Label(root, text="Enter sheet pile height above the soil (m):").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Enter angle of internal friction of the granular soil (degrees):").pack()
phi_entry = tk.Entry(root)
phi_entry.pack()

tk.Label(root, text="Enter the cohesion of the clay layer (kPa):").pack()
c_entry = tk.Entry(root)
c_entry.pack()

# Button to trigger the calculation
calculate_btn = tk.Button(root, text="Calculate", command=lambda: calculate_M_max(float(height_entry.get()), float(phi_entry.get()), float(c_entry.get())))
calculate_btn.pack()

root.mainloop()
